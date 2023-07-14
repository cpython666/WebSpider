from Spider.models import *
from Spider.utils import *
from Spider.logs import *
from Spider.config import *

def domainSpider(domain=None):
    while True:
        # try:
        urls = get_one_url(domain=domain)
        for url_obj in urls:
            url=url_obj['url']
            try:
                html = get_page(url)
                html=remove_css(html)
                # write_page(text=html,file_name='1.html')
                visited_url(url)
                save_page(url=url, html=html, status_code=201)
                print(f'{url}请求成功，保存完毕')
                logging.info(f'{url}请求成功，保存完毕')
            except Exception as e:
                logging.error(str(e))
                logging.info(f'{url}请求失败')
                print(f'{url}请求失败')
                visited_url(url)
                save_page(url=url, status_code=404, msg=str(e))
                continue

            new_urls = extract_links_from_url_and_html(url, html)
            print(f'提取到以下链接{new_urls}')
            for url in new_urls:
                save_url(url)
            sleep(choice(TIMES))

        # except Exception as e:
        #     logging.error(str(e))
def init(urls):
    '''将链接加入数据库，如果已经加入，则将访问状态更新为未访问，以让程序提取最新的新闻链接'''
    for url in urls:
        init_url(url)
ll=[
    # 'http://www.people.com.cn/',
    # 'https://www.sina.com.cn/',
    # 'http://news.sohu.com/',
    # 'https://www.thepaper.cn/',
    # 'https://news.163.com/',
    # 'https://news.ifeng.com/',
    # 'https://www.huxiu.com/',
]
init(ll)

# import threading
# for i in range(len(ll)):
#     domain=get_netloc(ll[i])
#     thread = threading.Thread(target=domainSpider, args=(domain,))
#     thread.start()

domainSpider(domain='news.sohu.com')
# domainSpider(domain='thepaper.cn')
# domainSpider(domain='huxiu.com')
# domainSpider()