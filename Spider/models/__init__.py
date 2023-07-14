from mongoengine import connect
connect(db='Spider',
        # username='root',
        # password='1234',
        host='localhost',
        port=27017,
        # authSource='root',
        maxPoolSize=10,
        minPoolSize=8,
        )

# 发现使用mongoengine不灵活
# 使用pymongo灵活点
from Spider.logs import logging

from Spider.config import *
from Spider.utils import *


from Spider.models.Links import *
from Spider.models.Pages import *
from Spider.models.utils import *

if __name__ == '__main__':
    print(get_collection_name('http://slide.news.sina.com.cn/c/slide_1_86058_574167.html'))
    # print(get_collection_name('http://news.sohu.com/20100126/n269841322.shtml'))
    # print(get_collection_name('https://news.163.com/photoview/00AN0001/2314408.html'))


