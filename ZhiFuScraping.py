# -*- coding:utf-8 -*-
import urllib2
import re
import requests
import HTMLParser #解析网页
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #输出内容的编码

#获取主页源码
def getHtml(url):
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    request = urllib2.Request(url,headers=header) #用地址创建一个对象
    response = urllib2.urlopen(request) #打开网址
    text = response.read() #获取所有源码
    return text

#解析每条日报的链接
def getUrls(html):
    pattern = re.compile('<a href="/story/(.*?)"',re.S) #re.S是匹配换行符
    items = re.findall(pattern,html)
    urls = []
    for item in items:
        urls.append('http://daily.zhihu.com/story/' + item)
        #print urls[-1]
    return urls

#获取日报标题
def getContent(url):
    html = getHtml(url)
    pattern =re.compile('<h1 class="headline-title">(.*?)</h1>')
    items = re.findall(pattern,html)
    print '********************' + items[0] + '****************'

    #获取日报内容
    pattern = re.compile('<div class="content">\\n<p>(.*?)</div>',re.S)
    items_withtag = re.findall(pattern,html)
    for item in items_withtag:
        for content in characterProcessing(item):
            print content

#去掉文章内容的标签
def characterProcessing(html):
    htmlPaeser = HTMLParser.HTMLParser()
    pattern = re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?',re.S)
    items = re.findall(pattern,html)
    result = []
    for index in items:
        if index != '':
            for content in index:
                tag = re.search('<.*?>',content)
                http = re.search('<.*?http.*?>',content)
                html_tag = re.search('&',content)
                if html_tag:
                    content = htmlPaeser.unescape(content)
                if http:
                    continue
                elif tag:
                    pattern = re.compile('(.*?)<.*?>(.*?)</.*?>(.*?)')
                    items = re.findall(pattern,content)
                    content_tags = ''
                    if len(items) > 0:
                        for item in items:
                            if len(item) > 0:
                                for item_s in item:
                                    content_tags = content_tags + item_s
                            else:
                                content_tags = content_tags + item_s
                        content_tags =re.sub('<.*?>','',content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result

#主函数
def main():
    url = 'http://daily.zhihu.com/'
    html = getHtml(url)
    urls = getUrls(html)
    for url in urls: #超链接
        try:
            getContent(url) #调用超链接
        except Exception,e:
            print e

if __name__ == "__main__":
    main()



