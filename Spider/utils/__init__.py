from Spider.config import *

from time import sleep
from time import time
from datetime import datetime
from random import choice
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import chardet

from Spider.utils.chrome_driver import get_page_selenium_huxiu,get_page_selenium_thepaper,get_page_selenium
from Spider.utils.utils_links import \
    extract_links_from_url_and_html,\
    remove_css,\
    remove_huxiu_nodes,remove_thepaper_nodes,remove_sohu_nodes,remove_ifeng_nodes,\
    filter_url_of_huxiu,filter_url_of_thepaper,filter_url_of_sohu,filter_url_of_ifeng,\
    get_netloc,get_collection_name,get_my_db,\
    clean_tags_of_link
from Spider.utils.write_page import write_page
from Spider.utils.spider_utils import get_headers,get_page
from Spider.utils.url2filename import url2filename,filename2url,get_filepath_and_filename_by_url