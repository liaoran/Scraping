#-*- coding:utf-8-*-
__author__ = 'kongnian'
from Tkinter import *
from ScrolledText import ScrolledText
import urllib,requests,re,threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


a = 1  # 页数
url_name = []


def get():
    global a
    hd = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    url = 'http://www.budejie.com/video/' + str(a)
    varl.set('已经获取到第%s页视频' % a)
    html = requests.get(url,headers=hd).text
    url_content = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)', re.S)
    url_contents = re.findall(url_content,html)
    for i in url_contents:
        url_reg = r'data-mp4="(.*?)">'
        url_items = re.findall(url_reg,i)
        if url_items:
            name_reg = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>', re.S)
            name_items = re.findall(name_reg,i)
            for i,k in zip(name_items,url_items):
                url_name.append([i,k])
    return url_name


id = 1  # 视频个数


def write():
    global id
    while id < 10:
        url_name = get()
        for i in url_name:
            urllib.urlretrieve(i[1],'videos//%s.mp4' % i[0])
            text.insert(END,str(id)+'.'+i[1]+'\n'+i[0]+'\n')
            url_name.pop(0)
            id += 1
    varl.set('视频和名称抓取完毕！')


def start():
    th = threading.Thread(target=write)
    th.start()


root = Tk()
root.title('视频下载')
text = ScrolledText(root,font=('微软雅黑',10))
text.grid()
button = Button(root,text='开始爬取',font=('微软雅黑',10),command=start)
button.grid()
varl = StringVar()
label = Label(root,font=('微软雅黑',10),fg='red',textvariable=varl)
label.grid()
varl.set('已准备...')
root.mainloop()