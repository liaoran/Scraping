# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class QSBK:
    def __init__(self): #构造函数，self指本身
        self.pageIndex = 1 #页数
        self.use_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.headers = {'User-Agent':self.use_agent}
        self.stories = [] #放置笑话的空列表
        self.enable = False #存放程序是否继续运行

    #获取源码
    def getPage(self,pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers) #提交请求
            response = urllib2.urlopen(request) #打开网址
            pageCode = response.read().decode('utf-8') #获取所有源码
            return pageCode
        except urllib2.URLError,e:
            print u'连接糗事百科失败，错误原因',e

    #获取到笑话，阅读量，评论
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex) #调用获取页面源码
        if not pageCode:
            print "页面加载失败。。。。"
            return None
        pattern = re.compile('<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?"number">(.*?)</i>.*?"number">(.*?)</i>',re.S) #编译，提高效率
        items = re.findall(pattern,pageCode)
        pageStories = [] #放置笑话的列表
        for item in items:
            it = item[1].replace('<span>','')
            it = it.replace('</span>','')
            pageStories.append([item[0],it,item[2],item[3]])
        return pageStories

    #缓存
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2: #小于两页
                pageStories = self.getPageItems(self.pageIndex) #获取新的一页
                if pageStories:
                    self.stories.append(pageStories) #stories代表已经缓存下来的段子
                    self.pageIndex += 1
    #调用
    def getOneStory(self,pageStories,page):
        n = 0 #当我们敲回车时的次数
        for story in pageStories:
            input = raw_input('')
            n += 1
            self.loadPage() #调用加载页面方法
            if input == "Q":
                self.enable == False
                return

            print u"第%d页\t第%d条发布人：%s\t%s" % (page,n,story[0],story[1]) #story[0]代表发布人，story[1]代表笑话
            print u"这条糗事百科的阅读量是%s，评论是%s条" % (story[2],story[3])

    #开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0 #局部变量，控制当前读到了第几页
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0] #从全局中取新笑话
                nowPage += 1
                del self.stories[0] #删除读过的，缓存新的笑话
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()

