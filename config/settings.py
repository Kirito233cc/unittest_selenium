import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_object.table_element import Element
"""
数据库连接以及redis连接相关设置
"""


class Config:
    m_host = "localhost"
    m_port = "3306"
    m_user = "root"
    m_pwd = "Xx7732088"
    m_db_name = "df_page_object"
    engine = create_engine(
        'mysql+pymysql://%s:%s@%s:%s/%s' % (m_user, m_pwd, m_host, m_port, m_db_name))


class link_redis:
    @staticmethod
    def link_redis():
        r_host = 'localhost'
        r_port = '6379'
        r_db = '0'
        return redis.StrictRedis(r_host, int(r_port), int(r_db))


if __name__ == '__main__':
    r = Config.engine
    DBSession = sessionmaker(bind=r.connect())
    session = DBSession()
    print(session.query(Element).all())