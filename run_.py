from Spider.models import *
from Spider.utils import *
from Spider.logs import *

def visited_url(url):
    Link.objects(url=url).update(visited=True)

def add_url(url):
    Link(url=url).save()

def save_page(url,html):
    Page(
        url=url,
        status_code=200,
        html=html,
        timestamp=datetime.now()
    ).save()

def update_page(url,html):
    Page.objects(
        url=url,
    ).update(
        status_code=200,
        html=html,
        timestamp=datetime.now()
    )

ll=[
    'http://www.people.com.cn/',
    'https://www.sina.com.cn/',
    'http://news.sohu.com/',
    'https://www.thepaper.cn/',
    'https://news.163.com/',
    'https://news.ifeng.com/'
]
for i in ll:
    try:
        add_url(i)
    except:
        print(f'{i}已添加~')
        Link.objects(url=i).update(visited=False)
while True:
    try:
        url_set = get_url_set()
        url_queue=get_no_visited_urls()
        for url in url_queue:
            print(url)
            try:
                html=get_page(url)
                visited_url(url)
                try:
                    save_page(url=url,html=html)
                except:
                    update_page(url=url,html=html)
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
                continue

            new_urls=extract_links_from_url_and_html(url,html)

            for _ in new_urls:
                if _ not in url_set:
                    add_url(_)
            url_set=url_set | set(new_urls)

    except Exception as e:
        pass
    finally:
        sleep(choice(TIMES))