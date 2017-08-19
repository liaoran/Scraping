#-*- coding:utf-8-*-
__author__ = 'kongnian'

import requests
from lxml import html

#日志，python3用
#def log(*args,**kwargs):
#   print(*args,**kwargs)

#def movie_log(*args,**kwargs):
#    with open('movie.txt','a') as f:
#        print(*args,file=f,**kwargs)


# 在打印一个东西的时候，实际上调用了str(m)，str(m)就是通过调用__repr__
# str() 产生人类可读的输出 repr() 产生机器可读的输出

class Model(object):
    def __repr__(self):
        #  得到实例的类名
        class_name = self.__class__.__name__
        #  self.__dict__会将实例变成一个字典
        #  item() 将字典变成[(key,value),()...]
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))
        return r


class Movie(Model):
    def __init__(self):
        self.ranking = 0  # 排名
        self.cover_url = ''  # 封面链接
        self.rating = 0  # 评分
        self.name = ''  # 电影名
        self.number_of_comments = 0  # 评分人数


def urls_from_douban():
    urls = []
    url = 'https://movie.douban.com/top250?start={}&filter='
    for index in range(0,250,25):
        u = url.format(index)
        urls.append(u)
    return urls


def movies_from_url(urls):
    all_movie = []
    for u in urls:
        r = requests.get(u)
        page = r.content
        root = html.fromstring(page)  # 树形结构
        movie_divs = root.xpath('//div[@class="item"]')  # 返回一个列表，每个元素都是一个element对象
        movies = [movie_from_div(div) for div in movie_divs]  # 归类好的电影数据
        all_movie.extend(movies)  # extends参数只能是列表，将列表里的元素添加到自己列表后面
    return all_movie


# 将信息归类
def movie_from_div(div):
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')[0]
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    #log('movie',movie)
    return movie


def download_covers(movies):
    for m in movies:
        image_url = m.cover_url
        r = requests.get(image_url)
        path = 'covers/' + m.name.split('/')[0] + '.jpg'
        with open(path,'wb') as f:
            f.write(r.content)


def main():
    urls = urls_from_douban()
    movies = movies_from_url(urls)
    #movie_log(movies)
    download_covers(movies)


if __name__ == '__main__':
    main()
