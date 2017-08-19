# -*- coding:utf-8 -*-
import urllib2,re
from bs4 import BeautifulSoup


# 获取主页源码
def getContentOrComment(Url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    headers = {'User-Agent':user_agent}
    req = urllib2.Request(url=Url,headers=headers)
    try:
        response = urllib2.urlopen(req)
        content = response.read().decode('utf-8') #获取源码
    except Exception,e:
        content = None
    return content

articleUrl = "https://www.qiushibaike.com/textnew/page/%d"#文章地址
commentUrl = "https://www.qiushibaike.com/article/%s"#评论地址
page = 0
while True:
    raw = raw_input("点击enter查看或者输入exit退出，请输入你的选择：")
    if raw == "exit":
        break
    page += 1
    Url = articleUrl % page
    print Url
    articlePage = getContentOrComment(Url)

    #获取文章内容
    soupArticle = BeautifulSoup(articlePage,'html.parser')
    articleFloor = 1 #楼层，为了美观
    for string in soupArticle.find_all(attrs="article block untagged mb15"):
        commentId = str(string.get('id'))[11:]
        print articleFloor,".",string.find(attrs="content").get_text().strip() #获取文章段子正文
        articleFloor += 1

        #获取评论
        commentPage = getContentOrComment(commentUrl % commentId) #获取评论页源码
        if commentPage is None:
            continue
        soupComment = BeautifulSoup(commentPage,'html.parser')
        commentFloor = 1
        for comment in soupComment.find_all(attrs="body"):
            print "     ",commentFloor,"楼回复：",comment.get_text()
            commentFloor += 1



