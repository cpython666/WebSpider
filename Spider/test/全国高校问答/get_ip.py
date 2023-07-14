import requests
from pprint import pprint
from Spider.utils import *
cur=0
url = f'http://webapi.http.zhimacangku.com/getip?num=22&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
r = requests.get(url, headers=get_headers()).text
r=r.split('\n')
r=[i.replace('\r','') for i in r]
ips=[i for i in r if i]
print(ips)
answer=[]
name=[]
for i in range(145):
    proxy=ips[cur%20]
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    url = f'https://api.eol.cn/web/api/?keyword=&page={i + 1}&province_id=&ranktype=&request_type=1&size=20&top_school_id=[436,589,459,3269,3117,434,1169,1159,435,457,1551,3374,3375]&type=&uri=apidata/api/gkv3/school/lists&signsafe=3503d1b58d5524822990435eb8f905ae'
    r = requests.get(url, headers=get_headers(),proxies=proxies).json()
    print(r)
    sleep(0.5)
    cur+=1
    data=r['data']['item']
    pprint(data)
    for _ in data:
        name.append(_['name'])
        answer.append(_['answerurl'])
    pprint(answer)

import json
with open('qa.json','w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False)
