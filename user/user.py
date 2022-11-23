import json
import uuid
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from data_object.table_user import User
from functools import wraps

from config.settings import Config, link_redis


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
        r = link_redis.link_redis()  # 通过静态方法建立redis连接
        if r.get(user_name):
            r_content = json.loads(r.get(user_name).decode('utf-8'))
            if r_content['pwd'] == user_pwd:
                token = uuid.uuid4().hex
                origin_token = r_content['token']
                r.delete(origin_token)  # 删除原有的token
                r_content['token'] = token  # 校验密码成功赋予token
                r.set(user_name, json.dumps(r_content))  # 设置username：token/pwd键值对
                r.expire(user_name, 604800)  # 设置过期时间一周
                r.set(token, json.dumps(dict(user_name=user_name)))  # 设置token：username键值对
                r.expire(token, 604800)  # 设置过期时间一周
                return dict(success=True, message='登陆成功', token=token)
            else:
                return dict(success=False, message='用户名或密码错误')
        else:
            conn = Config.engine.connect()  # 通过静态方法建立mysql连接
            dbSession = sessionmaker(bind=conn)
            session = dbSession()
            try:
                db_user_pwd = session.query(User).filter(User.user_name == user_name).one().user_pwd
                if db_user_pwd == user_pwd:
                    token = uuid.uuid4().hex
                    r_content = dict(pwd=user_pwd, token=token)
                    r.set(user_name, json.dumps(r_content))
                    r.expire(user_name, 604800)
                    r.set(token, json.dumps(dict(user_name=user_name)))
                    r.expire(token, 604800)
                    return dict(success=True, message='登陆成功', token=token)
                else:
                    return dict(success=False, message='用户名或密码错误')
            except NoResultFound:  # 捕获上方因为在数据库中查询不到结果产生的异常
                return dict(success=False, message='该用户尚未注册')
            finally:
                conn.close()
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
        r = link_redis.link_redis()
        conn = Config.engine.connect()
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
            r_content_u2t = dict(pwd=user_pwd, token=token)
            r_content_t2u = dict(user_name=user_name)
            r.set(user_name, json.dumps(r_content_u2t))
            r.set(token, json.dumps(r_content_t2u))
            return dict(success=True, message='注册成功', token=token)
        finally:
            r.shutdown()
            session.close()
            conn.close()


def token_check(func):
    """
    校验token是否有效的装饰器
    在传入参数中获取token，若没有则抛出"验证失败，请重新登录"
    获取到token到redis中查找，若无匹配，则抛出"验证失败，请重新登录"
    匹配到token，正常执行函数
    :param func:
    :return:
    """
    @wraps(func)
    def wrap_token_check():
        try:
            header_token = request.headers.get('token')
            r = link_redis.link_redis()
            json.loads(r.get(header_token).decode('utf-8'))
            return func()
        except AttributeError as e:
            print(e)
            return dict(success=False, message='验证失败，请重新登陆')
    return wrap_token_check


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
