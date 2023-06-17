from mongoengine import Document,StringField,BooleanField
# 链接表（Links）
class Link(Document):
    url = StringField(required=True,unique=True)
    visited = BooleanField(default=False)
    meta = {
        'collection': 'links',  # 指定集合名称,
        'indexes': [
            'visited',
        ]
    }