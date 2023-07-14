from enum import Enum

class AllowedDomains(Enum):
    # 搜索引擎
    # baidu = ('baidu.com',None)
    # bing = ('baidu.com',None)
    # 新闻类
    # 新浪 虎嗅 凤凰网 网易新闻,人民网，搜狐网
    xinlang=('sina.com.cn',None)
    xinlang_hainan=('hainan.sina.com.cn',None) #新浪海南

    huxiu=('huxiu.com',None)

    fenghuang=('news.ifeng.com',None)

    wangyi=('news.163.com',None)

    people=('people.com.cn',None)
    people_beijing=('bj.people.com.cn',None)

    souhu=('sohu.com',None)
    souhu_news=('news.sohu.com',None)
    souhu_sports=('sports.sohu.com',None)
    souhu_mil=('mil.sohu.com',None)
    souhu_learning=('learning.sohu.com',None)
    souhu_business=('business.sohu.com',None)
    souhu_yule=('yule.sohu.com',None)
    souhu_auto=('auto.sohu.com',None)
    souhu_it=('it.sohu.com',None)
    souhu_health=('health.sohu.com',None)
    souhu_cul=('cul.sohu.com',None)
    souhu_history=('history.sohu.com',None)

    pengpai=('thepaper.cn',None)
    # pengpai_h5=('h5.thepaper.cn',None)

    # 百科类
    # baidubaike = ('baike.baidu.com',None)
    # sougoubaike = ('baike.sogou.com',None)
    # 论坛类
    # zhihu = ('zhihu.com',None)
    # 技术类
    # csdn=('csdn.net',None)

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
    print(AllowedDomains.found_parser_by_domain('baidu.com').parser)