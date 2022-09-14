"""
使用sqlalchemy替代pymysql，将数据表对象化（ORM）
同时sqlalchemy支持数据库连接池，可以减少每次调用连接关闭数据库所产生的开销
"""
import configparser

from selenium import webdriver

from selenium.webdriver.common.by import By

from datetime import datetime

from time import sleep

from flask import Blueprint, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_object.table_element import Element
from data_object.table_element_locate import Element_locate
from data_object.table_element_operate import Element_operate
from data_object.table_page_module import Page_module
from data_object.table_page_module_detail import Page_module_detail

from settings import Config
from user.user import token_check

# 进行蓝图注册
page_module = Blueprint('page_module', __name__)


class execute_module:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(30)

    @staticmethod
    def execute_selenium(self, module_name='login'):
        """根据模块名字执行对应的selenium"""
        conn = Config.engine.connect()
        # 创建DBSession类型
        DBSession = sessionmaker(bind=conn)
        # 创建session对象
        session = DBSession()
        # 创建Eelement对象,多表关联查询出结果
        elements = session.query(Page_module.module_name,
                                 Page_module_detail.operate_step,
                                 Element.element_name,
                                 Element_locate.element_locate_name,
                                 Element.element_address,
                                 Element_operate.operate_name,
                                 Page_module_detail.send_msg). \
            select_from(Page_module). \
            join(Page_module_detail, Page_module.id == Page_module_detail.page_module_id). \
            join(Element, Page_module_detail.element_id == Element.id). \
            join(Element_operate, Page_module_detail.operate_type == Element_operate.operate_type). \
            join(Element_locate, Element.element_type == Element_locate.element_type). \
            filter(Page_module.module_name == module_name).order_by(Page_module_detail.operate_step).all()
        # 关闭连接
        session.close()
        conn.close()
        # 逐个执行selenium操作
        for step in elements:
            sleep(0.5)
            # 元素搜索方法
            by_func = step[3]
            # 元素搜索的值
            by_value = step[4]
            # 元素操作
            action = step[-2]
            # 元素操作传的值
            input_value = step[-1]
            exec(("self.driver.find_element(By.%s, '%s').%s(%s)" % (by_func, by_value, action, input_value)). \
                 replace('None', ''))


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

    def add_module_detail(self, element_id, operate_type, send_msg, operate_step):
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        new_page_module_detail = Page_module_detail(page_module_id=self.new_module_id, element_id=element_id,
                                                    operate_type=operate_type,
                                                    send_msg=send_msg, operate_step=operate_step, created_at=self.now,
                                                    updated_at=self.now)
        session.add(new_page_module_detail)
        session.commit()
        session.close()
        conn.close()


# 执行指定的模块
@page_module.route('/execute_module/', methods=['POST'])
@token_check
def execute_module_func():
    try:
        driver = webdriver.Chrome()
        driver.get('http://df.zhiyitech.cn/login')
        module = execute_module(driver)
        module.execute_selenium(request.json['module_name'])
        driver.quit()
        return dict(success=True, message='执行成功')
    except:
        return dict(success=False, message='运行失败')


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
            send_msg = index['send_msg']
            operate_step = index['operate_step']
            module.add_module_detail(ele_id, op_type, send_msg, operate_step)  # 再循环遍历添加所有的detail数据
        return dict(success=True, message='添加模块成功')
    except:
        return dict(success=False, message='添加失败')


if __name__ == '__main__':
    pass
    # drivers = webdriver.Chrome()
    # drivers.implicitly_wait(30)
    # drivers.get('http://df.zhiyitech.cn')
    # test = execute_module(drivers)
    # test.execute_selenium()
    # test = page_module_edit()
    # test.add_module('left_menu', 4, 0, '', 1)
