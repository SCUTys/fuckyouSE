# coding=utf-8
import os

import pymongo, time, random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote

MONGO_URL = 'localhost'
MONGO_DB = 'test'
MONGO_COLLECTION = 'huawei'
KEYWORD = '华为P50'
MAX_PAGE = 1
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# turn the keyword into url code
KEYWORD = quote(KEYWORD)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--user-data-dir=Default')
browser = webdriver.Chrome()
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

wait = WebDriverWait(browser, 30)


def slide_down(second):
    for i in range(int(second / 0.1)):
        js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
        browser.execute_script(js)
        time.sleep(random.uniform(0.2, 0.4))
    time.sleep(0.2)


def get_page(page):
    print('正在爬取第', page, '页')
    try:
        # url = 'https://shopsearch.taobao.com/search?q=' + quote(KEYWORD)
        url = f'https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&q={KEYWORD}&search_type=item&sourceId=tb.index&spm=a21bo.jianhua%2Fa.201856.d13&ssid=s5-e&tab=all'
        print(url)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#pageContent div.next-pagination-pages > input')))
            submit = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#pageContent div.next-pagination-pages > span.next-btn-helper')))
            slide_down(2.1)
            input.clear()
            input.send_keys(page)
            submit.click()
            time.sleep(random.uniform(1, 2))
        # <button aria-label="第1页，共100页" type="button" class="next-btn next-medium next-btn-normal next-pagination-item next-current"><span class="next-btn-helper" data-spm-anchor-id="a21n57.1.0.i6.361c523cabVn3n">1</span></button>
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     '#pageContent div.next-pagination-list > button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-current > span.next-btn-helper'),
                                                    str(page)))
        slide_down(2.1)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#list-container .list-item .item-bottom')))
        # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#list-container .list-item .list-info .info-sum'),'件宝贝'))
        time.sleep(random.uniform(1, 2))
        get_shops(page)
    except TimeoutException:
        print('遇到验证码，需要休息下！')
        time.sleep(15)
        get_page(page)


def get_shops(page):
    # html = browser.page_source
    # doc = pq(html)
    #
    # items = doc('#list-container .list-item').items()
    # for item in items:
    #     shop = {
    #         'shoptitle': item.find('h4 a').text(),  #店铺名称
    #         'shopimg': item.find('.list-img a img').attr('src'),  #店铺图片
    #         'seller': item.find('.shop-info-list a').text(),  #卖家名称
    #         'sales': item.find('.info-sale em').text(),  #销量
    #         'products': item.find('.info-sum em').text(),  #宝贝数量
    #         'goodcomt': item.find('.good-comt').text(),  #好评率
    #     'main' : item.find('.main-cat a').text(), # 主营
    #     'link' : item.find('.list-img a').attr('href') # 店铺链接
    #     }
    #     print(shop)
    #     save_to_mongo(shop)

    # <div class="Content--contentInner--QVTcU0M">
    # <div> ... <div>
    # <div> ... <div>
    # ...
    # <div> ... <div>
    # </div>

    time.sleep(random.uniform(1, 2))
    parent_div = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.Content--contentInner--QVTcU0M'))
    )
    child_divs = parent_div.find_elements(By.CSS_SELECTOR, '.Content--contentInner--QVTcU0M > div')
    hrefs = []
    for index, child in enumerate(child_divs):
        # Find all <a> elements within the current child <div>
        anchor_elements = child.find_elements(By.TAG_NAME, 'a')[0]

        href = anchor_elements.get_attribute('href')
        hrefs.append(href)
    # mkdir /taobao/{KEYWORD} if it doesn't exist
    if not os.path.exists(f'taobao/{KEYWORD}'):
        os.makedirs(f'taobao/{KEYWORD}')
    # write the hrefs to a file
    with open(f'taobao/{KEYWORD}/hrefs_{page}.txt', 'w') as f:
        for href in hrefs:
            f.write(f'{href}\n')
    f.close()
    print(f'Wrote {len(hrefs)} hrefs to file')


def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    for i in range(1, MAX_PAGE + 1):
        get_page(i)
        time.sleep(random.uniform(1, 2.5))
    browser.close()


if __name__ == '__main__':
    main()
