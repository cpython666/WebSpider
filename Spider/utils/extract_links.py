import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from Spider.config import *

allowed_extensions = ['.html', '.htm']

def filter_links(links, allowed_extensions):
    filtered_links = []
    for link in links:
        if any(link.endswith(ext) for ext in allowed_extensions):
            filtered_links.append(link)
    return filtered_links

def extract_links_from_url_and_html(url,page):
    soup = BeautifulSoup(page, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href!='javascript:;' and not href.endswith('.jpg') and not href.endswith('.png'):
            parsed_url = urlparse(href)
            if parsed_url.scheme == '' and parsed_url.netloc == '':
                # 相对链接，拼接成绝对链接
                absolute_url = urlparse(url)
                href = absolute_url.scheme + '://' + absolute_url.netloc + href
            if any(i in href for i in allowed_domains):
                links.append(href)
    return links

if __name__=="__main__":
    with open("虎嗅主页.html",'r',encoding='utf-8') as f:
        html_content=f.read()
    links = extract_links_from_url_and_html('http://baidu.com/1.html',html_content)
    print(links)