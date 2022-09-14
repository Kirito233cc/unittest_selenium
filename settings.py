import redis
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_object.table_element import Element
"""
数据库连接以及redis连接相关设置
"""


class Config:
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    m_host = config['database']['host']
    m_port = config['database']['port']
    m_user = config['database']['user']
    m_pwd = config['database']['passwd']
    m_db_name = config['database']['databaseName']
    engine = create_engine(
        'mysql+pymysql://%s:%s@%s:%s/%s' % (m_user, m_pwd, m_host, m_port, m_db_name))


class link_redis:
    @staticmethod
    def link_redis():
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        r_host = config['redis']['host']
        r_port = config['redis']['port']
        r_db = config['redis']['db']
        return redis.StrictRedis(r_host, int(r_port), int(r_db))


if __name__ == '__main__':
    r = Config.engine
    DBSession = sessionmaker(bind=r.connect())
    session = DBSession()
    print(session.query(Element).all())