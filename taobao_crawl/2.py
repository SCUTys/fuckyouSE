# coding=utf-8
import os

import pymongo, time, random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait as Wait
from pyquery import PyQuery as pq
from urllib.parse import quote

MONGO_URL = 'localhost'
MONGO_DB = 'test'
MONGO_COLLECTION = 'huawei'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--user-data-dir=Default')
browser = webdriver.Chrome()
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

wait = WebDriverWait(browser, 30)

path = 'taobao'
KEYWORD = '华为P50'
# turn the keyword into url code
KEYWORD = quote(KEYWORD)


def read_hrefs():
    path_to_folder = os.path.join(path, KEYWORD)

    # find all txt files in format hrefs_{}.txt
    files = [f for f in os.listdir(path_to_folder) if
             os.path.isfile(os.path.join(path_to_folder, f)) and f.startswith('hrefs_') and f.endswith('.txt')]
    urls = []
    for file in files:
        with open(os.path.join(path_to_folder, file), 'r') as f:
            urls += f.readlines()

    # remove '\n' from urls
    urls = [url.strip() for url in urls]

    return urls


urls = read_hrefs()


def slide_down(second):
    for i in range(int(second / 0.1)):
        js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
        browser.execute_script(js)
        time.sleep(random.uniform(0.2, 0.4))
    time.sleep(0.2)


def get_page(url, retry=0):
    context = []
    if retry > 2:
        print('too many retries, skipping', url)
        return ''
    print('正在爬取', url)
    try:
        browser.get(url)

        # if the url redirects to https://detail.tmall.com/auction/noitem.htm?type=1, return nothing
        if 'noitem.htm' in browser.current_url:
            print('redirected to a blank page, maybe the item is not available')
            return ''

        max_scroll_attempts = 5  # Maximum number of scroll attempts
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            try:
                # wait until one of the two components is present
                locator_1 = (By.CSS_SELECTOR, '.ItemDetail--attrs--3t-mTb3')
                locator_2 = (By.CLASS_NAME, 'InfoItem--infoItem--zCvv3MH')

                wait = Wait(browser, 3)  # Explicit wait for up to 10 seconds
                parent_div = wait.until(EC.presence_of_element_located(locator_1))
                if parent_div:
                    ptr = 1
                    break

            except TimeoutException:
                try:
                    wait = Wait(browser, 3)
                    parent_div = wait.until(EC.presence_of_element_located(locator_2))
                    if parent_div:
                        ptr = 2
                        break
                except TimeoutException:
                    # Scroll down a bit and try again
                    browser.execute_script("window.scrollBy(0, window.innerHeight * 1.0);")
                    time.sleep(random.uniform(1, 2))
                    scroll_attempts += 1
                    continue

        if scroll_attempts >= max_scroll_attempts:
            raise TimeoutException("Failed to find the required elements after scrolling")

        if ptr == 1:
            # find all divs with class Attrs--attrSection--2_G8xGa in the parent div
            divs = parent_div.find_elements(By.CSS_SELECTOR, '.Attrs--attrSection--2_G8xGa')
            for div in divs:
                # find all spans with class Attrs--attr--33ShB6X in the div
                spans = div.find_elements(By.CSS_SELECTOR, '.Attrs--attr--33ShB6X')
                for span in spans:
                    context.append(span.text)
        else:
            divs = browser.find_elements(By.CSS_SELECTOR, '.InfoItem--infoItem--zCvv3MH')
            for div in divs:
                context.append(div.text)
        print('success')

        slide_down(2.1)
        time.sleep(random.uniform(1, 2))
    except TimeoutException:
        print('Something went wrong')
        time.sleep(random.uniform(5, 8))
        get_page(url, retry + 1)

    ret = {'url': url, 'info': {}}
    flag = False
    for text in context[0]:
        if '：' in text:
            flag = True
    if flag:
        for text in context:
            if '：' in text:
                key, value = text.split('：')
                ret['info'][key] = value
    else:
        for text in context:
            if '\n' in text:
                key, value = text.split('\n')
                ret['info'][key] = value

    # dump the result to file
    with open('./taobao/result.txt', 'a') as f:
        f.write(str(ret) + '\n')

    print(ret)


for url in urls:
    get_page(url)
