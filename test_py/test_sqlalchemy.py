import configparser
import json
import uuid

import redis
from flask import Blueprint, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_object.table_user import User

config = configparser.ConfigParser()
config.read('../config/config.ini')
m_host = config['database']['host']
m_port = config['database']['port']
m_user = config['database']['user']
m_pwd = config['database']['passwd']
m_db_name = config['database']['databaseName']

engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' % (m_user, m_pwd, m_host, m_port, m_db_name))
conn = engine.connect()
DBSession = sessionmaker(bind=conn)
session = DBSession()
print(session.query(User).filter(User.user_name == "xushengchao").one())