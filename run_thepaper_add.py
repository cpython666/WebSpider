from Spider.models import *
from Spider.utils import *
from Spider.logs import *
from Spider.config import *

def spider_url(url):
    html=''
    try:
        # if url.startswith('https://www.thepaper.cn/tag/'):
        #     raise Exception('话题栏目信息有限无意义,信息动态加载,不再爬取')

        html = get_page_selenium_thepaper(url)
        # html = get_page(url)
        html = remove_css(html)
        # write_page(text=html,file_name='1.html')
        if '澎湃' not in html:
            raise Exception('暂时被检测到')
        if url.startswith('https://www.thepaper.cn/'):
            html_clean = remove_thepaper_nodes(html)
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
    new_urls = filter_url_of_thepaper(new_urls)

    print(f'提取到以下链接{new_urls}')
    for url in new_urls:
        save_url(url)
    sleep(choice(TIMES))
# except Exception as e:
#     logging.error(str(e))
def domainSpider(domain=None):
    spider_time=time()
    while True:
        sleep(0.1)
        if time()-spider_time>60*50:
            break
        # try:
        urls = get_one_url(domain=domain)
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
    # 'https://www.huxiu.com/article/'

    # 'https://www.thepaper.cn/',
    # 'https://www.thepaper.cn/list_25462',
    # 'https://www.thepaper.cn/list_25488',
    # 'https://www.thepaper.cn/list_97924',
    # 'https://www.thepaper.cn/list_25489',
    # 'https://www.thepaper.cn/list_25490',
    # 'https://www.thepaper.cn/list_25423',
    # 'https://www.thepaper.cn/list_25427',
    # 'https://www.thepaper.cn/list_127425',
    # 'https://www.thepaper.cn/list_25422',
    # 'https://www.thepaper.cn/list_25429',
    # 'https://www.thepaper.cn/list_27234',
    # 'https://www.thepaper.cn/list_119445',
    # 'https://www.thepaper.cn/list_119447',
    # 'https://www.thepaper.cn/list_119446',
    # 'https://www.thepaper.cn/list_119448',
    # 'https://www.thepaper.cn/list_119449',
    # 'https://www.thepaper.cn/list_25446',
    # 'https://www.thepaper.cn/list_25445',
    # 'https://www.thepaper.cn/list_26915',
    # 'https://www.thepaper.cn/list_25456',
    # 'https://www.thepaper.cn/list_25444',
    # 'https://www.thepaper.cn/list_27224',
    # 'https://www.thepaper.cn/list_26525',
    # 'https://www.thepaper.cn/list_26878',
    # 'https://www.thepaper.cn/list_25457',
    # 'https://www.thepaper.cn/list_25574',
    # 'https://www.thepaper.cn/list_25455',
    # 'https://www.thepaper.cn/list_26937',
    # 'https://www.thepaper.cn/list_26937',
    # 'https://www.thepaper.cn/list_25450',
    # 'https://www.thepaper.cn/list_25482',
    # 'https://www.thepaper.cn/channel_119908',
    # 'https://www.thepaper.cn/channel_-21',
    # 'https://www.thepaper.cn/list_26173',
    # 'https://www.thepaper.cn/list_25942',
    # 'https://www.thepaper.cn/channel_25950',
    # 'https://www.thepaper.cn/channel_25950',
    # 'https://www.thepaper.cn/channel_122908',
    # '',
    # '',
    # '',
    # '',
    # '',
]
init(ll)

domainSpider(domain='thepaper.cn')