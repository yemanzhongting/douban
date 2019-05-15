#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from snownlp import sentiment
#import numpy as np
from snownlp import SnowNLP
#from snownlp.sentiment import Sentiment
from lxml import etree
import codecs
import csv

comment = []

array1 =[]
array2 =[]

count_num = 0

content_list = []
label_list=[]
with codecs.open('Earth_yingpping.csv', 'r', 'utf_8_sig') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        try:
            cc = row[5]
            ll=row[6]
            content_list.append(cc)
            label_list.append(ll)
                # 添加了评论数据

            # print("row5")
            # print(row[5])
        except IndexError:
            pass

print(content_list)
print(label_list)

for line_data in content_list:
    
    comment = line_data
    try:
        s = SnowNLP(comment)
        rates = s.sentiments

        if (rates >= 0.5):
            eva_label = 1

        else:
            eva_label = -1

        eva = str(eva_label)
    except:
        eva=''

    array2.append(eva)
    # f = open("eva_result.dat", "a+")
    # f.write(eva)
    # f.write('\n')
    #f.close()
#
# for line1 in open("eva_label.dat"):
#     array1.append(line1)

array1=label_list#准确值

# for line2 in open("eva_result.dat"):
#     array2.append(line2)   判断值

count_sum=0
for i in range(1,100):
    if array2[i]!='':
        count_sum+=1
        if (array1[i] == array2[i]):

            count_num += 1

print(count_sum)
print(count_num)
#0.5454545454545454
correct_rate = count_num / count_sum

print(correct_rate)

# 99
# 96
# 0.9696969696969697