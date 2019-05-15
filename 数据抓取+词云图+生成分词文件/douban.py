# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2019/5/1 0:28'
#流浪地球
import jieba
import requests
import pandas as pd
import time
import random
from lxml import etree
import codecs
import csv

from wordcloud import WordCloud
import PIL
import matplotlib.pyplot as plt
import numpy as np
import cv2

import pymongo


def start_spider():
    #https://movie.douban.com/subject/26266893/comments?status=P
    base_url = 'https://movie.douban.com/subject/26266893/comments'
    #base_url = "https://book.douban.com/subject/19995918/comments/"
    start_url=base_url+"?start=0"
    number = 1

    html = request_get(start_url)

    #数据既可以存csv又可以mongo数据库    ，不一定保证有环境所以这里注释了
    # client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    # db = client.test
    # dbname = 'earth'

    while html.status_code == 200:
        # 获取下一页的 url
        selector = etree.HTML(html.text)
        nextpage = selector.xpath("//div[@id='paginator']/a[@class='next']/@href")
        nextpage = nextpage[0]
        next_url = base_url + nextpage
        # 获取评论
        comments = selector.xpath("//div[@class='comment']")
        marvelthree = []

        # commentlist.append(user)
        # commentlist.append(watched)
        # commentlist.append(rating)
        # commentlist.append(comment_time)
        # commentlist.append(votes)
        # commentlist.append(content.strip())

        for each in comments:
            tmp=get_comments(each)
            marvelthree.append(tmp)
            print(tmp)

            # 数据既可以存csv又可以mongo数据库 ，不一定保证有环境所以这里注释了
            # try:
            #     data_tmp={
            #         'user':tmp[0],
            #         'watch':tmp[1],
            #         'rating':tmp[2],
            #         'time':tmp[3],
            #         'votes':tmp[4],
            #         'split':tmp[5]
            #     }
            #     db[dbname].insert_one(data_tmp)
            #     print('写入一个')
            # except:
            #     print('失败')


        data = pd.DataFrame(marvelthree)
        # 写入csv文件,'a+'是追加模式
        print(data.head())
        try:
            if number == 1:
                csv_headers = ['用户', '是否看过', '五星评分', '评论时间', '有用数', '评论内容']
                data.to_csv('./Earth_yingpping.csv', header=csv_headers, index=False, mode='a+', encoding='utf_8_sig')
            else:
                data.to_csv('./Earth_yingpping.csv', header=False, index=False, mode='a+', encoding='utf_8_sig')
        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

        html = request_get(next_url)
        number=number+1

def request_get(url):
    '''
    使用 Session 能够跨请求保持某些参数。
    它也会在同一个 Session 实例发出的所有请求之间保持 cookie
    '''
    timeout = 3

    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    ]

    header = {
        'User-agent': random.choice(UserAgent_List),
        'Host': 'movie.douban.com',
        #'Referer': 'https://movie.douban.com/subject/26100958/?from=showing',
    }

    session = requests.Session()

    cookie = {
        #'cookie':'bid=RmJoMiZFi7M; douban-fav-remind=1; ll="118254"; gr_user_id=e712b9ba-1506-45fb-a403-9fc101f05479; _vwo_uuid_v2=D58AA9923E1E261419125AD737A9E2ECA|36b7c53b8aec45befb83ec69146be2e6; viewed="26708820_25779298_27093745_27093647_30231519_20282296_1418776_30236842_30173624_30275915"; push_noty_num=0; push_doumail_num=0; dbcl2="179333894:PUpFVwhsLUk"; __utmv=30149280.17933; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1556894413%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utma=223695111.1187496661.1553679492.1556813776.1556894413.7; __utmz=223695111.1556894413.7.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=d6726781c19a7637.1553679492.7.1556895676.1556813776.; ck=flj3; ap_v=0,6.0; __utma=30149280.271240917.1551599238.1556894408.1556949764.33; __utmc=30149280; __utmz=30149280.1556949764.33.32.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.2.10.1556949764'
    }
    time.sleep(random.randint(5, 15))
    response = requests.get(url, headers=header, cookies=cookie, timeout = 3)
    if response.status_code != 200:
        print(response.status_code)
    return response

# def clearBlankLine(file_name):
#     file1 = open(file_name+'.dat', 'r', encoding='utf-8') # 要去掉空行的文件
#     file2 = open(file_name+'_no_blank.dat', 'w', encoding='utf-8') # 生成没有空行的文件
#     try:
#         for line in file1.readlines():
#             if line == '\n':
#                 line = line.strip("\n")
#             file2.write(line)
#     finally:
#         file1.close()
#         file2.close()

def get_comments(eachComment):
    commentlist = []
    user = eachComment.xpath("./h3/span[@class='comment-info']/a/text()")[0]  # 用户
    watched = eachComment.xpath("./h3/span[@class='comment-info']/span[1]/text()")[0]  # 是否看过
    rating = eachComment.xpath("./h3/span[@class='comment-info']/span[2]/@title")  # 五星评分
    if len(rating) > 0:
        rating = rating[0]

    comment_time = eachComment.xpath("./h3/span[@class='comment-info']/span[3]/@title")  # 评论时间
    if len(comment_time) > 0:
        comment_time = comment_time[0]
    else:
        # 有些评论是没有五星评分, 需赋空值
        comment_time = rating
        rating = ''

    votes = eachComment.xpath("./h3/span[@class='comment-vote']/span/text()")[0]  # "有用"数
    content = eachComment.xpath("./p/span/text()")[0]  # 评论内容
    content_c = eachComment.xpath("./p/span/text()")

    print('评论内容：')
    print(content)

    commentlist.append(user)
    commentlist.append(watched)
    commentlist.append(rating)
    commentlist.append(comment_time)
    commentlist.append(votes)
    commentlist.append(content.strip())
    # print(list)
    return commentlist

def split_word():
    with codecs.open('Earth_yingpping.csv', 'r','utf_8_sig') as csvfile:
        reader = csv.reader(csvfile)
        content_list = []
        for row in reader:
            try:
                cc = row[5]
                if len(cc) > 2:
                    content_list.append(cc)
                    #添加了评论数据

                #print("row5")
                #print(row[5])
            except IndexError:
                pass

        content = ''.join(content_list)


        seg_list = list(jieba.cut(content, cut_all=False))
        result = []
        for word in seg_list:
            if len(word) > 1:
                if word == '我们' or word == '他们' or word == '一个' or word == '电影':
                    continue
                result.append(word)

        result = '\n'.join(result)
        print(type(result))
        #print('result:::')
        print(type(result))

        return result

#写入分词文件
def write_seg_file():
    with codecs.open('Earth_yingpping.csv', 'r','utf_8_sig') as csvfile:
        reader = csv.reader(csvfile)
        content_list = []
        for row in reader:
            try:
                cc = row[5]
                if len(cc) > 2:
                    cc=cc.replace('\n',' ')
                    print('我知道'+cc)
                    content_list.append(cc)
            except:
                print('index_error')

        data={
            'content':content_list
        }

        with open('seg_data.dat', 'w+', encoding='utf-8') as f:
            for j in content_list:
                j.replace('\n',' ')
                tmp = ' '.join(list(jieba.cut(j)))
                print(tmp)
                f.write(tmp)

        print('分词库写入完成')

# def wordcloudplot(txt):
#     path = 'msyh.ttf'
#     path.encode('gb18030')
#     alice_mask = cv2.imread('mask2.jpg')
#     alic = cv2.resize(alice_mask, (960, 900), interpolation=cv2.INTER_CUBIC)
#     print(alic.shape)
#     wordcloud = WordCloud(font_path=path, background_color="white", margin=5, width=1800, height=800, mask=alic, max_words=2000, max_font_size=60, random_state=42)
#     wordcloud = wordcloud.generate(txt)
#     wordcloud.to_file('f2.jpg')
#     plt.imshow(wordcloud)
#     plt.axis("off")
#     plt.show()

#coding=utf-8
#导入wordcloud模块和matplotlib模块
from wordcloud import WordCloud,ImageColorGenerator
import  matplotlib.pyplot as plt
import jieba
import jieba.analyse


def show_gra(content):

    background_image = np.array(PIL.Image.open('mask2.jpg'))

    tags = jieba.analyse.extract_tags(content, topK=200, withWeight=False)
    text =" ".join(tags)
    print(text)
    # text = unicode(text)

    font=r'Songti.ttc'#
    wordcloud=WordCloud(mask=background_image,background_color='white',width=1000,max_font_size=100, height=1000,font_path=font,scale=3.5).generate(text)

    #img_color = ImageColorGenerator(self.img)
    #显示词云

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

    wordcloud.to_file('earth_test.jpg')

from matplotlib.font_manager import FontProperties
def Histogram(content):
    result = jieba.analyse.textrank(content, topK=20, withWeight=True)

    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]
    print(keywords)  # 输出一个字典的形式

    font = FontProperties(fname='Songti.ttc')
    bar_width = 0.5

    X = []
    Y = []

    for key in keywords:
        X.append(key)
        Y.append(keywords[key])

    num = len(X)

    fig = plt.figure(figsize=(28, 10))
    plt.bar(range(num), Y, tick_label=X, width=bar_width)

    plt.xticks(rotation=50, fontproperties=font, fontsize=20)
    plt.yticks(fontsize=20)
    plt.title("归一化词频直方图", fontproperties=font, fontsize=11)
    plt.savefig("归一化词频直方图.jpg", dpi=360)
    plt.show()

if __name__ == '__main__':
    start_spider()#爬虫程序，运行会覆盖生成的csv
    result = split_word()#分词，生成result
    write_seg_file()#生成分词文件 seg_data
    # show_gra(result)#显示词云图
    # Histogram(result)#显示直方图