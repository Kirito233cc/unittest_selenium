"""
使用sqlalchemy替代pymysql，将数据表对象化（ORM）
同时sqlalchemy支持数据库连接池，可以减少每次调用连接关闭数据库所产生的开销
"""
import sys
sys.path.append("..")


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import datetime

from time import sleep

from flask import Blueprint, request, jsonify

from sqlalchemy.orm import sessionmaker

from celery.result import AsyncResult

from celery_thing.celeryapp import celery_app

from data_object.table_page_module import Page_module
from data_object.table_page_module_detail import Page_module_detail

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.common.by import By

from config.settings import Config
from user.user import token_check


# 进行蓝图注册
page_module = Blueprint('page_module', __name__)


class execute_module:
    def __init__(self, driver):
        self.driver = driver
        # self.driver.implicitly_wait(30)

    def execute_selenium(self, module_name='login'):
        driver = self.driver
        driver.set_window_size(1920, 1080)
        """根据模块名字执行对应的selenium"""
        conn = Config.engine.connect()
        elements = conn.execute(
            "select a.module_name,b.operate_step,c.element_name, e.element_locate_name, c.element_address, d.operate_name, b.send_msg, b.pause_time from page_module a join page_module_detail b on a.id = b.page_module_id left join element c on b.element_id = c.id join element_operate d on b.operate_type = d.operate_type left join element_locate e on c.element_type = e.element_type where a.module_name = '%s' order by b.operate_step " % module_name).fetchall()
        # # 创建DBSession类型
        # DBSession = sessionmaker(bind=conn)
        # # 创建session对象
        # session = DBSession()
        # # 创建Eelement对象,多表关联查询出结果
        # elements = session.query(Page_module.module_name,
        #                          Page_module_detail.operate_step,
        #                          Element.element_name,
        #                          Element_locate.element_locate_name,
        #                          Element.element_address,
        #                          Element_operate.operate_name,
        #                          Page_module_detail.send_msg,
        #                          Page_module_detail.pause_time). \
        #     select_from(Page_module). \
        #     join(Page_module_detail, Page_module.id == Page_module_detail.page_module_id). \
        #     join(Element, Page_module_detail.element_id == Element.id, isouter=True). \
        #     join(Element_operate, Page_module_detail.operate_type == Element_operate.operate_type). \
        #     join(Element_locate, Element.element_type == Element_locate.element_type, isouter=True). \
        #     filter(Page_module.module_name == module_name).order_by(Page_module_detail.operate_step).all()
        # # 关闭连接
        # session.close()
        conn.close()
        if not elements:
            raise ValueError("无法找到对应的模块")
        else:
            # 逐个执行selenium操作
            for step in elements:
                # by_func元素搜索方法,by_value元素搜索的值,action元素操作,input_value元素操作传的值,sleep_time等待时间
                by_func = step[3]
                by_value = step[4]
                action = step[-3]
                input_value = step[-2]
                sleep_time = step[-1]
                operateName = step[5]
                if not sleep_time:
                    if operateName == 'save_screenshot':
                        driver.save_screenshot("../%s.png" % str(module_name))
                    else:
                        try:
                            exec(("driver.find_element(By.%s, '%s').%s(%s)" % (
                                by_func, by_value, action, input_value)).replace('None', ''))
                        except InvalidSelectorException:
                            raise InvalidSelectorException("%s元素路径格式不正确" % step[2])
                        except NoSuchElementException:
                            raise NoSuchElementException("无法定位到元素%s" % step[2])
                else:
                    sleep(sleep_time)


class page_module_edit:
    def __init__(self):
        self.new_module_id = None
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 添加模块方法，需要接收模块名、元素id、操作类型、携带信息、操作步骤
    # 同时修改page_module表和page_module_detail表
    def add_module(self, module_name):
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        new_page_module = Page_module(module_name=module_name, created_at=self.now, updated_at=self.now)
        session.add(new_page_module)
        session.flush()  # 此时能通过new_page_module获取到刚新增数据的id了
        self.new_module_id = new_page_module.id
        session.commit()
        session.close()
        conn.close()

    def add_module_detail(self, element_id, operate_type, pause_time, send_msg, operate_step):
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        new_page_module_detail = Page_module_detail(page_module_id=self.new_module_id, element_id=element_id,
                                                    operate_type=operate_type, pause_time=pause_time,
                                                    send_msg=send_msg, operate_step=operate_step, created_at=self.now,
                                                    updated_at=self.now)
        session.add(new_page_module_detail)
        session.commit()
        session.close()
        conn.close()


@celery_app.task(name='page_module/execute_module_func')
def execute_module_func(module_name):
    try:
        ch_options = Options()
        ch_options.add_argument("--headless")  # 设置为headless模式
        driver = webdriver.Chrome(chrome_options=ch_options)
        driver.get('http://df.zhiyitech.cn/login')
        module = execute_module(driver)
        module.execute_selenium(module_name)
        driver.quit()
        return dict(success=True, message='执行成功')
    except ValueError as e:
        return dict(success=False, message=e.args[0])
    except InvalidSelectorException as e:
        return dict(success=False, message=e.msg)
    except NoSuchElementException as e:
        return dict(success=False, message=e.msg)


# 执行指定的模块
@page_module.route('/execute_wait/', methods=['POST'])
@token_check
def execute_wait():
    module_name = request.json['module_name']
    results = execute_module_func.delay(module_name)
    return dict(sessionId=results.id)


# 获取模块执行结果
@page_module.route('/execute_result/', methods=['POST'])
@token_check
def execute_result():
    resultId = request.json['resultId']
    async_result = AsyncResult(id=resultId, app=celery_app)
    if async_result.state == 'PENDING':
        # 任务还没开始
        response = {
            'state': async_result.state,
            'status': '排队中...'
        }
    elif async_result.state != 'FAILURE':
        response = async_result.info
    else:
        # 如果不是PENDING，或者SUCCESS，那么可能是出现异常了
        response = {
            'state': async_result.state,
            'status': str(async_result.info),  # 返回错误信息
        }
    return jsonify(response)


# 向数据库添加模块内容和详情
@page_module.route('/add_module/', methods=['POST'])
@token_check
def add_module():
    try:
        # module_name, element_id, operate_type, send_msg, operate_step
        module = page_module_edit()
        module_name = request.json['module_name']
        module.add_module(module_name)  # 先添加page_module表数据
        for index in request.json['module_ele']:
            ele_id = index['element_id']
            op_type = index['operate_type']
            pause_time = index['pause_time']
            send_msg = index['send_msg']
            operate_step = index['operate_step']
            module.add_module_detail(ele_id, op_type, pause_time, send_msg, operate_step)  # 再循环遍历添加所有的detail数据
        return dict(success=True, message='添加模块成功')
    except:
        return dict(success=False, message='添加失败')


if __name__ == '__main__':
    # pass
    ch_options = Options()
    ch_options.add_argument("--headless")  # 设置为headless模式
    drivers = webdriver.Chrome(chrome_options=ch_options)
    drivers.implicitly_wait(30)
    drivers.get('http://df.zhiyitech.cn')
    test = execute_module(drivers)
    test.execute_selenium()
