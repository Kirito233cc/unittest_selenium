"""
使用sqlalchemy替代pymysql，将数据表对象化（ORM）
同时sqlalchemy支持数据库连接池，可以减少每次调用连接关闭数据库所产生的开销
"""
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from data_object.table_element import Element
from flask import Blueprint, request
from config.settings import Config
from user.user import token_check

page_object = Blueprint('page_object', __name__)


class page_objects:
    def __init__(self):
        """"""

    # @staticmethod
    # def get_element_address(element_name):
    #     """从数据库中获取对应名字的元素信息"""
    #     conn = Config.engine.connect()
    #     # 创建DBSession类型
    #     DBSession = sessionmaker(bind=conn)
    #     # 创建session对象
    #     session = DBSession()
    #     # 创建Eelement对象
    #     element = session.query(Element).filter(Element.element_name == element_name).one()
    #     # 关闭连接
    #     session.close()
    #     conn.close()
    #     return element.element_address

    @staticmethod
    def add_element(element_name, element_type, element_address):
        """添加元素信息到数据库"""
        # 获取当前时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 建立连接
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        element = Element(element_name=element_name, element_type=element_type, element_address=element_address, created_at=now, updated_at=now)
        session.add(element)
        session.commit()
        session.close()
        conn.close()

    @staticmethod
    def del_element(element_id):
        """删除对应id的元素"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        session.query(Element).filter(Element.id == element_id).update({Element.deleted_at: now, Element.updated_at: now})
        session.commit()
        session.close()
        conn.close()

    @staticmethod
    def update_element(element_id, element_name, element_type, element_address):
        """更新元素信息"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        result = session.query(Element).filter(Element.id == element_id).update({Element.element_name: element_name, Element.element_type: element_type, Element.element_address: element_address, Element.updated_at: now})
        session.commit()
        session.close()
        conn.close()
        return result

    @staticmethod
    def page_element(page):
        """获取元素分页信息"""
        conn = Config.engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        page_content = session.query(Element).order_by(Element.id.desc()).paginate(page, per_page=20)
        return page_content


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


# 删除元素
@page_object.route('/delete_element/', methods=['POST'])
@token_check
def del_elements():
    page = page_objects
    for index in request.json['elements']:
        element_id = index['id']
        page.del_element(element_id)
    return dict(success=True, message='删除成功')


# 更新元素
@page_object.route('/update_element/', methods=['POST'])
@token_check
def update_elements():
    """可以同时更新多个，其中部分元素数据错误不影响其他正常数据更新"""
    page = page_objects
    fail_elements = []
    for index in request.json['elements']:
        element_id = index['id']
        ele_name = index['element_name']
        ele_type = index['element_type']
        ele_addr = index['element_address']
        if page.update_element(element_id, ele_name, ele_type, ele_addr):
            pass
        else:
            fail_elements.append({"element_id": element_id, "element_name": ele_name})
    if fail_elements:
        message = ''
        for fail_index in fail_elements:
            message += (fail_index['element_name'] + ' ')
        message += '更新失败'
        return dict(success=False, message=message, fail_elements=fail_elements)
    else:
        return dict(success=True, message='更新成功')


# 查询元素列表
@page_object.route('/element/page', methods=['GET'])
@token_check
def elements_page():
    """待完工……"""
    page = page_objects
    page_index = request.args.get('page', default=1, type=int)
    return dict(success=True, result=page.page_element(page_index))


if __name__ == '__main__':
    # testPo = page_objects()
    # testPo.add_element('login_code', 1, 'codeInput')
    # ts = testPo.get_element_address('login_confirm')
    # print(ts)
    conn = Config.engine.connect()
    DBSession = sessionmaker(bind=conn)
    session = DBSession()
    print(session.query(Element).filter(Element.id == 1).update(
        {Element.element_name: 'test', Element.element_type: 0,
         Element.element_address: 'test'}))