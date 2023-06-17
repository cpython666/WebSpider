from Spider.models import *
from Spider.utils import *
from Spider.logs import *

def page_save(url,status_code=None,msg=None,html=None,timestamp=datetime.now(),title=None,content=None,abstract=None):
    try:
        Page(url=url,status_code=status_code,msg=msg,html=html,timestamp=timestamp,title=title,content=content,abstract=abstract).save()
        print(f'{url}请求成功，保存完毕')
    except:
        Page.objects(url=url).update(status_code=status_code, msg=msg, html=html, timestamp=timestamp, title=title, content=content, abstract=abstract)
        print(f'{url}请求成功，更新完毕')


def url_save(url,visited=None):
    try:
        Link(url=url, visited=visited).save()
    except:
        Link.objects(url=url).update(visited=visited)

def visited_url(url):
    Link.objects(url=url).update(visited=True)

def url_add(url):
    Link(url=url).save()



ll=[
    'http://www.people.com.cn/',
    'https://www.sina.com.cn/',
    'http://news.sohu.com/',
    'https://www.thepaper.cn/',
    'https://news.163.com/',
    'https://news.ifeng.com/'
]
def init_url(urls):
    for url in urls:
        try:
            url_add(url)
        except:
            Link.objects(url=url).update(visited=False)
init_url(ll)
while True:
    url_set = get_url_set()
    url_queue=get_no_visited_urls()
    for url in url_queue:
        sleep(choice(TIMES))
        print(url)
        try:
            html=get_page(url)

            visited_url(url)
            page_save(url=url,html=html,status_code=200)
            logging.info(f'{url}请求成功，保存完毕')
        except Exception as e:
            logging.info(f'{url}请求失败')
            print(f'{url}请求失败')
            visited_url(url)
            page_save(url=url,status_code=404,msg=str(e))

            continue

        new_urls=extract_links_from_url_and_html(url,html)

        for url in new_urls:
            if url not in url_set:
                url_save(url)
        url_set=url_set | set(new_urls)