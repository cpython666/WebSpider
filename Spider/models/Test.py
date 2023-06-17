from mongoengine import Document,StringField,BooleanField
# 链接表（Links）
from Spider.models import *
class Test(Document):

    url = StringField(required=True,unique=True)
    visited = BooleanField(default=True)
    a=StringField()
    meta = {
        'collection': 'tests',  # 指定集合名称,
        'indexes': [
            'visited',
        ]
    }
# Test(
#     url='521111',
#     visited=1,
#     a=None
#      ).save()

# print(len(Test.objects(a=None)))
Test.objects(
    url='21111'
).update(a=None)