from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


ch_options = Options()
ch_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=ch_options)
driver.set_window_size(1920, 1080)
driver.get('http://df.zhiyitech.cn')
sleep(2)
driver.save_screenshot('./ch.png')

driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[1]/span/input').send_keys('18958048696')
sleep(2)
driver.save_screenshot('./ch_1.png')
driver.find_element(By.XPATH, '//*[@id="codeInput"]').send_keys('123123')
sleep(2)
driver.save_screenshot('./ch_2.png')
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/button/span').click()
sleep(15)
driver.save_screenshot('./ch_3.png')

driver.quit()