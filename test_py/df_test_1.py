# Generated by Selenium IDE
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep


class TestDfTest1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('whitelisted-ips')
        driver = webdriver.Remote(command_executor='http://10.1.101.151:4444',
                                  desired_capabilities=DesiredCapabilities.CHROME)
        # driver = webdriver.Remote('http://10.1.101.130:9515')
        # driver = webdriver.Chrome()
        # 设置隐式等待30s
        # driver.implicitly_wait(30)
        cls.driver = driver

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_menu(self):
        try:
            driver = self.driver
            """测试左侧页面点击"""
            driver.get("http://df.zhiyitech.cn/login")
            driver.set_window_size(1440, 875)
            # 调用登陆模块
            sleep(0.5)
            driver.find_element(By.XPATH, "//*[@id='root-master']/div/div[2]/div/div[2]/div[1]/span/input").send_keys('18958048696')
            sleep(0.5)
            driver.find_element(By.ID, "//*[@id='codeInput']").send_keys("123123")
            sleep(0.5)
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]").click()
        except:
            self.driver.quit()
        # 点击左侧列表菜单
        # driver.find_element(By.XPATH, "//span[contains(.,\'抖音选款\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'小红书推荐\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'灵感集\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'小红书达人\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'淘系商品\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'抖音小店\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'商品企划\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'设计任务\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'样衣库\')]").click()
        # driver.find_element(By.XPATH, "//span[contains(.,\'出入库记录\')]").click()


if __name__ == '__main__':
    unittest.main()
