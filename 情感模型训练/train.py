#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jieba

from snownlp import sentiment
import codecs,csv
# 全模式
label_list=[]
content_list=[]
with codecs.open('Earth_yingpping.csv', 'r', 'utf_8_sig') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        try:

            cc = row[5]
            seg_list = jieba.cut(cc, cut_all=True)

            ll=row[6]
            content_list.append(' '.join(seg_list))

            label_list.append(ll)
                # 添加了评论数据

            # print("row5")
            # print(row[5])
        except IndexError:
            pass

array1=label_list#准确值

neg=[]
pos=[]
for i in range(1,100):
    # if array2[i]!='':
    #     count_sum+=1
    if (array1[i] == '-1'):
        neg.append(content_list[i])
    if (array1[i]=='1'):
        pos.append(content_list[i])

with open('neg','w+',encoding='utf-8') as f:
    f.write(' '.join(neg))
    f.close()
with open('pos','w+',encoding='utf-8') as f:
    f.write(' '.join(pos))
    f.close()

sentiment.train('neg','pos')
sentiment.save('sentiment.marshal')