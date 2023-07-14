from mongoengine import Document,StringField,BooleanField,IntField
from pymongo.errors import DuplicateKeyError
from Spider.models import *

class Link(Document):
    url = StringField(required=True,unique=True)
    visited = BooleanField(default=False)
    meta = {
        'collection': 'links',  # 指定集合名称,
        'indexes': [
            'visited',
        ]
    }

def save_url(url):
    collection_name=get_collection_name(url,type='link')
    collection = Link().switch_collection(collection_name)._get_collection()
    query = {'url': url}
    result = collection.find_one(query)
    if result:
        logging.info(f'链接{url}已存储进{collection_name}集合')
        # print(f'链接{url}已存储')
    else:
        try:
            collection.insert_one({'url': url,'visited':False})
            logging.info(f'链接{url}已插入进{collection_name}集合')
            # print(f'链接{url}已插入')
        except DuplicateKeyError as e:
            print(str(e))
def visited_url(url):
    collection_name=get_collection_name(url,type='link')
    collection = Link()._get_db()[collection_name]
    query = {'url': url}
    result = collection.find_one(query)
    if result:
        update_query = {'$set': {'visited': True}}
        collection.update_one(query, update_query)

def init_url(url):
    collection_name=get_collection_name(url,type='link')
    collection = Link().switch_collection(collection_name)._get_collection()
    query = {'url': url}
    result = collection.find(query)
    if result:
        update_query = {'$set': {'visited': False}}
        collection.update_one(query, update_query)
    else:
        try:
            collection.insert_one({'url': url, 'visited': False})
            logging.info(f'链接{url}已插入')
            # print(f'链接{url}已插入')
        except DuplicateKeyError as e:
            print(str(e))

def get_one_url(domain=None,limit=1):
    db=Link()._get_db()
    collections=list(filter(lambda x:x.startswith('links_'),db.list_collection_names()))
    if domain:
        collections=list(filter(lambda x:domain in x,collections))
    collection=db[choice(collections)]
    pipeline = [
        { '$match': { 'visited': False } },
        { '$limit': limit }
    ]
    results=list(collection.aggregate(pipeline))
    return results

def get_one_error_url(domain=None,limit=1):
    db=Link()._get_db()
    collections=list(filter(lambda x:x.startswith('pages_'),db.list_collection_names()))
    if domain:
        collections=list(filter(lambda x:domain in x,collections))
    collection=db[choice(collections)]
    pipeline = [
        { '$match': { 'status_code': 404 } },
        { '$limit': limit }
    ]
    results=list(collection.aggregate(pipeline))
    return results

def get_link_count():
    pipeline = [
        {"$group": {"_id": None, "count": {"$sum": 1}}}
    ]
    return Link.objects.aggregate(*pipeline).next()['count']

def get_link_thepaper_user():
    db=Link()._get_db()
    collections=list(filter(lambda x:x.startswith('links_thepaper.cn'),db.list_collection_names()))
    print(collections)
# print(get_one_url())
if __name__ == '__main__':
    from Spider.models import *
    from Spider.models.utils import *

    # print(get_one_url())
    get_link_thepaper_user()