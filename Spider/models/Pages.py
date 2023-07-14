from mongoengine import Document,StringField,DateTimeField,EmailField,IntField
from datetime import datetime
from Spider.models import *

class Page(Document):
    url = StringField(required=True,unique=True)
    status_code=IntField()
    msg=StringField()
    html = StringField()
    timestamp = DateTimeField(default=datetime.now)
    title=StringField()
    content=StringField()
    abstract=StringField()

    meta = {
        'collection': 'pages',  # 指定集合名称
        'indexes': [
            'url',
            'status_code',
            'timestamp',
        ]
    }

def save_page(url,status_code=None,msg=None,html=None,title=None,content=None,abstract=None):
    timestamp = datetime.now()
    collection_name=get_collection_name(url=url,type='page')
    collection = Page().switch_collection(collection_name)._get_collection()
    query = {'url': url}
    result = list(collection.find(query))
    # 如果页面数据已存在并且此次请求码为200,则更新
    # if result and status_code==200:
    #     update_query = {'$set': {'status_code':status_code,
    #                              'msg':msg,'html':html,'timestamp':timestamp,
    #                              'title':title,'content':content,'abstract':abstract}}
    #     collection.update_one(query, update_query)
    #     print(f'页面{url}已更新进{collection_name}集合')
    if result==[]:
        collection.insert_one({'url':url,
                               'status_code':status_code,
                                 'msg':msg,'html':html,'timestamp':timestamp,
                                 'title':title,'content':content,'abstract':abstract})
        print(f'页面{url}已插入进{collection_name}集合')
    elif result[0]['status_code']==404:
        if status_code == 201:
            collection.update_one({'url':url},{"$set":{'status_code':status_code,
                                                     'msg':msg,'html':html,'timestamp':timestamp,
                                                     'title':title,'content':content,
                                                   'abstract':abstract}})
            print(f'页面{url}已更新进{collection_name}集合')
        elif status_code ==404:
            status_code=405
            collection.update_one({'url':url},{"$set":{'status_code':status_code,
                                                     'msg':msg,'html':html,'timestamp':timestamp,
                                                     'title':title,'content':content,
                                                   'abstract':abstract}})
            print(f'页面{url}已更新进{collection_name}集合')


def get_scuess_len():
    return len(Page.objects(status_code=200))

def get_detail_count():
    pipeline = [
        {"$group": {"_id": None, "count": {"$sum": 1}}},
    ]
    return Page.objects.aggregate(*pipeline).next()['count']



def get_domains():
    '''查询域名的集合'''
    pipeline = [
        {"$project": {
            "_id": 0,
            "domain": {"$arrayElemAt": [{"$split": ["$url", "/"]}, 2]}
        }},
        {"$group": {"_id": None, "domains": {"$addToSet": "$domain"}}},
        {"$project": {"_id": 0, "domains": 1}}
    ]

    # 执行聚合查询
    result = Page.objects.aggregate(*pipeline)

    # 获取查询结果
    for doc in result:
        domains = doc['domains']
        print(domains)



def get_page_count():
    pipeline = [
        {"$group": {"_id": None, "count": {"$sum": 1}}}
    ]
    return Page.objects.aggregate(*pipeline).next()['count']

# def get_page_by_url(url):



if __name__=="__main__":
    from Spider.models.utils import *
    from Spider.models import *
    from Spider.utils import *
    pass