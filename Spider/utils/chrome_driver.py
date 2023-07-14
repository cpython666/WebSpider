from Spider.utils import *
from selenium import webdriver
import os
try:
    current_path = os.path.dirname(os.path.abspath(__file__))
    driver = webdriver.Chrome(executable_path=os.path.join(current_path,'chromedriver.exe'))

    with open(os.path.join(current_path,'stealth.min.js')) as f:
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
except:
    print('chromedriver未成功初始化~')

def get_page_selenium_huxiu(url):
    driver.get(url)
    sleep(1.5)
    while True:
        if url.startswith('https://www.huxiu.com/article/') and url.endswith('.html'):
            break
        page=driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        if page==driver.page_source:
            break
    return driver.page_source
def get_page_selenium_thepaper(url):
    driver.get(url)
    sleep(1)
    while True:
        # if url.startswith('https://www.huxiu.com/article/') and url.endswith('.html'):
        #     break
        page=driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        if page==driver.page_source:
            break
    return driver.page_source

def get_page_selenium(url):
    driver.get(url)
    sleep(1)
    while True:
        # if url.startswith('https://www.huxiu.com/article/') and url.endswith('.html'):
        #     break
        page=driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        if page==driver.page_source:
            break
    return driver.page_source
if __name__ == '__main__':
    import time
    # time.sleep(50)
    get_page_selenium_huxiu('https://www.huxiu.com/article/')