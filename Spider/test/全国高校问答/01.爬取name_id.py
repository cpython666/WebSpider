# -*- coding: utf-8 -*-
import requests
from pprint import pprint
from Spider.utils import *
cur=0
url = f'http://webapi.http.zhimacangku.com/getip?num=55&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
r = requests.get(url, headers=get_headers()).text
r=r.split('\n')
r=[i.replace('\r','') for i in r]
ips=[i for i in r if i]
print(ips)

answer=[]
name=[]
error=[]
for i in range(145):
    try:

        proxy=ips[cur%50]
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
        url=f'https://api.eol.cn/web/api/?keyword=&page={i+1}&province_id=&ranktype=&request_type=1&size=20&top_school_id=[436,589,459,3269,3117,434,1169,1159,435,457,1551,3374,3375]&type=&uri=apidata/api/gkv3/school/lists&signsafe=3503d1b58d5524822990435eb8f905ae'
        r=requests.get(url,headers=get_headers(),proxies=proxies).json()

        data=r['data']['item']
        pprint(data)
        for _ in data:
            name.append(_['name'])
            answer.append(_['answerurl'])
        pprint(answer)
        cur+=1
        print(i)

        sleep(0.2)
    except:
        error.append(i)
# id_str='\n'.join(answer)
# with open('1.txt','w',encoding='utf-8') as f:
#     f.write(id_str)

obj_list=[]
import re
for i in range(len(answer)):
    id_list=re.findall('id=(.*?)&',answer[i])
    if id_list:
        obj_list.append({
            'name':name[i],
            'id':id_list[0]
        })
import json
json_str = json.dumps(obj_list)
with open('output1.json', 'w',encoding='utf-8') as f:
    f.write(json_str)
print(error)

