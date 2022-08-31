"""
使用sqlalchemy替代pymysql，将数据表对象化（ORM）
同时sqlalchemy支持数据库连接池，可以减少每次调用连接关闭数据库所产生的开销
"""
import configparser

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_object.table_element import Element
from data_object.table_element_locate import Element_locate
from data_object.table_element_operate import Element_operate
from data_object.table_page_module import Page_module
from data_object.table_page_module_detail import Page_module_detail


class module_demo:
    def __init__(self, driver):
        self.driver = driver
        """从config.ini提取数据库信息并初始化数据库连接"""
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        user = config['database']['user']
        passwd = config['database']['passwd']
        host = config['database']['host']
        port = config['database']['port']
        databaseName = config['database']['databaseName']
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (user, passwd, host, port, databaseName))

    def execute_module(self, module_name='login'):
        """根据模块名字执行对应的selenium"""
        conn = self.engine.connect()
        # 创建DBSession类型
        DBSession = sessionmaker(bind=conn)
        # 创建session对象
        session = DBSession()
        # 创建Eelement对象
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
            sleep(2)
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
            # print(("self.driver.find_element(By.%s, '%s').%s(%s)" % (by_func, by_value, action, input_value)). \
            # replace('None', ''))
            # self.driver.find_element(By.XPATH, data).send_keys(userPhone)
            # self.driver.find_element(By.ID, "codeInput").send_keys(password)


if __name__ == '__main__':
    drivers = webdriver.Chrome()
    drivers.get('http://df.zhiyitech.cn')
    test = module_demo(drivers)
    test.execute_module()
