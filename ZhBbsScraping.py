# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

url = 'http://www.pythontab.com/html/pythonhexinbiancheng/index.html'
url_list = [url] #链接放入列表
for i in range(2,19):
    url_list.append('http://www.pythontab.com/html/pythonhexinbiancheng/%s.html' % i)
source_list = [] #放置标题和文字的空列表
for j in url_list:
    request = urllib2.urlopen(j)
    html = request.read() #获取源码
    soup = BeautifulSoup(html,'html.parser')
    titles = soup.select('#catlist > li > a') #查找文章标题
    links = soup.select('#catlist > li > a') #查找文章链接
    for title,link in zip(titles,links):
        data = {
            "title" : title.get_text(), #获取文章标题
            "link" : link.get('href') #获取文章链接
        }
        source_list.append(data)
    #获取文章内容
    for l in source_list:
        request = urllib2.urlopen(l['link'])
        html = request.read()
        soup = BeautifulSoup(html,'html.parser')
        text_p = soup.select('div.content > p')
        text = [] #放置文章的空列表
        for t in text_p:
            text.append(t.get_text().encode('utf-8'))
        title_txt = l['title'] #文章标题
        title_txt = title_txt.replace('*','').replace('/','or')
        with open('study/%s.txt' % title_txt, 'wb') as f:
            for a in text:
                f.write(a)