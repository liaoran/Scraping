#-*- coding:utf-8 -*-
from Tkinter import *
from ScrolledText import ScrolledText #文本滚动条
import urllib
import re
import time
import threading

def get(ID):
    var1.set('已经获取到第%s本书' % ID)
    html = urllib.urlopen('https://read.douban.com/tag/%E7%9F%AD%E7%AF%87%E5%B0%8F%E8%AF%B4/?cat=article&sort=top&start=' + str(ID)).read()
    reg = r'<span class="price-tag ">(.*?)元</span>.*?<a href="/ebook/.*?/">(.*?)</a>'
    reg = re.compile(reg)
    return re.findall(reg,html)


#计算书本的数量
def write():
    ID = 0 #书本递增展示在GUI上的数量
    a = []
    s = 0 #书本数量
    while ID <= 240:
        L = get(ID) #调用上面的函数，获取书名跟价格
        ID += 20
        for i in L:
            s += 1
            a.append(float(i[0]))
            text.insert(END,'书名：%s         价格：%s\n' % (i[1],i[0]))

    text.insert(END,'------------------------\n')
    text.insert(END,'该分类书本总数量%s\n' % s)
    text.insert(END,'书本总价格：%s\n' % sum(a))
    text.insert(END,'平均每本%.2f元' % (sum(a)/s))
    fn = open('read.txt','w')
    fn.write(text.get(1.0,END).encode('utf-8'))
    fn.close()
    var1.set('全部处理完成')

def th():
    t1 = threading.Thread(target=write)
    t1.start()

root = Tk() #创建窗口
root.geometry('+800+200') #窗口大小
root.title('豆瓣图书展示')
text = ScrolledText(root,font=('微软雅黑',10))
text.grid() #布局方法
button = Button(root,text='开始采集',font=('微软雅黑',10),command = th)
button.grid()
var1 = StringVar() #设置变量，文字会发生改变
label = Label(root,font=('微软雅黑',10),fg='red',textvariable = var1)
label.grid()
var1.set('准备中...')
root.mainloop() #进入消息循环，发送命令
