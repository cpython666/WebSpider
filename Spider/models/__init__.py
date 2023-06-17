from mongoengine import connect
from Spider.models.Links import Link
from Spider.models.Pages import Page
from Spider.models.utils import *
connect(db='Spider',
        # username='root',
        # password='1234',
        host='localhost',
        port=27017,
        # authSource='root'
        )