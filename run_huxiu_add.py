from Spider.models import *
from Spider.utils import *
from Spider.logs import *
from Spider.config import *

def spider_url(url):
    html=''
    try:
        if url.startswith('https://www.huxiu.com/member/'):
            raise Exception('个人主页无意义，不再爬取')
        html = get_page_selenium_huxiu(url)
        html = remove_css(html)
        # write_page(text=html,file_name='1.html')
        if '虎嗅' not in html:
            raise Exception('暂时被检测到')
        if url.startswith('https://www.huxiu.com/'):
            html_huxiu = remove_huxiu_nodes(html)
            save_page(url=url, html=html_huxiu, status_code=201)
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
    new_urls = filter_url_of_huxiu(new_urls)
    print(f'提取到以下链接{new_urls}')
    for url in new_urls:
        save_url(url)
    # break
    sleep(choice(TIMES))

def domainSpider(domain=None):
    spider_time=time()
    while True:
        sleep(0.1)
        if time()-spider_time>60*35:
            break
        # try:
        urls = get_one_url(domain=domain)
        print(urls)
        for url_obj in urls:
            url=url_obj['url']
            spider_url(url)
def init(urls):
    '''将链接加入数据库，如果已经加入，则将访问状态更新为未访问，以让程序提取最新的新闻链接'''
    for url in urls:
        spider_url(url)
        # init_url(url)
ll=[
    # 'http://www.people.com.cn/',
    # 'https://www.sina.com.cn/',
    # 'http://news.sohu.com/',
    # 'https://www.thepaper.cn/',
    # 'https://news.163.com/',
    # 'https://news.ifeng.com/',
    # 'https://www.huxiu.com/',
    # 'https://www.huxiu.com/article/1655141.html'

    # 虎嗅
    # 'https://www.huxiu.com/channel/4.html',
    # 'https://www.huxiu.com/channel/107.html',
    # 'https://www.huxiu.com/channel/112.html',
    # 'https://www.huxiu.com/channel/2.html',
    # 'https://www.huxiu.com/channel/110.html',
    # 'https://www.huxiu.com/channel/102.html',
    # 'https://www.huxiu.com/channel/114.html',
    # 'https://www.huxiu.com/channel/113.html',
    # 'https://www.huxiu.com/channel/111.html',
    # 'https://www.huxiu.com/channel/22.html',
    # 'https://www.huxiu.com/channel/115.html',
    # 'https://www.huxiu.com/channel/105.html',
    # 'https://www.huxiu.com/channel/21.html',
    # 'https://www.huxiu.com/article/',
]
init(ll)

try:
    domainSpider(domain='huxiu.com')
except:
    pass