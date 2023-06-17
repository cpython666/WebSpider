from enum import Enum

class AllowedDomains(Enum):
    # 搜索引擎
    baidu = ('baidu.com',None,)
    bing = ('baidu.com',None)
    # 新闻类
    # 新浪 虎嗅 凤凰网 网易新闻,人民网，搜狐网
    xinlang=('sina.com.cn',None)
    huxiu=('huxiu.com',None)
    fenghuang=('news.ifeng.com',None)
    wangyi=('news.163.com',None)
    people=('people.com.cn',None)
    souhu=('news.sohu.com',None)
    pengpai=('thepaper.cn',None)

    # 百科类
    baidubaike = ('baike.baidu.com',None)
    sougoubaike = ('baike.sogou.com',None)
    # 论坛类
    zhihu = ('zhihu.com',None)
    # 技术类
    csdn=('csdn.net',None)

    def __new__(cls, domain, parser):
        obj = object.__new__(cls)
        obj._value_ = domain
        obj.parser = parser
        return obj

    @classmethod
    def found_parser_by_domain(cls,domain):
        found_member = None
        for member in cls.__members__.values():
            if member.value == domain:
                found_member = member
                break
        return found_member

if __name__ == '__main__':
    print(AllowedDomains.found_parser_by_domain('baidu.com'))