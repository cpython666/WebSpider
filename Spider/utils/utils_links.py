# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup,Comment
from urllib.parse import urlparse
from Spider.config import not_allowed_suffix,allowed_domains

def get_netloc(url):
    ans=urlparse(url).netloc.strip('.').replace('www.','')
    if 'sohu.com' in ans:
        return 'sohu.com'
    return ans
def get_collection_name(url,type='link'):
    return f'{type}s_{get_netloc(url)}'
def get_my_db():
    pass
def clean_tags_of_link(link):
    # link = "https://example.com/page.html?key=value#section"
    # 找到第一个 "#" 或 "?" 的索引
    x,y=link.find("#"),link.find("?")
    x=x if x!=-1 else 100000
    y=y if y!=-1 else 100000
    index_=min(x,y)
    # 切片字符串
    return link[:index_]

def check_url(url,href):
    # href不为空,不等于javascript,并且后缀名合要求
    if href and href != 'javascript:;' and not any(href.endswith(i) for i in not_allowed_suffix):
        try:
            parsed_url = urlparse(href)
        except:
            return False
        if href.startswith('//'):
            href = href.strip('/')
            href = href.strip(':')
        if parsed_url.scheme == '' and parsed_url.netloc == '':
            absolute_url = urlparse(url)
            href = absolute_url.scheme + '://' + absolute_url.netloc + href
        # href已经改变,需重新解析
        parsed_url = urlparse(href).netloc.strip('.').replace('www.', '')
        href=href.strip('#').strip('/').strip('#')

        href=clean_tags_of_link(href)

        if any(parsed_url == i for i in allowed_domains):
            return href
        return False
import re
def filter_url_of_huxiu(urls):
    member_url=list(filter(lambda i:i.startswith('https://www.huxiu.com/member/'),urls))
    url_text=','.join(member_url)
    ids=set(i.replace('/comment','') for i in re.findall('https://www.huxiu.com/member/(.*?).html',url_text))
    for id in ids:
        with open('huxiu_ids.txt','a',encoding='utf-8') as f:
            f.write(id+'\n')

    return list(filter(lambda i:not i.startswith('https://www.huxiu.com/member/')
                        and not i.startswith('https://www.huxiu.com/zttype/')
                        and not i.startswith('https://www.huxiu.com/ztcontents/')
                        and not i.startswith('https://www.huxiu.com/zhuanti/')
                        and not i.startswith('https://www.huxiu.com/wow')
                        and not i.startswith('https://www.huxiu.com/v')
                        and not i.startswith('https://www.huxiu.com/u')
                        and not i.startswith('https://www.huxiu.com/t')
                        and not i.startswith('https://www.huxiu.com/s')
                        and not i.startswith('https://www.huxiu.com/r')
                        and not i.startswith('https://www.huxiu.com/p')
                        and not i.startswith('https://www.huxiu.com/m')
                        and not i.startswith('https://www.huxiu.com/r')
                        and not i.startswith('https://www.huxiu.com/active/')

                        and i.startswith('https://www.huxiu.com/')
                       ,urls))

def filter_url_of_thepaper(urls):
    return list(filter(lambda i:not i.startswith('https://www.thepaper.cn/tag/')
                                and not i.startswith('https://www.thepaper.cn/user_')
                                and not i.startswith('https://www.thepaper.cn/asktopic_detail_')
                                and not i.startswith('https://www.thepaper.cn/ask_index')
                                and not i.startswith('https://www.thepaper.cn/gov_')
                                and not i.startswith('https://www.thepaper.cn/list_')

                                and i.startswith('https://www.thepaper.cn/')
                       ,urls))

def filter_url_of_sohu(urls):
    urls=[i.replace('http://','https://') for i in urls]
    urls=[i.replace('https://sohu.com/','https://www.sohu.com/') for i in urls]
    return list(filter(lambda i:'xinwendakao' not in i
                       and not i.startswith('https://news.sohu.com/xtopic/')
                       ,urls))
def filter_url_of_ifeng(urls):
    urls=[i.replace('http://','https://') for i in urls]
    # urls=[i.replace('https://sohu.com/','https://www.sohu.com/') for i in urls]
    return list(filter(lambda i:True,urls))
def extract_links_from_url_and_html(url,page):
    soup = BeautifulSoup(page, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        href=check_url(url=url,href=href)
        if href:
            links.append(href)
    return links

def remove_css(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.text)
    # 删除<style>标签
    for style_tag in soup('style'):
        style_tag.decompose()
    # 删除<link>标签
    for link_tag in soup('link'):
        link_tag.decompose()
    # 删除<symbol>标签
    for symbol_tag in soup('symbol'):
        symbol_tag.decompose()
    # 删除<script>标签
    for script_tag in soup('script'):
        script_tag.decompose()
    # 删除<svg>标签
    for script_tag in soup('svg'):
        script_tag.decompose()
    # 删除注释
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return str(soup)

def remove_huxiu_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes_to_remove = soup.select(
        # 头部栏,转载解释,转载解释app,相关推荐
        '#header-nav,.article__reprinted-explain,.article__reprinted-explain-app,.article__related-article-wrap,.default-footer')
    # 删除节点
    for node in nodes_to_remove:
        node.decompose()
    return str(soup)

def remove_thepaper_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes_to_remove = soup.select(
        # 头部栏,转载解释,转载解释app,相关推荐
        '.index_headerfixed__GyBYK,.index_content___Uhtm')
    # 删除节点
    for node in nodes_to_remove:
        node.decompose()
    return str(soup)
def remove_sohu_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes_to_remove = soup.select(
        # 头部栏,转载解释,转载解释app,相关推荐
        # news.sohu
        '#foot,#channelNav,#main-header,.review,#r_col,sohufootercode,#logo_nav,.location,.mutualityNEW,#indexNav')
    # 删除节点
    for node in nodes_to_remove:
        node.decompose()
    return str(soup)
def remove_ifeng_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes_to_remove = soup.select(
        # 头部栏,转载解释,转载解释app,相关推荐
        # news.sohu
        '.index_title_9X1oe,.index_list_box_TLUw-,.index_rightContent_Caqe0')
    # 删除节点
    for node in nodes_to_remove:
        node.decompose()
    return str(soup)
if __name__=="__main__":
    # with open("虎嗅主页.html",'r',encoding='utf-8') as f:
    #     html_content=f.read()
    # links = extract_links_from_url_and_html('http://baidu.com/1.html',html_content)
    # print(links)
    # print(check_url('https://games.sina.com.cn/wm/2022-12-07/detail-i-imqqsmrp8808884.shtml'))
    # print(urlparse('http://www.thepaper.cn/user_6386935').netloc)
    # print(urlparse('http://www.thepaper.cn/user_6386935').scheme)
    a='''
    <!DOCTYPE html>
        <html>
        <head>
            <title>HTML示例</title>
            <style>
                body {
                    background-color: #f5f5f5;
                }
                h1 {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>这是一个标题</h1>
            <p>这是一个段落。</p>
            <script>
                alert("这是一个 JavaScript 弹窗。");
            </script>
            <svg></svg>
                    <!-- 123 -->
                    <div class="a b" style="display:;"></div>
                    <div data-v-009474f2="" class="a b"><div class="article__reprinted-explain" style="display:;" data-v-009474f2="">本内容为作者独立观点，不代表虎嗅立场。未经允许不得转载，授权事宜请联系hezuo@huxiu.com<br>如对本稿件有异议或投诉，请联系tougao@huxiu.com</div><div class="article__reprinted-explain-app" style="display:;" data-v-009474f2="">正在改变与想要改变世界的人，都在<a class="download_a" href="https://www.huxiu.com/app.html" target="_blank"> 虎嗅APP<span class="download-i"></span></a></div></div>
                    <div class="article__related-article-wrap" data-v-009474f2=""><div data-v-5a46c1b0="" data-v-009474f2="" class="related-article"><h3 data-v-5a46c1b0="">相关推荐</h3><div data-v-5a46c1b0="" style="position: relative;"><div data-v-5a46c1b0="" class="related-article__info swiper-container swiper-container-initialized swiper-container-horizontal"><ul data-v-5a46c1b0="" class="related-article__info__ul swiper-wrapper" style="transform: translate3d(0px, 0px, 0px);"><li data-v-5a46c1b0="" class="swiper-slide swiper-slide-active" style="width: 788px; margin-right: 20px;"><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:486624,&quot;subscribe&quot;:1}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/486624.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202112/31/083108282076.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202112/31/083108282076.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">专访齐泽克：西方迫切需要一场真正的觉醒</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:409613,&quot;subscribe&quot;:2}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/409613.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202102/13/182118359251.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" src="https://img.huxiucdn.com/article/cover/202102/13/182118359251.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" lazy="loaded"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">中外抗疫一周年对比：孰优孰劣？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:355336,&quot;subscribe&quot;:3}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/355336.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/201801/03/182514607848.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/201801/03/182514607848.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">专访弗朗西斯·福山：全球危机远远大于机遇</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:391886,&quot;subscribe&quot;:4}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/391886.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202011/05/180230054795.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202011/05/180230054795.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">美国今日的疯狂，60年前就已上演</div></a></div></li><li data-v-5a46c1b0="" class="swiper-slide swiper-slide-next" style="width: 788px; margin-right: 20px;"><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:351606,&quot;subscribe&quot;:1}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/351606.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202004/20/213554695019.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202004/20/213554695019.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">福山：新自由主义已死，但中国模式难以复制</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:1670159,&quot;subscribe&quot;:2}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/1670159.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202306/12/101759653463.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202306/12/101759653463.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">“AGI政治家”奥特曼？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:348586,&quot;subscribe&quot;:3}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/348586.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/201911/27/092655559230.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/201911/27/092655559230.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">新冠病毒全球大流行，我们缺乏的只是疫苗？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:559053,&quot;subscribe&quot;:4}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/559053.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202205/19/103151637596.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202205/19/103151637596.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">过去10年美国人的生活为何如此愚蠢？</div></a></div></li><li data-v-5a46c1b0="" class="swiper-slide" style="width: 788px; margin-right: 20px;"><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:724303,&quot;subscribe&quot;:1}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/724303.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202211/25/022634815841.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="https://img.huxiucdn.com/article/cover/202211/25/022634815841.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" lazy="loaded"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">国际政客接连遇刺，暗杀越来越流行了吗？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:350858,&quot;subscribe&quot;:2}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/350858.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202004/16/164138570268.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">周轶君：我们可能无法打败“三体人”了</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:343967,&quot;subscribe&quot;:3}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/343967.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202003/11/100040829295.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><!----></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">“3·11”日本大地震九周年：它改变了日本什么？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:348089,&quot;subscribe&quot;:4}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/348089.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202004/02/185835232476.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">新冠肺炎是如何攻陷全世界的？</div></a></div></li><li data-v-5a46c1b0="" class="swiper-slide" style="width: 788px; margin-right: 20px;"><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:346913,&quot;subscribe&quot;:1}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/346913.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/201908/22/074239569193.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">美国抗疫靠“甩锅”，我们怎么办？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:373984,&quot;subscribe&quot;:2}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/373984.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202008/07/162919978008.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">频频刁难中国为哪番？深扒历届美国总统为连任使出的“国际策略”</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:372612,&quot;subscribe&quot;:3}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/372612.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202007/31/184517279464.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">为了连任不顾人命，众叛亲离的川普要凉了？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:469320,&quot;subscribe&quot;:4}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/469320.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202111/03/145219118295.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">美国文化霸权，如何一步步渗透到全世界？</div></a></div></li><li data-v-5a46c1b0="" class="swiper-slide" style="width: 788px; margin-right: 20px;"><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:405930,&quot;subscribe&quot;:1}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/405930.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202101/22/125231344727.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">后疫情时代世界经济格局如何变幻？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:399544,&quot;subscribe&quot;:2}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/399544.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202012/12/130517882579.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">醒醒吧，人家从来就不是咱们的“好朋友”</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:465827,&quot;subscribe&quot;:3}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/465827.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202110/21/173239464028.png?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/png" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">中国为何能顽强崛起？</div></a></div><div data-v-5a46c1b0="" event-track-params="{&quot;customize&quot;:{&quot;page_position&quot;:&quot;相关推荐&quot;,&quot;aid&quot;:807455,&quot;subscribe&quot;:4}}" class="slide-list"><a data-v-164c51d1="" data-v-5a46c1b0="" href="/article/807455.html" target="_self" class="related-article__content"><div data-v-164c51d1="" class="related-article-pic"><img data-v-164c51d1="" data-src="https://img.huxiucdn.com/article/cover/202303/01/101050479937.jpg?imageView2/1/w/250/h/141/|imageMogr2/strip/interlace/1/quality/85/format/jpg" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" lazy="loading"><div data-v-164c51d1="" class="icon-flag-wrap"><svg data-v-1e778ed0="" data-v-164c51d1="" aria-hidden="true" class="hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-play"></use></svg></div></div><div data-v-164c51d1="" class="related-article-info multi-line-overflow">刘慈欣34年前的第一部小说，到底藏了怎样的秘密？</div></a></div></li></ul><span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span></div><div data-v-5a46c1b0=""><div data-v-5a46c1b0="" class="arrow-wrap arrow-left middle-center swiper-button-prev swiper-button-disabled" tabindex="0" role="button" aria-label="Previous slide" aria-disabled="true" style="display: none;"><svg data-v-1e778ed0="" data-v-5a46c1b0="" aria-hidden="true" class="arrow hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-arrow-left"></use></svg></div><div data-v-5a46c1b0="" class="arrow-wrap arrow-right middle-center swiper-button-next" tabindex="0" role="button" aria-label="Next slide" aria-disabled="false"><svg data-v-1e778ed0="" data-v-5a46c1b0="" aria-hidden="true" class="arrow hx-icon"><use data-v-1e778ed0="" xlink:href="#icon-arrow-right"></use></svg></div></div></div></div></div>
        </body>
        </html>
    '''
    # a=remove_huxiu_nodes(a)
    # soup = BeautifulSoup(a, 'html.parser')
    # print(soup('svg'))
    # print(a)