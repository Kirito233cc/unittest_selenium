from page_module.page_module import page_module
from page_object.page_objects import page_object
from flask import Flask, jsonify

app = Flask(__name__)

# 蓝图注册各功能模块
app.register_blueprint(page_module, url_prefix='/page_module')
app.register_blueprint(page_object, url_prefix='/page_object')


@app.errorhandler(Exception)
def error_all(error):
    response = dict(status=0, message='系统繁忙～')
    return jsonify(response), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
