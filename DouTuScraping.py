# -*- coding:utf-8 -*-
import requests
import threading
from bs4 import BeautifulSoup
from lxml import etree
import time


# 获取主页源码
def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    request = requests.get(url=url, headers=headers)  # 发送get请求
    response = request.content  # 获取网页内容
    return response


# 匹配内页的url
def get_img_html(html):
    soup = BeautifulSoup(html, 'lxml')  # 解析网页
    all_a = soup.find_all('a', class_='list-group-item')  # 找到a标签
    for i in all_a:
        img_html = get_html(i['href'])  # 获取超链接的网页内容
        get_img(img_html)
        #print img_html  # 网页源码


# 获取每张图片的url
def get_img(html):
    soup = etree.HTML(html)  # 初始化源码
    items = soup.xpath('//div[@class="artile_des"]')  # 找这个盒子下面的内容
    for item in items:
        imgurl_list = item.xpath('table/tbody/tr/td/a/img/@onerror')  # 选取属性
        start_save_img(imgurl_list)


# 下载图片
def save_img(img_url):
    img_url = img_url.split('=')[-1][1:-2].replace('jp', 'jpg')  # 分割
    print u"正在下载" + 'http:' + img_url
    img_content = requests.get('http:' + img_url).content
    with open('doutu/%s' % img_url.split('/')[-1], 'wb') as f:
        f.write(img_content)


# 下载图片,另一种方式
#x = 1
#def save_img(img_url):
    #global x
    #x += 1
    #img_url = img_url.split('=')[-1][1:-2].replace('jp','jpg')
    #print u"正在下载" + 'http:' + img_url
    #img_content = requests.get('http:' + img_url).content
    #with open('doutu/%s.jpg' % x,'wb') as f:
        #f.write(img_content)


def start_save_img(imgurl_list):
    for i in imgurl_list:
        print i
        th = threading.Thread(target=save_img, args=(i,))
        th.start()


# 多页源码
def main():
    start_url = 'https://www.doutula.com/article/list/?page='
    time.sleep(10)
    for i in range(1, 10):
        start_html = get_html(start_url.format(i))
        get_img_html(start_html)


if __name__ == '__main__':
    main()