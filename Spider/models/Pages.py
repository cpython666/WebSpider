from mongoengine import Document,StringField,DateTimeField,EmailField,IntField
from datetime import datetime
# 网页表（Pages）
class Page(Document):
    url = StringField(required=True,unique=True)
    status_code=IntField()
    msg=StringField()
    html = StringField()
    timestamp = DateTimeField(default=datetime.now)
    title=StringField()
    content=StringField()
    abstract=StringField()

    meta = {
        'collection': 'pages',  # 指定集合名称
        'indexes': [
            'url',
            'status_code',
            'timestamp',
        ]
    }