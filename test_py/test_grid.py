from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep


driver = webdriver.Remote(command_executor='http://10.1.101.151:4444', desired_capabilities=DesiredCapabilities.CHROME)
driver.get('htts://www.baidu.com')
driver.quit()