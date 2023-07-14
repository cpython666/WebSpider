# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 14:30
# @Author  : wsh
# @File    : url2filename.py
import os
from Spider.utils import *
def url2filename(url):
    '''
    链接序列化函数，将非法字符转化为 __
    之所以转化为 __，是因为可以反序列化为链接
    先替换https______为https://，再替换__为/
    '''
    special_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for special_char in special_chars:
        url=url.replace(special_char,'--')
    return url
def filename2url(filename):
    return filename.replace('https------','https://').replace('--','/')

def get_filepath_and_filename_by_url(url):
    filename=url2filename(url)
    filepath=os.path.dirname(__file__)
    folder=get_netloc(url).replace('.','--')
    if not os.path.exists(os.path.join(filepath,'html')):
        os.mkdir(os.path.join(filepath,'html'))
    if not os.path.exists(os.path.join(filepath,'html',folder)):
        os.mkdir(os.path.join(filepath,'html',folder))
    # print(os.path.join(filepath, 'html', folder,filename))
    return os.path.join(filepath, 'html', folder,filename)+'.html'

if __name__ == '__main__':
    url='https://www.yucongming.com/book/1667549758731923458'
    filename=url2filename(url)
    url_=filename2url(filename)
    print(url)
    print(filename)
    print(url_)
    file=get_filepath_and_filename_by_url('https://www.yucongming.com/book/1667549758731923458')

    with open(file,'w',encoding='utf-8') as f:
        f.write("123")