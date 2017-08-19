#-*- coding:utf-8-*-
__author__ = 'kongnian'

import requests
from bs4 import BeautifulSoup
import xlwt

#获取源代码
def get_content(url,headers=None,proxy=None):
    html = requests.get(url,headers=headers).content #content可解决网站编码问题
    return html

def get_url(html):
    soup = BeautifulSoup(html,'lxml')
    shop_url_list = soup.find_all('div',class_='tit')
    return [i.find('a')['href'] for i in shop_url_list]

def get_detail_content(html):
    soup = BeautifulSoup(html,'lxml')
    price = soup.find('span',id='avgPriceTitle').text
    evaluation = soup.find('span',id='comment_score').find_all('span',class_='item')
    the_star = soup.find('div',class_='brief-info').find('span')['title']
    title = soup.find('div',class_='breadcrumb').find('span').text
    comments = soup.find('span',id='reviewCount').text
    address = soup.find('span',itemprop='street-address').text
    print u'店名：' + title
    for i in evaluation:
        print i.text
    print price
    print u'评论数量：' + comments
    print u'地址：' + address.strip()
    print u'评价星级：' + the_star
    print '==================='
    return (title,evaluation[0].text,evaluation[1].text,evaluation[2].text,address,the_star,price,comments)

if __name__ == '__main__':
    items = []
    start_url = 'https://www.dianping.com/search/category/344/10'
    base_url = 'https://www.dianping.com'
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Cookie':'JSESSIONID=0B1A4A964767929665BEB1D2558C9232; aburl=1; cy=344; cye=changsha; _hc.v=b09660a9-ac75-b2ac-a26b-61828797d158.1501496326; __utma=1.1053894146.1501496327.1501496327.1501496327.1; __utmc=1; __utmz=1.1501496327.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; s_ViewType=10; _lxsdk_cuid=15d982d0609c8-0be036f20867708-70216751-100200-15d982d060aa6; _lxsdk=15d982d0609c8-0be036f20867708-70216751-100200-15d982d060aa6; _lxsdk_s=15d982d060c-889-987-78d%7C%7C23; PHOENIX_ID=0a010725-15d983d4be6-bcef8c4; __mta=54311703.1501497742331.1501497742331.1501497742331.1'
    }
    start_html = get_content(start_url)
    url_list = [base_url + url for url in get_url(start_html)]
    for i in url_list:
        detail_html = get_content(i,headers=headers)
        item = get_detail_content(detail_html)
        items.append(item)

    newTable = 'DZDP.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('test1')
    headData = ['商户名称','口味评分','环境评分','服务评分','人均价格','评论数量','地址','商户星级']
    for colnum in range(0,8):
        ws.write(0,colnum,headData[colnum],xlwt.easyxf('font:bold on'))

    index = 1

    lens = len(items)
    for j in range(0,lens):
        for i in range(0,8):
            ws.write(index,i,items[j][i])
        index += 1

    wb.save(newTable)



