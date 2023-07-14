from Spider.models import *
from Spider.utils import *
from Spider.logs import *
from Spider.config import *

def spider_url(url):
    html = ''
    try:
        html = get_page_selenium(url)
        html = remove_css(html)
        # write_page(text=html,file_name='1.html')
        if 'xinwendakao' in url:
            raise Exception('垃圾页面')
        if url.startswith('https://news.sohu.com/xtopic/'):
            raise Exception('垃圾页面')
        if '搜狐' not in html:
            raise Exception('暂时被检测到')
        if 'sohu.com' in url:
            html_clean = remove_sohu_nodes(html)
            save_page(url=url, html=html_clean, status_code=201)
        else:
            save_page(url=url, html=html, status_code=201)
        visited_url(url)
        print(f'{url}请求成功，保存完毕')
        logging.info(f'{url}请求成功，保存完毕')
    except Exception as e:
        logging.error(str(e))
        logging.info(f'{url}请求失败')
        print(f'{url}请求失败')
        visited_url(url)
        save_page(url=url, status_code=404, msg=str(e))
        # continue

    new_urls = extract_links_from_url_and_html(url, html)
    new_urls = filter_url_of_sohu(new_urls)

    print(f'提取到以下链接{new_urls}')
    for url in new_urls:
        save_url(url)
    sleep(choice(TIMES))

def domainSpider(domain=None):
    while True:
        urls = get_one_url(domain=domain)
        for url_obj in urls:
            url=url_obj['url']
            spider_url(url)

def init(urls):
    '''将链接加入数据库，如果已经加入，则将访问状态更新为未访问，以让程序提取最新的新闻链接'''
    for url in urls:
        spider_url(url)
ll=[
    # 'http://www.people.com.cn/',
    # 'https://www.sina.com.cn/',
    # 'https://news.sohu.com/',
    # 'https://www.thepaper.cn/',
    # 'https://news.163.com/',
    # 'https://news.ifeng.com/',
    # 'https://www.huxiu.com/',
    # 'https://www.huxiu.com/article/'

    'https://news.sohu.com/',
    'https://sohu.com/',
    'https://sports.sohu.com/',
    'https://learning.sohu.com/',
    'https://business.sohu.com/',
    'https://it.sohu.com/',
    'https://travel.sohu.com/',
    'https://yule.sohu.com/',

]
init(ll)

domainSpider(domain='sohu.com')
# domainSpider()