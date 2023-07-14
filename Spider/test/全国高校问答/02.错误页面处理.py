from Spider.utils import *
import requests
name=[]
answer=[]
err=[92, 139, 140]
for i in err:
    url = f'https://api.eol.cn/web/api/?keyword=&page={i + 1}&province_id=&ranktype=&request_type=1&size=20&top_school_id=[436,589,459,3269,3117,434,1169,1159,435,457,1551,3374,3375]&type=&uri=apidata/api/gkv3/school/lists&signsafe=3503d1b58d5524822990435eb8f905ae'
    r = requests.get(url, headers=get_headers()).json()
    data = r['data']['item']
    pprint(data)
    for _ in data:
        name.append(_['name'])
        answer.append(_['answerurl'])
print(name)
print(answer)
import json
obj_list=[]
import re
for i in range(len(name)):
    id_list=re.findall('id=(.*?)&',answer[i])
    if id_list:
        obj_list.append({
            'name':name[i],
            'id':id_list[0]
        })
print(obj_list)
with open('output_err.json', 'w',encoding='utf-8') as f:
    json.dump(obj_list,f,ensure_ascii=False)