from page_module.page_module import page_module
from page_object.page_objects import page_object
from user.user import user_api
from celery_thing.celeryapp import app


# app.config.from_object('./config/settings.Config')

# 蓝图注册各功能模块
app.register_blueprint(page_module, url_prefix='/page_module')
app.register_blueprint(page_object, url_prefix='/page_object')
app.register_blueprint(user_api, url_prefix='/user_api')


# @app.errorhandler(Exception)
# def error_all(error):
#     response = dict(status=0, message='系统繁忙～')
#     return jsonify(response), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
