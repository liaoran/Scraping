#-*- coding:utf-8-*-
__author__ = 'kongnian'

import urllib,re
from bs4 import BeautifulSoup


#x = 0
# 打开网址，获取源码
def getHtml():
    page = urllib.urlopen('http://www.wmpic.me/meinv')
    html = page.read()
    #soup = BeautifulSoup(html,'html.parser')
    #my_girl = soup.find_all('img')
    #for girl in my_girl:
    #    link = girl.get('src')
    #    print link
    #    global x
    #    urllib.urlretrieve(link,'mvimg/%s.jpg' % x)
    #    x += 1
    #    print '正在下载第%s张图片' % x

    return html


# 匹配图片
x = 0 # 默认的图片名称，第一张为0.jpg


def getImg(html):
    imgre = re.compile(r' src="(.*?)" class=')
    imglist = re.findall(imgre,html)
    for imgurl in imglist:
        global x
        urllib.urlretrieve(imgurl, 'mvimg/%s.jpg' % x)  # 下载
        x += 1
        print '正在下载第%s张图片' % x


for page in range(1,5):
    page += 1
    html = getHtml()
    getImg(html)