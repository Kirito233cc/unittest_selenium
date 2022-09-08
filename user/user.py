import configparser
import json
import uuid
from datetime import datetime

import redis
from flask import Blueprint, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from data_object.table_user import User

user_api = Blueprint('user_api', __name__)


class user:
    def __init__(self):
        """
        从/config/config.ini中获取redis、数据库连接信息
        """
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        self.r_host = config['redis']['host']
        self.r_port = config['redis']['port']
        self.r_db = config['redis']['db']
        self.m_host = config['database']['host']
        self.m_port = config['database']['port']
        self.m_user = config['database']['user']
        self.m_pwd = config['database']['passwd']
        self.m_db_name = config['database']['databaseName']
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_login(self, user_name, user_pwd):
        """
        先在redis中校验用户名和密码，若通过则赋予token；若redis中没有则连接数据库查询，若有则添加数据到redis
        :param user_name: 用户名
        :param user_pwd: 密码
        :return: 返回json串提示登录校验结果及token
        """
        r = redis.StrictRedis(self.r_host, self.r_port, self.r_db)  # 建立redis连接
        if r.get(user_name):
            r_content = json.loads(r.get(user_name).decode('utf-8'))
            if r_content['pwd'] == user_pwd:
                token = uuid.uuid4().hex
                r_content['token'] = token  # 校验密码成功赋予token
                r.set(user_name, json.dumps(r_content))
                return dict(success=True, message='登陆成功', token=token)
            else:
                return dict(success=False, message='用户名或密码错误')
        else:
            engine = create_engine(
                'mysql+pymysql://%s:%s@%s:%s/%s' % (self.m_user, self.m_pwd, self.m_host, self.m_port, self.m_db_name))
            conn = engine.connect()
            DBSession = sessionmaker(bind=conn)
            session = DBSession()
            try:
                db_user_pwd = session.query(User).filter(User.user_name == user_name).one().user_pwd
                if db_user_pwd == user_pwd:
                    token = uuid.uuid4().hex
                    r_content = dict(pwd=user_pwd, token=token)
                    r.set(user_name, json.dumps(r_content))
                    return dict(success=True, message='登陆成功', token=token)
                else:
                    return dict(success=False, message='用户名或密码错误')
            except NoResultFound:  # 捕获上方因为在数据库中查询不到结果产生的异常
                return dict(success=False, message='该用户尚未注册')
            coon.dispose()
        r.shutdown()  # 关闭连接

    def sign_up(self, user_name, user_pwd):
        """
        注册
        :param user_name:新用户的用户名
        :param user_pwd: 新用户的密码
        :return: 返回json串提示登录校验结果及token
        """
        r = redis.StrictRedis(self.r_host, self.r_port, self.r_db)  # 建立redis连接
        engine = create_engine(
            'mysql+pymysql://%s:%s@%s:%s/%s' % (self.m_user, self.m_pwd, self.m_host, self.m_port, self.m_db_name))  # 建立数据库连接
        conn = engine.connect()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        try:
            session.query(User).filter(User.user_name == user_name).one()
            return dict(success=False, message='该用户已注册')
        except NoResultFound:
            new_user = User(user_name=user_name, user_pwd=user_pwd, created_at=self.now, updated_at=self.now)
            session.add(new_user)
            session.commit()
            token = uuid.uuid4().hex
            r_content = dict(pwd=user_pwd, token=token)
            r.set(user_name, json.dumps(r_content))
            return dict(success=True, message='注册成功', token=token)
        r.shutdown()
        session.close()
        conn.dispose()


@user_api.route('/login/', methods=['POST'])
def user_login():
    user_name = request.json['user_name']
    user_pwd = request.json['user_pwd']
    current_user = user()
    return current_user.check_login(user_name, user_pwd)


@user_api.route('/sign_up/', methods=['POST'])
def user_sign_up():
    user_name = request.json['user_name']
    user_pwd = request.json['user_pwd']
    new_user = user()
    msg = new_user.sign_up(user_name, user_pwd)
    return msg


if __name__ == '__main__':
    test_user = user()
    print(test_user.check_login('xushengchao', '123456'))
