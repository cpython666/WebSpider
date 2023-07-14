# -*- coding: utf-8 -*-
# @Time    : 2023/7/4 10:51
# @Author  : wsh
# @File    : run_huxiu_add_person.py
from Spider.models import *
import requests
# 虎嗅通过用户id获取该用户所有文章的接口
url='https://api-account.huxiu.com/web/article/articleList'

def get_articles_by_user_id(id):
    data = {
        'platform': 'www',
        'uid': id,
        'type': 0,
        'page': 1
    }
    res = requests.post(url=url, data=data).json()
    data=res['data']
    totalpage=data['total_page']
    for i in range(1,totalpage+1):
        data = {
            'platform': 'www',
            'uid': id,
            'type': 0,
            'page': i
        }
        res = requests.post(url=url, data=data).json()
        data = res['data']
        datalist=data['datalist']
        article_url=[i['url'] for i in datalist]
        print(article_url)
        for _ in article_url:
            save_url(_)

# id=1871517
# get_articles_by_user_id(id)

with open('huxiu_ids.txt','r',encoding='utf-8') as f:
    ids=f.read()
print(ids)
