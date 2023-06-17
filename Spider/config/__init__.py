from Spider.config.AllowedDomains import AllowedDomains
from Spider.utils import *

allowed_domains = {d.value for d in AllowedDomains}
# print(allowed_domains)
# print('baike.sogou.com' in allowed_domains)

print(any('zhihu.com1' in i for i in allowed_domains))
TIMEOUT=3
TIMES=[i/10 for i in range(10,30,1)]