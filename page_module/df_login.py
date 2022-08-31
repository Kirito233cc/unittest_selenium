from selenium import webdriver
from selenium.webdriver.common.by import By
from page_object.dfElement import df_po
from time import sleep


class Df(df_po):
    def __init__(self, driver):
        self.df = df_po()
        self.driver = driver
        self.driver.implicitly_wait(30)

    def login(self, userPhone=18958048696, password=123123):
        """登陆"""
        sleep(1)
        data = self.df.getData("login_input")
        self.driver.find_element(By.XPATH, data).send_keys(userPhone)
        self.driver.find_element(By.ID, "codeInput").send_keys(password)
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/button").click()

    def leftMenu(self):
        """点击左侧菜单列"""



if __name__ == '__main__':
    drivers = webdriver.Chrome()
    drivers.get('http:df.zhiyitech.cn')
    testDf = Df(drivers)
    testDf.login()
