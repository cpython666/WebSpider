from mongoengine import Document,StringField,BooleanField
# 链接表（Links）
from Spider.config import *
from pprint import pprint
from pymongo.errors import DuplicateKeyError

import pymongo
from Spider.models import *
class Test(Document):
    url = StringField(required=True,unique=True)
    visited = BooleanField(default=True)
    a=StringField()
    meta = {
        'collection': 'test',  # 指定集合名称,
        'indexes': [
            'visited',
        ]
    }

from time import sleep
def delete():
    '''删除多于垃圾集合'''
    db=Test()._get_db()
    cols=db.list_collection_names()
    for col in cols:
        print(col)
        pipeline = [
            {"$group": {"_id": None, "count": {"$sum": 1}}}
        ]
        count = list(db[col].aggregate(pipeline))
        print(count)
        if count and count[0]['count']<20:
            db[col].drop()
            print(f'删除了{col}')
            sleep(1)
        else:
            print(f'没有删除{col}')

def delete_other_domain():
    # 删除不允许域名的集合
    db=Test()._get_db()
    cols=db.list_collection_names()
    print('集合名',cols)
    print('允许域名',allowed_domains)
    tmp=[i.split('_')[-1].replace('www.','') for i in cols]
    print('集合名去掉前缀',tmp)
    tmp_=[i for i in tmp if i not in allowed_domains]
    print('不允许的集合',tmp_)
    for col_name in cols:
        if col_name.split('_')[-1].replace('www.','') not in allowed_domains:
            print(col_name)
            db[col_name].drop()

def move_data_to_no_www():
    # 将www开头的移到没有www开头的
    db=Test()._get_db()
    colllections=list(filter(lambda x:x.startswith('pages_www') or x.startswith('links_www'),db.list_collection_names()))
    for collection in colllections:
        print(collection)
        while True:
            obj=db[collection].find_one({})
            if obj==None:
                break
            collection_=collection.replace('www.','')
            try:
                obj['id']=None
                db[collection_].insert_one(obj)
                print(obj['url'])
            except Exception as e:
                print(e)
            filter_query = {'url': obj['url']}
            db[collection].delete_one(filter_query)

        #     break
        # break
    print(colllections)

    # a=list(db.find())
    # print(db.insert_one({'url': 121}))
    # print(a)

def remove_www_col():
    # 删除pages_www或者links_www.开头的集合
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_www') or x.startswith('links_www'), db.list_collection_names()))
    # collections=db.list_collection_names()
    print(collections)
    for collection in collections:
        obj = db[collection].find_one({})
        if obj == None:
            db[collection].drop()
            print(f'{collection}已删除')
        else:
            print(collection)

def filter_url_on_links_and_pages():
    # 遍历页面和连接集合,将//开头链接去掉开头//,并去掉不允许域名链接
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_') or x.startswith('links_'), db.list_collection_names()))
    print(collections)
    # pprint(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url=data['url']
            netloc=get_netloc(url)
            if netloc=='' or data['url'].startswith('//') or netloc not in allowed_domains:
                # print(data)
                print(url)
                db[collection].delete_one({'url':url})
                # db[collection].update_one({'url':data['url']},{"$set": {"url": url}})
                # break
            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})
        # break

def move_data_to_right_collection():
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages') or x.startswith('links'), db.list_collection_names()))
    print(collections)
    types=['links_','pages_']
    for collection in collections:
        for type_tmp in types:
            if collection.startswith(type_tmp):
                collection_type=type_tmp
                collection_netloc=collection.split(type_tmp)[-1]
                break
        else:
            collection_type=None
            collection_netloc=None

        print(collection,collection_type,collection_netloc)
        if collection_netloc is None and collection_type is None:
            netloc='abcdefg'
            collection_type=collection+'_'
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            id = data['_id']
            url = data['url']
            netloc = get_netloc(url)
            if netloc != collection_netloc:
                print(data)
                print(url)
                db[collection].delete_one({'url': url})
                # data['_id']=None
                try:
                    db[collection_type+netloc].insert_one(data)
                    print(data['url'],'未插入')
                except DuplicateKeyError:
                    print(data['url'],'已插入')
            data = db[collection].find_one({"_id": {"$gt": id}})
        # break
def update_null_key():
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages') or x.startswith('links'), db.list_collection_names()))
    for collection in collections:
        print(collection)
        data=db[collection].find_one({'_id':None})
        if data:
            data_ = {}
            print(data)
            # print(data.keys())
            for key in data.keys():
                if key!='_id':
                    data_[key]=data[key]
            db[collection].delete_one({'url':data['url']})
            try:
                db[collection].insert_one(data_)
            except DuplicateKeyError:
                print('键值重复')
def test_thread_id():
    db=Test()._get_db()
    print(id(db))
def compare_links_and_pages():
    db = Test()._get_db()
    collections = list(
        filter(lambda x : x.startswith('links_'), db.list_collection_names()))
    print(collections)
    # pprint(collections)
    for collection in collections:
        data_link = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data_link:
            url=data_link['url']
            visited=data_link['visited']
            netloc=get_netloc(url)
            data_page=db['pages_'+netloc].find_one({'url':url})
            if data_page is None and visited == True:
                db[collection].update_one({'url':url},{'$set':{'visited':False}})
                print(data_link)

            data_link = db[collection].find_one({"_id": {"$gt": data_link["_id"]}})
        #     break
        # break
def turn_huxiu_http_to_https():
    db = Test()._get_db()
    collections = list(
        filter(lambda x:x.startswith('links_huxiu.com') or x.startswith('pages_huxiu.com'), db.list_collection_names()))
    print(collections)
    for collection in collections:
        data_link = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data_link:
            url=data_link['url']
            if url.startswith('http://'):
                try:
                    db[collection].update_one({'url':url},{'$set':{'url':url.replace('http://','https://')}})
                except DuplicateKeyError:
                    db[collection].delete_one({'url':url})
            data_link = db[collection].find_one({"_id": {"$gt": data_link["_id"]}})

def get_page_by_url(url):
    db = Test()._get_db()
    collections = list(
        filter(lambda x:x.startswith('pages_huxiu.com'), db.list_collection_names()))
    print(collections)
    data=db[collections[0]].find_one({'url':url}, sort=[("_id", pymongo.ASCENDING)])
    print(data)

def change_huxiu_no_www():
    # 将虎嗅网网址规范化统一化,去掉无意义tag（#），域名格式统一
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_huxiu.com') or x.startswith('links_huxiu.com'),
               db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url = data['url']
            new_url = ''
            try:
                if url.startswith('http://huxiu.com'):
                    new_url=url.replace('http://huxiu.com', 'https://www.huxiu.com')
                    db[collection].update_one({'url': url}, {'$set': {
                        'url': new_url}})
                    print(url)
                elif url.startswith('https://huxiu.com'):
                    new_url=url.replace('https://huxiu.com', 'https://www.huxiu.com')
                    db[collection].update_one({'url': url}, {'$set': {
                        'url': new_url}})
                    print(url)
                elif url.startswith('http://www.huxiu.com'):
                    new_url=url.replace('http://www.huxiu.com', 'https://www.huxiu.com')
                    db[collection].update_one({'url': url}, {'$set': {
                        'url': new_url}})
                    print(url)
                else:
                    new_url=url
                    # print(url)
            except DuplicateKeyError:
                db[collection].delete_one({'url': url})
                print(url,'已删除')

            try:
                if '#' in new_url or '?' in new_url:
                    print(new_url)
                    new_url_=clean_tags_of_link(new_url)
                    print(new_url_)
                    db[collection].update_one({'url': new_url}, {'$set': {
                        'url': new_url_}})
            except DuplicateKeyError:
                db[collection].delete_one({'url': new_url})
                print(new_url,'已删除')

            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})

def change_thepaper_no_www():
    # 将澎湃网网址规范化统一化,去掉无意义tag（#），域名格式统一
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_thepaper.cn') or x.startswith('links_thepaper.cn'), db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url=data['url']
            new_url = url
            try:
                flag=False
                if url.startswith('http://thepaper.cn'):
                    flag = True
                    new_url=url.replace('http://thepaper.cn','https://www.thepaper.cn').replace('?commTag=true','')
                elif url.startswith('https://thepaper.cn'):
                    flag = True
                    new_url=url.replace('https://thepaper.cn','https://www.thepaper.cn').replace('?commTag=true','')
                elif url.startswith('http://www.thepaper.cn'):
                    flag = True
                    new_url=url.replace('http://www.thepaper.cn','https://www.thepaper.cn').replace('?commTag=true','')
                elif '?commTag=true' in url:
                    flag = True
                    new_url=url.replace('?commTag=true','')
                if flag:
                    db[collection].update_one({'url':url},{'$set':{'url':new_url}})
                    print(url)
            except DuplicateKeyError:
                db[collection].delete_one({'url':url})

            try:
                if '#' in new_url or '?' in new_url:
                    print(new_url)
                    new_url_=clean_tags_of_link(new_url)
                    print(new_url_)
                    db[collection].update_one({'url': new_url}, {'$set': {
                        'url': new_url_}})
            except DuplicateKeyError:
                db[collection].delete_one({'url': new_url})
                print(new_url,'已删除')

            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})
def change_sohu_no_www():
    # 将搜狐网网址规范化统一化,去掉无意义tag（#），域名格式统一
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_sohu.com') or x.startswith('links_sohu.com'), db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url=data['url']
            new_url = url
            try:
                flag=False
                if url.startswith('http://'):
                    flag = True
                    new_url=url.replace('http://','https://')
                elif url.startswith('https://'):
                    new_url=url
                if new_url.startswith('https://sohu.com'):
                    flag = True
                    new_url=url.replace('https://sohu.com','https://www.sohu.com')
                if '#' in new_url or '?' in new_url:
                    flag=True
                    print(new_url)
                    new_url=clean_tags_of_link(new_url)
                    print(new_url)
                if flag:
                    db[collection].update_one({'url':url},{'$set':{'url':new_url}})
                    print(url)
            except DuplicateKeyError:
                db[collection].delete_one({'url':url})

            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})

def clean_thepaper_no_target():
    # 删除个人信息，标签页，话题，问题页面
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_thepaper.cn') or x.startswith('links_thepaper.cn'),
               db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url = data['url']
            i=url
            if not i.startswith('https://www.thepaper.cn/tag/') and not i.startswith('https://www.thepaper.cn/user_') \
                and not i.startswith('https://www.thepaper.cn/asktopic_detail_') \
                and not i.startswith('https://www.thepaper.cn/ask_index') \
                and not i.startswith('https://www.thepaper.cn/gov_') \
                and not i.startswith('https://www.thepaper.cn/list_'):
                pass
            else:
                db[collection].delete_one({'url': i})
                print(i, '已删除')
                # break
            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})

def clean_huxiu_no_target():
    # 删除个人信息，标签页，话题，问题页面
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_huxiu.com') or x.startswith('links_huxiu.com'),
               db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url = data['url']
            i=url
            if not i.startswith('https://www.huxiu.com/zttype/') and not i.startswith('https://www.huxiu.com/ztcontents/') \
                and not i.startswith('https://www.huxiu.com/zhuanti/') \
                and not i.startswith('https://www.huxiu.com/wow') \
                and not i.startswith('https://www.huxiu.com/v') \
                and not i.startswith('https://www.huxiu.com/u') \
                and not i.startswith('https://www.huxiu.com/t') \
                and not i.startswith('https://www.huxiu.com/s') \
                and not i.startswith('https://www.huxiu.com/r') \
                and not i.startswith('https://www.huxiu.com/p') \
                and not i.startswith('https://www.huxiu.com/m') \
                and not i.startswith('https://www.huxiu.com/r') \
                and not i.startswith('https://www.huxiu.com/active/'):
                pass
            else:
                db[collection].delete_one({'url': i})
                print(i, '已删除')
                # break
            data = db[collection].find_one({"_id": {"$gt": data["_id"]}})
def clean_all_pages_css_and_script():
    # 删除页面里的所有css与js等无用标签
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_'),
               db.list_collection_names()))
    print(collections)
    for collection in collections:
        data = db[collection].find_one({'status_code':200}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url = data['url']
            # print(data)
            html=remove_css(data['html'])
            # print(url,html)
            print(url)
            db[collection].update_one({'url': url}, {'$set': {'html': html,'status_code':201}})
            # break
            data = db[collection].find_one({"_id": {"$gt": data["_id"]},'status_code':200})
        # break
def move_page_html_to_floder():
    # 移动数据库中的html代码到本地
    db = Test()._get_db()
    collections = list(
        filter(lambda x: x.startswith('pages_'),
               db.list_collection_names()))
    print(collections)
    for collection in collections:
        print(collection)
        data = db[collection].find_one({'status_code': 201}, sort=[("_id", pymongo.ASCENDING)])
        while data:
            url = data['url'].strip('\n').strip('\r').strip('\n').strip('\t')
            html = data['html']

            filepath=get_filepath_and_filename_by_url(url)
            print(url,filepath)
            with open(filepath,'w',encoding='utf-8') as f:
                f.write(html)

            db[collection].update_one({'url': url}, {'$set': {'html': '', 'status_code': 202}})
            data = db[collection].find_one({"_id": {"$gt": data["_id"]}, 'status_code': 201})
            # break
        # break

if __name__=="__main__":
    from Spider.models import *
    # delete_other_domain()
    # move_data_to_no_www()
    # remove_www_col()
    # filter_url_on_links_and_pages()
    # move_data_to_right_collection()
    # update_null_key()
    # compare_links_and_pages()
    # turn_huxiu_http_to_https()
    # get_page_by_url('https://www.huxiu.com/article/482133.html')
    # change_thepaper_no_www()
    # change_huxiu_no_www()
    # change_sohu_no_www()
    # print(clean_tags_of_link('https://www.huxiu.com/search.html?s=小鹏汽车'))
    # clean_huxiu_no_target()
    # clean_thepaper_no_target()
    # clean_all_pages_css_and_script()
    move_page_html_to_floder()
    pass

