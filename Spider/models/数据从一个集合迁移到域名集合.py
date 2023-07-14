from mongoengine import Document,StringField,BooleanField
from Spider.models import *
# 链接表（Links）
class Link(Document):
    url = StringField(required=True,unique=True)
    visited = BooleanField(default=False)
    meta = {
        'collection': 'links',  # 指定集合名称,
        'indexes': [
            'visited',
        ]
    }


# collection=Link().switch_collection('a111')._get_collection()
# # collection=collection._get_collection()
# # link=collection._get_collection().find()
# query = {'url': '12345612'}
# result = collection.find_one(query)
# if result:
#     new_value = '222'
#     update_query = {'$set': {'url': new_value}}
#     collection.update_one(query, update_query)
#     print('Document updated.')
# else:
#     # 插入新文档
#     new_document = {'url': '12345612'}
#     collection.insert_one(new_document)
#     print('Document inserted.')


def move_links(limit=1):
    '''
    将链接从links集合转移到链接域名集合
    '''
    for _ in range(limit):
        print(Link.objects.first().to_json())
        link=Link.objects.first()
        url,collection_name,id=link['url'].strip('.'),get_collection_name(link['url'].strip('.'),type='link'),link['id']
        print(url,collection_name,id)
        link=link.switch_collection(collection_name.strip('.'))
        link.id=None
        link.url=url
        link.save(collention=collection_name)
        # link.save()
        Link.objects(id=id).delete()
# move_links(180000)

def query_links(url,type='link'):
    '''
    查询某个链接或者页面是否存在
    '''
    collection_name=get_collection_name(url,type=type).strip('.')
    collection=Link().switch_collection(collection_name)
    return collection._get_collection().count_documents({'url':url})
# print(query_links('https://spanish.news.cn/index.htm'))

def move_pages(limit=1):
    '''
    将页面从pages集合转移到页面域名集合
    '''
    for _ in range(limit):
        print(Page.objects.first().to_json())
        page=Page.objects.first()
        url,collection_name,id=page['url'].strip('.'),get_collection_name(page['url'].strip('.'),type='page'),page['id']
        print(url,collection_name,id)
        page=page.switch_collection(collection_name)
        page.id=None
        # link.url=url
        page.save(collention=collection_name)
        Page.objects(id=id).delete()
# move_pages(50000)