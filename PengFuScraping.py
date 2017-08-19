# -*- coding:utf-8 -*-
import urllib
import re


# 获取源码
def page(pg):
    url = 'https://www.pengfu.com/index_%s.html' % pg
    html = urllib.urlopen(url).read()  # 读取所有源代码
    return html


# 匹配标题
def title(html, pg):
    html = page(pg)
    reg = re.compile(r'<h1 class="dp-b"><a href=".*?" target="_blank">(.*?)</a>') #加括号是为了取下来，不加只是匹配
    item = re.findall(reg, html)
    return item


# 匹配图片
def content(html):
    reg = r'<img src="(.*?)" width='
    item = re.findall(reg, html)
    return item


# 下载
def download(url, name):
    path = 'img/%s.jpg' % name
    urllib.urlretrieve(url, path)

# 多页，标题对应图片
for i in range(1, 6):
    html = page(i)
    title_list = title(html, i)  # 图片名称
    content_list = content(html)  # 图片路径
    for i,z in zip(title_list, content_list):
        download(z, i)
        print i, z
