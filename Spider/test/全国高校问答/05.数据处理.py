import json

with open('qa.json', 'r',encoding='utf-8') as file:
    obj_list = json.load(file)

from pprint import pprint
pprint(len(obj_list))
# pprint(obj_list[0])
pprint(obj_list[0].keys())
pprint(len(obj_list[0]['qa']))
count=0
import re
f=open('qa_.txt','a',encoding='utf-8')
for obj in obj_list:
    name=obj['name']
    count+=len(obj['qa'])
    for qa in obj['qa']:
        q = qa['question'].replace('\n', '')
        a = re.sub(r'<.*?>', '',qa['answer'].replace('\n', ''))
        if any(i in q for i in ['贵校','学校','你们学校']):
            q=q.replace('贵校',name).replace('学校',name).replace('你们学校',name)
        else:
            q=name+q
        q = '问:' + q
        a = '答:' +a
        f.write(q + ' '+a)
        f.write('\n')
        f.write('\n')
print(count)