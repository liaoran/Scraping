# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import lxml

url = 'http://ta.meituan.com/'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'ta.meituan.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Content-Type':'text/html; charset=UTF-8'
}

#获取分类信息（美食，电影）
def get_start_links(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    links = [link.find('div').find('div').find('dl').find('dt').find('a')['href']
             for link in soup.find_all('div',class_ = 'J-nav-item')]
    return links

#因为是ajax加载，获取店铺ID
def get_detail_id(url,headers=None):
    html = requests.get(url,headers=headers).text
    soup = BeautifulSoup(html,'lxml')
    content_id = json.loads(soup.find('div',class_ ='J-scrollloader cf J-hub')['data-async-params'])
    return json.loads(content_id.get('data')).get('poiidList')

#获取店铺详情数据
def get_item_info(url,headers=None):
    html = requests.get(url,headers=headers).text
    soup = BeautifulSoup(html,'lxml')
    title = soup.find('span',class_ = 'title').text
    score = soup.find('span',class_ = 'biz-level').get_text()
    address = soup.find('span',class_ = 'geo').text
    phone = soup.find_all('p',class_ = 'under-title')[1].get_text()
    evaluation_number = soup.find('a',class_ = 'num rate-count').text
    print u'店名：' + title
    print u'地址：' + address
    print u'电话：' + phone
    print u'得分：' + score.strip()
    print u'评价人数：' + evaluation_number
    print '========================'
    return (title,score,address,phone,evaluation_number)

#多页获取商品ID
def main(url):
    start_url_list = get_start_links(url)
    for j in start_url_list: #分类链接
        for i in range(1,11): #多页
            category_url = j + '/all/page{}'.format(i) #完整的分类多页链接
            shop_id_list = get_detail_id(category_url,headers=headers)
            #print shop_id_list
            for shop_id in shop_id_list:
                items = get_item_info(url + 'shop/{}'.format(shop_id),headers)
                items_list.append(items)

if __name__ == '__main__':
    items_list = []
    main(url)