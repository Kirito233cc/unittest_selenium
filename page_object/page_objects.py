"""
使用sqlalchemy替代pymysql，将数据表对象化（ORM）
同时sqlalchemy支持数据库连接池，可以减少每次调用连接关闭数据库所产生的开销
"""
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from data_object.table_element import Element
from sqlalchemy import create_engine
from flask import Blueprint, request
import configparser
from settings import Config
from user.user import token_check

page_object = Blueprint('page_object', __name__)


class page_objects:
    def __init__(self):
        """"""

    @staticmethod
    def get_element_address(element_name):
        """从数据库中获取对应名字的元素信息"""
        conn = Config.engine.connect()
        # 创建DBSession类型
        DBSession = sessionmaker(bind=conn)
        # 创建session对象
        session = DBSession()
        # 创建Eelement对象
        element = session.query(Element).filter(Element.element_name == element_name).one()
        # 关闭连接
        session.close()
        conn.close()
        return element.element_address

    @staticmethod
    def add_element(element_name, element_type, element_address):
        """添加元素信息到数据库"""
        # 获取当前时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 建立连接
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        element = Element(element_name=element_name,
                          element_type=element_type,
                          element_address=element_address,
                          created_at=now,
                          updated_at=now)
        session.add(element)
        session.commit()
        session.close()
        conn.close()


# 向数据库添加页面元素
@page_object.route('/add_element/', methods=['POST'])
@token_check
def add_elements():
    page = page_objects()
    # element_name, element_type, element_address
    for index in request.json['elements']:
        ele_name = index['element_name']
        ele_type = index['element_type']
        ele_addr = index['element_address']
        page.add_element(ele_name, ele_type, ele_addr)
    return dict(success=True, message='添加成功')


if __name__ == '__main__':
    testPo = page_objects()
    # testPo.add_element('login_code', 1, 'codeInput')
    ts = testPo.get_element_address('login_confirm')
    print(ts)
