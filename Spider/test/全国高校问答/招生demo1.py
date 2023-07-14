# -*- coding: utf-8 -*-
# # with open('1.txt','r',encoding='utf-8') as f:
# #     id_str=f.read()
# #
# # import re
# #
# # print(re.findall('id=(.*?)&', 'https://m-view.eol.cn/h5/zsgk/answer_noresult.html?t=1111'))
# # # print(re.findall('id=(.*?)&', id_str))
# import requests
#
# url_ = f'https://static-answer.eol.cn/html/www/data/question/992.json'
# r = requests.get(url=url_).json()
# print(r)
# # r = requests.get(url=url_, headers=get_headers()).json()
import json

# with open('output.json', 'r',encoding='utf-8') as f:
#     tmp=f.read()
#
# # 将 Python 对象转换为 JSON 字符串，保留汉字
# json_str = json.dumps(tmp, ensure_ascii=False)
# print(json_str)
with open('output.json', 'r') as file:
    data = json.load(file)
print(data)
with open('qa.json','w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False)