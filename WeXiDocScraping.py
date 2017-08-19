#-*- coding:utf-8-*-
__author__ = 'kongnian'

from selenium import webdriver
import time
import json
import requests

driver = webdriver.Firefox()
driver.get('https://mp.weixin.qq.com')
driver.find_element_by_xpath('//*[@id="account"]').clear()
driver.find_element_by_xpath('//*[@id="account"]').send_keys('982247830@qq.com')
time.sleep(2)
driver.find_elements_by_xpath('//*[@id="pwd"]').clear()
driver.find_elements_by_xpath('//*[@id="pwd"]').send_keys('guang2566')
time.sleep(2)
driver.find_elements_by_xpath('//*[@id="loginForm"]/div[3]/label').click()
time.sleep(2)
driver.find_elements_by_xpath('//*[@id="loginBt"]').click()
time.sleep(15)

cookies = driver.get_cookies()
cookie = {}
for items in cookies:
    cookie[items.get('name')] = items.get('value')

with open('cookies.txt','wb') as file:
    file.write(json.dumps(cookie))

driver.close()

with open('cookie.txt','r') as file:
    cookie = file.read()

cookies = json.loads(cookie)