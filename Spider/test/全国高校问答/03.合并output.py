import json

with open('output1.json', 'r',encoding='utf-8') as file:
    data1 = json.load(file)

with open('output_err.json', 'r',encoding='utf-8') as file:
    data2 = json.load(file)

print(len(data1))
print(len(data2))
data=data1+data2
print(len(data))

print(data)
with open('output.json','w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False)