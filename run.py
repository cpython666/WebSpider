from Spider.models import *
from Spider.utils import *
from Spider.logs import *

def visited_url(url):
    '''
    请求成功后更新该值
    :return:
    '''
    Link.objects(url=url).update(visited=True)

def add_url(url):
    '''
    队列添加，数据库添加
    '''
    Link(url=url).save()

try:
    add_url('https://www.huxiu.com/')
except:
    pass
while True:
    try:
        url_set = get_url_set()
        url_queue=get_no_visited_urls()
        for url in url_queue:
            print(url)
            try:
                html=get_page(url)
                visited_url(url)
                Page(
                    url=url,
                    status_code=200,
                    html=html,
                    timestamp=datetime.now()
                ).save()
                logging.info(f'{url}请求成功，保存完毕')
                print(f'{url}请求成功，保存完毕')
            except Exception as e:
                logging.info(f'{url}请求失败')
                print(f'{url}请求失败')
                visited_url(url)
                Page(
                    url=url,
                    status_code=404,
                    msg=str(e),
                    timestamp=datetime.now()
                ).save()
                Link(
                    url = url
                ).save()
                continue
            new_urls=extract_links_from_url_and_html(url,html)
            # print(new_urls)
            for _ in new_urls:
                if _ not in url_set:
                    add_url(_)
            url_set=url_set | set(new_urls)

    except Exception as e:
        pass
    finally:
        sleep(choice(TIMES))