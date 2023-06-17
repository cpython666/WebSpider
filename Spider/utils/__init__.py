from Spider.utils.extract_links import extract_links_from_url_and_html
from Spider.utils.write_page import write_page

from Spider.utils.spider_utils import get_headers,get_netloc,get_page

from Spider.config import *

from time import sleep
from time import time
from datetime import datetime
from random import choice
from pprint import pprint

from bs4 import BeautifulSoup
import requests

import chardet