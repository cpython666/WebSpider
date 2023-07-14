from random import choice

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    ]

def get_headers():
    return {"user-agent": choice(UserAgents)}

from Spider.config import *
from Spider.utils import *

import chardet
import requests
def get_page(url):
    r=requests.get(url,headers=get_headers())
    if r.status_code == 200:
        try:
            encoding=chardet.detect(r.content)["encoding"]
            if encoding.lower() == "gb2312":
                html= r.content.decode('gb18030')
            else:
                html= r.content.decode(encoding)
        except:
            html= r.text
        return remove_css(html)
    else:
        raise Exception(f"请求失败{r.text}")

if __name__=="__main__":
    # get_page('http://www.cs.com.cn/')
    # print(get_page('https://news.163.com/'))
    print(get_page('https://www.huxiu.com/'))