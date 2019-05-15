#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
#from snownlp.sentiment import Sentiment
import matplotlib.pyplot as plt

#训练库G:\ProgramData\Anaconda3\Lib\site-packages\snownlp\sentiment

comment = []
pos_count = 0
neg_count = 0

for line_data in open("seg_data.dat",encoding='utf-8'):
    
    comment = line_data
    
    s = SnowNLP(comment)
    rates = s.sentiments    
    
    if (rates >= 0.5):
        pos_count += 1

    elif (rates < 0.5):
        neg_count += 1
    
    else :
        pass

#\n(eg. pray,eulogize and suggestion)   \n(eg. abuse,sarcasm and indignation)
labels = 'Positive Side', 'Negative Side'
fracs = [pos_count,neg_count]
explode = [0.1,0] # 0.1 凸出这部分，
plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
#autopct ，show percet

plt.pie(x=fracs, labels=labels, explode=explode,autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)

plt.savefig("emotions_pie_chart.jpg",dpi = 360)
plt.show()
