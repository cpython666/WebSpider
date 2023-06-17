text = "要写入的文本"
# 以写入模式打开文件
with open("https://english.news.cn/home.htm", "w", encoding='utf-8') as f:
    f.write(text)