import scrapy
import bs4
import re
from ..items import RecordItem
from pymongo import MongoClient


class DoubanSpider(scrapy.Spider):
    name = "doban"
    allowed_domains = ['douban.com']
    start_urls = []

    for x in range(62):#0-62,62-124,124-186,186-248
        url = 'https://book.douban.com/top250?start=' + str(x * 25)
        start_urls.append(url)
        # 把豆瓣Top250图书的xx-xx页网址添加进start_urls。

    def start_requests(self):
        for book_url in self.start_urls:
            yield scrapy.Request(book_url,callback=self.parse,dont_filter=True)

    def parse(self, response):

        # parse是默认处理response的方法。
        bs_book = bs4.BeautifulSoup(response.text, 'html.parser')

        # 用BeautifulSoup解析response。
        #book_list =[ bs_book.find('tr', class_="item")]#test
        #print(book_list)
        book_list=bs_book.find_all('tr',class_="item")
        for book in book_list:
            #print(book)
            # 历遍book_list
            comment_url=book.find('a')['href']+'comments/'
            print(comment_url)
            yield scrapy.Request(comment_url,callback=self.parse_users_enter,meta={'head':comment_url},dont_filter=True)
            # 进入当前书目短评页面。

    def parse_users_enter(self,response):
        '''获取用户页面'''
        bs_user_list=bs4.BeautifulSoup(response.text,'html.parser')
        #user_list = [bs_user_list.find('li', class_="comment-item")]#test
        #print(user_list)
        user_list=bs_user_list.find_all('li',class_="comment-item")
        for user in user_list:
            for i in range(3):
                u_url=user.find('a')['href']+"collect?start="+str(i*30)+"&sort=time&rating=all&filter=all&mode=list"
                try:
                    yield scrapy.Request(u_url,callback=self.parse_user_records,dont_filter=True)
            #进入用户‘读过’页面
                except Exception:
                    None
        try:
            url_head=response.meta['head']
            next_user_page_url=bs_user_list.find('div',class_="paginator-wrapper").find('a',attrs={'data-page':"next"})['href']
        except Exception:
            print('we meet an error')
            next_user_page_url=None
        if next_user_page_url:
            print('we get'+url_head+next_user_page_url)
            yield scrapy.Request(url_head+next_user_page_url,meta={'head':url_head},callback=self.parse_users_enter,dont_filter=True)

    def parse_user_records(self,response):

        bs_user=bs4.BeautifulSoup(response.text, 'html.parser')
        #读取每个用户的九十条记录，即前3页，不足三页读取全部，同时存储用户id，书名，时间，id用来数据除重
        #print(bs_user)
        try:
            record_list=bs_user.find_all('li',class_="item")

        except Exception:
            record_list=None
        #print(record_list)
        for info in record_list:
        #    print("we are in")
            record=RecordItem()
            #实例化一个RecordItem对象
            try:
                patt1='/\S/'
                temp_bookname=info.find('div',class_="title").find('a').text
                record['bookname']=re.search('\S+',temp_bookname).group()
            except Exception:
                record['bookname']='no info'
            try:
                temp_date=info.find('div',class_="date").text
                record['date']=re.search('\S+',temp_date).group()
            except Exception:
                record['date']='no info'
            try:
                temp_rate=info.find('div',class_="date").find('span')['class'][0]
                record['rate']=re.search('[0-9]+',temp_rate).group()
            except Exception:
                record['rate']='no info'

            try:
                temp_publish=info.find('div',class_="grid-date").find('span',class_="intro").text
                record['author']=re.sub(r'/.*$', "", temp_publish)
            except Exception:
                record['author']='no info'
            try:
                temp_id=bs_user.find('ul',class_="nav-list").find('li').find('a')['href']
                record['user_id']=re.sub('/',"",re.sub(r'/people/',"",temp_id))
            except Exception:
                record['user_id']='no info'
            try:
                record['tag_url']=info.find('div',class_="title").find('a')['href']

            except Exception:
                record['tag_url']='no info'
            #print(dict(record))
            yield record        #返回一个对象!!!!!!!

    '''def parse_tag(self,response):

        #tag=''
        bs_tag=bs4.BeautifulSoup(response.text,'html.parser')
        tag_list=bs_tag.find('div',class_='indent').find_all('a',class_='  tag')
        print(tag_list)'''




#index error add try and except
#RecordItem

