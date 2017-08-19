# -*- coding:utf-8 -*-
import requests
import json
import xlwt

items = [] #招聘信息
pn = 1

#抓取数据
def get_content(pn):
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    data = {
        'first':'true',
        'pn':pn,
        'kd':'python'
    }
    #url发送post请求，把data数据发送过去
    html = requests.post(url,data).text #获取文本
    html = json.loads(html) #json格式字符串解码转换Python dict对象

    for i in range(14):
        item = []
        item.append(html['content']['positionResult']['result'][i]['positionName'])
        item.append(html['content']['positionResult']['result'][i]['companyFullName'])
        item.append(html['content']['positionResult']['result'][i]['salary'])
        item.append(html['content']['positionResult']['result'][i]['city'])
        item.append(html['content']['positionResult']['result'][i]['positionAdvantage'])
        item.append(html['content']['positionResult']['result'][i]['companyLabelList'])
        item.append(html['content']['positionResult']['result'][i]['firstType'])
        items.append(item)
        print items
    return items

#创建excel表格
def excel_write(items):
    newTable = 'test.xls'
    wb = xlwt.Workbook(encoding='utf-8') #创建文件
    ws = wb.add_sheet('test1') #创建表
    headData = ['招聘职位','公司','薪资','地区','福利','提供条件','工作类型']
    for hd in range(0,7):
        ws.write(0,hd,headData[hd],xlwt.easyxf('font:bold on')) #0代表行数，hd代表列数
    #写数据
    index = 1 #行
    for item in items:
        for i in range(0,7):
            print item[i]
            ws.write(index,i,item[i])
        index += 1 #隔一行写新数据
        wb.save(newTable) #保存

if __name__ == "__main__":
    items = get_content(pn)
    excel_write(items)