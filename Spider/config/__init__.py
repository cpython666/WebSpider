from Spider.config.AllowedDomains import AllowedDomains
from Spider.config.NotAllowedSuffix import not_allowed_suffix

allowed_domains = {d.value for d in AllowedDomains}
# print(any('zhihu.com1' in i for i in allowed_domains))

TIMEOUT=3
TIMES=[i/5 for i in range(10,15,1)]