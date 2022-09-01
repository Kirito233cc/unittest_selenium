from selenium import webdriver
from page_object.page_object import page_object
from page_module.page_module import execute_module, page_module
from flask import Flask, request

app = Flask(__name__)


# 执行指定的模块
@app.route('/page_module/execute_module/', methods=['POST'])
def execute_module():
    driver = webdriver.Chrome()
    driver.get('http://df.zhiyitech.cn/login')
    module = execute_module(driver)
    module.execute_selenium(request.json['module_name'])
    driver.quit()
    return 'success'


# 向数据库添加页面元素
@app.route('/page_object/add_element/', methods=['POST'])
def add_elements():
    page = page_object()
    # element_name, element_type, element_address
    for index in request.json['elements']:
        ele_name = index['element_name']
        ele_type = index['element_type']
        ele_addr = index['element_address']
        page.add_element(ele_name, ele_type, ele_addr)
    return 'SUCCESS'


# 向数据库添加模块内容和详情
@app.route('/page_module/add_module/', methods=['POST'])
def add_module():
    # module_name, element_id, operate_type, send_msg, operate_step
    module = page_module()
    module_name = request.json['module_name']
    module.add_module(module_name)  # 先添加page_module表数据
    for index in request.json['module_ele']:
        ele_id = index['element_id']
        op_type = index['operate_type']
        send_msg = index['send_msg']
        operate_step = index['operate_step']
        module.add_module_detail(ele_id, op_type, send_msg, operate_step)  # 再循环遍历添加所有的detail数据
    return 'SUCCESS'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
