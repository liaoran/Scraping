#-*- coding:utf-8-*-
__author__ = 'kongnian'

import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept - Encoding': 'gzip, deflate',
    'Accept - Language': 'en-US,zh-CN;q=0.8,zh;q=0.5,en;q=0.3'
}


def get_urls(url):
    html = requests.get(url,headers=headers).text
    table = BeautifulSoup(html,'lxml').find('div',class_='houseList').find_all('div',class_='list rel')
    urls = []
    for item in table:
        urls.append(item.find('dl',class_='plotListwrap clearfix').find('a').get('href'))
    return urls


def get_content(url):
    url = 'http://yunhuguoji.fang.com/xiangqing/'
    try:
        response = requests.get(url,headers=headers,timeout=30)
        html = response.text.encode('ISO-8859-1').decode('utf-8','ignore')
    except Exception as e:
        print e

    soup = BeautifulSoup(html,'lxml')
    title = soup.find('div',class_='ceninfo_sq').find('h1').find('a').get_text()
    pri_table = soup.find('div',class_='box detaiLtop mt20 clearfix').find_all('span')
    price = pri_table[0].get_text()
    month_lilv = pri_table[1].get_text()
    lilv = pri_table[2].get_text()
    tables = soup.find('div',class_="inforwrap clearfix").find_all('dd')

    address = ''
    area = ''
    huanxian = ''
    chanquan = ''
    wuye = ''
    jungong = ''
    kfshang = ''
    jzjiegou = ''
    jzleibie = ''
    jzmianji = ''
    dqhushu = ''
    lvhua = ''
    rongji = ''
    wuyephone = ''
    wuyefei = ''
    fujia = ''
    for item in tables:
        if item.find('strong').get_text == '小区地址：':
            address = item.get('title')
        if item.find('strong').get_text == '所属区域：':
            area = item.get_text().replace('所属区域：','')
        if item.find('strong').get_text == '环线位置':
            huanxian = item.get_text().replace('环线位置：', '')
        if item.find('strong').get_text == '产权描述：':
            chanquan = item.get_text().replace('产权描述：', '')
        if item.find('strong').get_text == '物业类别：':
            wuye = item.get_text().replace('物业类别：','')
        if item.find('strong').get_text == '竣工时间：':
            jungong = item.get_text().replace('竣工时间：','')
        if item.find('strong').get_text == '开 发 商：':
            kfshang = item.get_text().replace('开 发 商：','')
        if item.find('strong').get_text == '建筑结构：':
            jzjiegou = item.get_text().replace('建筑结构：','')
        if item.find('strong').get_text == '建筑类别：':
            jzleibie = item.get_text().replace('建筑类别：','')
        if item.find('strong').get_text == '建筑面积：':
            jzmianji = item.get_text().replace('建筑面积：','')
        if item.find('strong').get_text == '当期户数：':
            dqhushu = item.get_text().replace('当期户数：','')
        if item.find('strong').get_text == '绿 化 率：':
            lvhua = item.get_text().replace('绿 化 率：','')
        if item.find('strong').get_text == '容 积 率：':
            rongji = item.get_text().replace('容 积 率：','')
        if item.find('strong').get_text == '物业办公电话：':
            wuyephone = item.get_text().replace('物业办公电话：','')
        if item.find('strong').get_text == '物 业 费：':
            wuyefei = item.get_text().replace('物 业 费：','')
        if item.find('strong').get_text == '附加信息：':
            fujia = item.get_text().replace('附加信息：','')

    return title,price,month_lilv,lilv,address,area,huanxian,chanquan,wuye,jungong,kfshang,jzjiegou,jzleibie,jzmianji,dqhushu,lvhua,rongji,wuyephone,wuyefei,fujia


def save(content,file):
    a = ''
    for item in content:
        a = a + item + '|'
    file.write(a)


def main():
    f = open('data.txt','w')
    start_url = 'http://esf.sh.fang.com/housing/__0_0_0_0_2_0_0/'
    urls = get_urls(start_url)
    for url in urls:
        contents = get_content(url)
        save(contents,file)
        break


if __name__ == '__main__':
    main()