from Spider.config import *
from Spider.utils import *
import chardet
import requests
def get_page(url):
    r=requests.get(url,headers=get_headers(),timeout=TIMEOUT)
    if r.status_code == 200:
        r = r.content.decode(chardet.detect(r.content)["encoding"])
        return r
    else:
        raise Exception(f"请求失败{r.text}")

if __name__=="__main__":
    get_page('http://www.cs.com.cn/')