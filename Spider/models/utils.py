from Spider.models import Link
from Spider.models import Page
from datetime import datetime, timedelta
from Spider.models import *

def get_daily_count(x=8):
    '''
    查询每天页面爬取数量
    :param x: 近x天
    :return: 日期，数量 的二位列表
    '''
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    pipeline = [
        {"$match": {
            "timestamp": {
                "$gte": current_date - timedelta(days=x-1),
                "$lt": current_date + timedelta(days=1)
            }
        }},
        {"$group": {
            "_id": {
                "year": {"$year": "$timestamp"},
                "month": {"$month": "$timestamp"},
                "day": {"$dayOfMonth": "$timestamp"}
            },
            "count": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "year": "$_id.year",
            "month": "$_id.month",
            "day": "$_id.day",
            "count": 1
        }},
        {"$sort": {"year": 1, "month": 1, "day": 1}}
    ]
    result = list(Page.objects.aggregate(*pipeline))
    date_range = [(current_date - timedelta(days=i)).date() for i in range(x-1, -1, -1)]
    date_dict = {date: 0 for date in date_range}

    for entry in result:
        date = datetime(entry["year"], entry["month"], entry["day"]).date()
        count = entry["count"]
        date_dict[date] = count
    return [[str(date),cnt] for date,cnt in date_dict.items()]

def get_scuess_and_fail():
    pipeline = [
        {"$match": {"status_code": {"$in": [200, 404]}}},
        {"$group": {"_id": "$status_code", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "status_code": "$_id", "count": 1}}
    ]

    # 执行聚合查询
    result = Page.objects.aggregate(*pipeline)
    ans={
        404:0,
        200:0
    }

    # 获取查询结果
    for doc in result:
        ans[doc['status_code']]=doc['count']
    return ans

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

def get_no_visited_urls():
    links=Link.objects(visited=False)
    urls=[i.url for i in links]
    return urls

def get_url_set():
    links=Link.objects()
    return set([i.url for i in links])

def clean_no_visited_url():
    Link.objects(visited=False).delete()

def get_scuess_len():
    return len(Page.objects(status_code=200))

def get_page_by_regex():
    search_string = "example"
    results = Page.objects(url__regex=search_string)
    for doc in results:
        print(doc.url)

def get_page_count():
    pipeline = [
        {"$group": {"_id": None, "count": {"$sum": 1}}}
    ]
    return Page.objects.aggregate(*pipeline).next()['count']
def get_link_count():
    pipeline = [
        {"$group": {"_id": None, "count": {"$sum": 1}}}
    ]
    return Link.objects.aggregate(*pipeline).next()['count']

def get_detail_count():
    pipeline = [
        # {"$match": {"status_code":None}},
        {"$group": {"_id": None, "count": {"$sum": 1}}},
        # {"$project": {"_id": 0, "count": 1}}
    ]
    return Page.objects.aggregate(*pipeline).next()['count']

if __name__ == "__main__":
    print(get_page_count())
    # print(get_daily_count())
    # clean_no_visited_url()
    # print(get_scuess_len())
    # print(len(Page.objects(status_code=200)))
    # fillNone()
    # get_count()
    # get_domains()
    # print(get_scuess_and_fail())
    # print(39536 + 2072+29713)
    # 71321
    # 29713
    # Page.objects(status_code=None).update(set__status_code=200)