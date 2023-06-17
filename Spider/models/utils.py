from Spider.models import Link
from Spider.models import Page

def get_no_visited_urls():
    links=Link.objects(visited=False)
    urls=[i.url for i in links]
    return urls

def get_url_set():
    links=Link.objects()
    return set([i.url for i in links])

if __name__ == "__main__":
    # print(get_no_visited_urls())
    # print(get_no_visited_urls())
    l=Page.objects(url='https://german.news.cn20230605/da9d0fed4b594b63b63b6d1a14242bff/c.html')
    # l=Page.objects(status_code=404)
    print(l.to_json())
    print(Link.objects(url='https://german.news.cn20230605/da9d0fed4b594b63b63b6d1a14242bff/c.html').to_json())
