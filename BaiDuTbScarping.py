#-*- coding:utf-8-*-
__author__ = 'kongnian'

import urllib2,re

class BDTB:
    baseUrl = 'https://tieba.baidu.com/p/5253318343?see_lz=1'

    #def __init__(self,baseUrl,seeLZ):
    #    self.baseUrl = baseUrl
    #    self.seeLZ = '?see_lz=' + seeLZ

    # 获取网页源码
    def getPage(self):
        try:
            url = self.baseUrl
            req = urllib2.Request(url)
            res = urllib2.urlopen(req).read()
            return res
        except Exception,e:
            print e

    # 匹配标题
    def Title(self):
        html = self.getPage()  # 调用获取源码
        reg = re.compile(r'<h3 class="core_title_txt pull-left text-overflow  " title="(.*?)" style=')
        items = re.findall(reg,html)
        for item in items:
            f = open('text.txt','w')
            f.write('标题'+'\t'+item)
            f.close()
        return items

    # 匹配正文
    def Text(self):
        html = self.getPage()
        reg = re.compile(r'class="d_post_content j_d_post_content ">            (.*?)</div><br>',re.S)
        req = re.findall(reg,html)
        for i in req:
            removeAddr = re.compile('<a.*?>|</a>')
            removeImg = re.compile('<img.*?>')
            removeHttp = re.compile('http.*?.html')
            i = re.sub(removeAddr,"",i)
            i = re.sub(removeImg,"",i)
            i = re.sub(removeHttp,"",i)
            i = i.replace('<br>','')
            f = open('text.txt','a')
            f.write('\n\n' + i)
            f.close()







b = BDTB()
b.getPage()
b.Title()
b.Text()

