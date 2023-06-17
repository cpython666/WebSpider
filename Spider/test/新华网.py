from Spider.utils import *

res=get_page("http://www.news.cn/")
write_page('新华网.html',res)
print(res)