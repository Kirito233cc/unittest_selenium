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
from functools import wraps
from static_method.static import link


user_api = Blueprint('user_api', __name__)


class user:
    def __init__(self):
        """"""

    @staticmethod
    def check_login(user_name, user_pwd):
        """
        先在redis中校验用户名和密码，若通过则赋予token；若redis中没有则连接数据库查询，若有则添加数据到redis
        :param user_name: 用户名
        :param user_pwd: 密码
        :return: 返回json串提示登录校验结果及token
        """
        r = link.link_redis()  # 通过静态方法建立redis连接
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
            conn = link.link_mysql()  # 通过静态方法建立mysql连接
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

    @staticmethod
    def sign_up(user_name, user_pwd):
        """
        注册
        :param user_name:新用户的用户名
        :param user_pwd: 新用户的密码
        :return: 返回json串提示登录校验结果及token
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        r = link.link_redis()
        conn = link.link_mysql()
        DBSession = sessionmaker(bind=conn)
        session = DBSession()
        try:
            session.query(User).filter(User.user_name == user_name).one()
            return dict(success=False, message='该用户已注册')
        except NoResultFound:
            new_user = User(user_name=user_name, user_pwd=user_pwd, created_at=now, updated_at=now)
            session.add(new_user)
            session.commit()
            token = uuid.uuid4().hex
            r_content = dict(pwd=user_pwd, token=token)
            r.set(user_name, json.dumps(r_content))
            return dict(success=True, message='注册成功', token=token)
        r.shutdown()
        session.close()
        conn.dispose()


# def tokenCheck(func):
#     @wraps(func)
#     def wrapTokenCheck():
#         config = configparser.ConfigParser()
#         config.read('./config/config.ini')
#         r_host = config['redis']['host']
#         r_port = config['redis']['port']
#         r_db = config['redis']['db']
#         header_token = request.headers.get('token')
#         r = redis.StrictRedis(r_host, r_port, r_db)
#         r_content = json.loads(r.get().decode('utf-8'))
#         func()
#     return wrapTokenCheck


@user_api.route('/login/', methods=['POST'])
def user_login():
    user_name = request.json['user_name']
    user_pwd = request.json['user_pwd']
    return user.check_login(user_name, user_pwd)


@user_api.route('/sign_up/', methods=['POST'])
def user_sign_up():
    user_name = request.json['user_name']
    user_pwd = request.json['user_pwd']
    msg = user.sign_up(user_name, user_pwd)
    return msg


if __name__ == '__main__':
    test_user = user()
    print(test_user.check_login('xushengchao', '123456'))
