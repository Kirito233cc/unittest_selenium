import redis
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class link:
    @staticmethod
    def link_redis():
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        r_host = config['redis']['host']
        r_port = config['redis']['port']
        r_db = config['redis']['db']
        return redis.StrictRedis(r_host, r_port, r_db)

    @staticmethod
    def link_mysql():
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        m_host = config['database']['host']
        m_port = config['database']['port']
        m_user = config['database']['user']
        m_pwd = config['database']['passwd']
        m_db_name = config['database']['databaseName']
        engine = create_engine(
            'mysql+pymysql://%s:%s@%s:%s/%s' % (m_user, m_pwd, m_host, m_port, m_db_name))
        return engine.connect()


if __name__ == '__main__':
    r = link.link_redis()
    s = link.link_mysql()
    print(r)
    print(s)