# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import urllib2
import re
from bs4 import BeautifulSoup
import time
import socket


fanly_url = 'http://zhide.fanli.com/p' #多页
format_url = 'http://zhide.fanli.com/detail/1-' #商品链接

class Faly():
    def __init__(self): #初始化构造函数
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' #用户代理
        self.html_data = [] #放置商品信息列表

    # 获取主页的源码,多页
    def get_html(self,start_page = 1,end_page = 5):
        for i in range(start_page,end_page + 1):
            rt = urllib2.Request(fanly_url + str(i)) #用地址创建一个对象
            rt.add_header('User-Agent',self.user_agent)
            try:
                my_data = urllib2.urlopen(rt).read() #打开网页，获取源码
                self.html_data.append(my_data)
                time.sleep(2) #停顿时间
                socket.setdefaulttimeout(15) #设置超时等待时间,超出时间停止下载
            except urllib2.URLError,e:
                if hasattr(e,'reason'):
                    print u'连接失败',e.reason
        return str(self.html_data)

class GetData():
    def __init__(self):
        self.html = Faly().get_html() #获取源码
        self.href = [] #放6位数字的列表
        self.ls = []
        self.url = []

    # 获取产品的超链接
    def get_hrefUrl(self):
        reg = r'data-id="\d{6}' #商品6位数字正则
        result = re.compile(reg)
        tag = re.findall(result,self.html)
        #tag = result.findall(self.html) #与上一行代码作用相同
        for i in tag:
            self.href.append(i)
        #去重
        reg2 = r"\d{6}"
        result2 = re.findall(reg2,str(self.href))
        if len(result2):
            for data in result2:
                if data not in self.ls:
                    self.ls.append(data)
                    url = format_url + str(data) #完整的商品链接
                    self.url.append(url)
        return self.url
#a = GetData().get_hrefUrl()
#获取产品信息
class Href_mg():
    def __init__(self):
        self.list = GetData().get_hrefUrl() #超链接
        self.txt_list = [] #放置商品信息列表
    def show_mg(self):
        for item in range(len(self.list)):
            if len(self.list):
                url = str(self.list[item])
                mg = urllib2.Request(url)
                try:
                    req = urllib2.urlopen(mg).read()
                    soup = BeautifulSoup(req,'html.parser')
                    txt = soup.find_all('h1')
                    self.txt_list.append(txt)
                    #print self.txt_list[-1] #打印商品列表
                except urllib2.URLError,e:
                    print e.reason
        return str(self.txt_list).decode("unicode_escape")

if __name__ == '__main__':
    path = "shangpin.txt"
    with open(path,'a') as file:
        data = Href_mg().show_mg() #获取产品的内容
        reg4 = r'<.*?>'
        data_s = re.sub(reg4,' ',data).replace('全网最低','').replace('[','').replace(']','').replace(',','\n').strip().replace('  ','')
        #data_s = re.sub('[\[,\],\,, ]','',data)
        file.write(str(data_s))