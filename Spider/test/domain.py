from enum import Enum

class Domain(Enum):
    GOOGLE = ('google.com', None)
    FACEBOOK = ('facebook.com', None)
    TWITTER = ('twitter.com', 'TwitterParser')

    def __new__(cls, domain, parser):
        obj = object.__new__(cls)
        obj._value_ = domain
        obj.parser = parser
        return obj

# 使用示例
print(Domain.GOOGLE)  # 输出: Domain.GOOGLE
print(Domain.GOOGLE.value)  # 输出: ('google.com', GoogleParser)
print(Domain.GOOGLE.parser)  # 输出: GoogleParser
