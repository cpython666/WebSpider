from mongoengine import connect
connect(db='Spider',
        # username='root',
        # password='1234',
        host='localhost',
        port=27017,
        # authSource='root'
        )

from Spider.models.Links import Link
from Spider.models.Pages import Page
from Spider.models.utils import *