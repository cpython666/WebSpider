from Spider.utils import *
import json

cur=0
url = f'http://webapi.http.zhimacangku.com/getip?num=55&type=1&pro=&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
r = requests.get(url, headers=get_headers()).text
r=r.split('\n')
r=[i.replace('\r','') for i in r]
ips=[i for i in r if i]
print(ips)
with open('output.json', 'r',encoding='utf-8') as file:
    obj_list = json.load(file)
print(obj_list)
# for i in obj_list:
#     print(i['id'])
for obj in obj_list:
    url_=f'https://static-answer.eol.cn/html/www/data/question/{obj["id"]}.json'
    print(url_)
    r=requests.get(url=url_,headers=get_headers()).json()
    qa=r['item']
    obj['qa']=qa
    print(obj_list.index(obj))

    sleep(0.1)
    cur+=1

with open('qa.json','w',encoding='utf-8') as f:
    json.dump(obj_list,f,ensure_ascii=False)
