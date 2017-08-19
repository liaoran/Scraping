# -*- coding:utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

x = 0 #图片数
def crawl(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    req = urllib2.Request(url,headers=headers) #创建对象，发送请求
    page = urllib2.urlopen(req,timeout=20) #打开网站，设置超时
    contents = page.read() #获取源码

    soup = BeautifulSoup(contents,'html.parser') #创建一个soup对象，解析网页
    my_girl = soup.find_all('img') #找到img标签
    for girl in my_girl:
        link = girl.get('src') #获取src
        print link
        global x
        urllib.urlretrieve(link,'mvimg/%s.jpg' % x) #下载
        x += 1
        print "正在下载第%s张" % x

#多页
for page in range(1,2):
    page += 1
    url = 'http://www.dbmeinv.com/?pager_offset=%s' % page
    crawl(url)

print "报告长官：图片下载完毕！"

