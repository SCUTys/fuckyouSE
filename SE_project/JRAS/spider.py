# coding='utf-8'
import argparse
import os
import requests
import json
import time
import openpyxl
from openpyxl import Workbook
import parsel
import re
import pandas as pd
from tqdm import tqdm
import sqlite3



#input:
#   page_num: 爬取页数， 默认为1
#return:
#   {product_id: {"name": name, "price": price, "image": img}}
def spider_product(cookie, content, page_num=2):

    url = f'https://search.jd.com/Search?keyword={content}&page='

    goods = []

    for page in range(1, page_num):
        header = {
            'Referer': 'https://search.jd.com/',
            'Origin': 'https://search.jd.com',
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }

        new_url = url + str(page)


        response = requests.get(url=new_url, headers=header)

        html_data = response.text
        # print(html_data)
        selector = parsel.Selector(html_data)

        goods.extend(selector.xpath('//div[@class="gl-i-wrap"]'))

    product_ids = {}

    for good in goods:
        detail_url = good.xpath('.//div[@class="p-name p-name-type-2"]/a/@href').get("").strip()
        product_id = re.findall(r'\d+', detail_url)[0]

        name = ''.join([data.get() for data in good.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')]).strip()
        price = good.xpath('.//div[@class="p-price"]/strong/i/text()').get("").strip()

        html = good.xpath('.//div[@class="p-img"]/a/img').get("").strip()
        pos = html.find('data-lazy-img="')
        substr = html[pos + 15:]
        img = substr[:substr.find('"')]

        product_ids[product_id] = {"name" : name, "price" : price, "image" : img}
    print(product_ids)
    return product_ids


#intput:
#   page: 爬取评论页数, 默认为3
#return:
#   [{nickname: nickname, id: id, content: content, creationTime: creationTime}]
def spider_comment(product_id, page_amount=3):

    score = 4

    comments = ''

    for i in tqdm(range(1, page_amount + 1)):
        time.sleep(0.5)
        url = f'https://club.jd.com/comment/productPageComments.action?&productId={product_id}&score={score}&sortType=5&page={i}&pageSize=10&isShadowSku=0&fold=1'

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
        }

        time.sleep(1)
        response = requests.get(url=url, headers=headers)
        data = json.loads(response.text)

        for item in data['comments']:
            comments = comments + '\n' + item['content']

    return comments


def spider_parameter(cookie, product_id):

    url = f'https://item.jd.com/{product_id}.html'

    headers = {
        'Referer': 'https://search.jd.com/',
        'Origin': 'https://search.jd.com',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    response = requests.get(url=url, headers=headers)


    selector = parsel.Selector(response.text)

    ul_element = selector.xpath('//ul[@class="parameter2 p-parameter-list"]')

    li_elements = ul_element.xpath('.//li')

    parameters = {}

    for element in li_elements:
        title = element.xpath('./@title').get()
        text = element.xpath('string(.)').get()

        if '商品编号' in text:
            continue

        parameters[text.split("：")[0]] = text.split("：")[1]

    return parameters


def spider(cookie, content, page_num=1):

    conn = sqlite3.connect('jd_comments.sqlite3')
    cursor = conn.cursor()

    product_ids = spider_product(cookie, content, page_num)

    store_data = {}

    for product_id, value in product_ids.items():


        # cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_name = 'phone-'{product_id};")
        # if cursor.fetchone() is not None:
        #     continue
        #
        # cursor.execute("")

        store_data[product_id] = {}
        store_data[product_id]['brief'] = value
        store_data[product_id]['detail'] = spider_parameter(cookie, product_id)
        store_data[product_id]['comment'] = spider_comment(product_id)

    #将数据存到数据库



if __name__ == '__main__':
    cookie = 'shshshfpa=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; shshshfpx=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; __jdu=17134908428041536521440; __jdv=76161171|www.bing.com|-|referral|-|1716431528090; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; qrsc=3; TrackID=1eTKDQOFnNxPQGaszQJ7torU2Qqbg4mvGoH5prNMNLNIm71TXDBqLjxi78yUCPyDwa0pDT8mChvTco3Xst3YSEWEgWQFoeFaWA-CmXkK0gFqOiJJHKXJa6DQFSW9yuNM8; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC50772C4CE028EA18C2550B6EDD12A9510B9DB71B1A0EB13F0A7415C17FEAD235FF17DB3AC1D70F66C4FED351BC4E47D2FDC671664E42EAB6C140E1C8A7B1704898B5D433763206537128AC9359EA24D83CBBD8E0075E5E5208E30CE94F3D41DC9E047753B556FBF6D0CE2F46D9426B7250FE230EF6636AC5F02A70E2D946B2626A28; flash=2_3aLITYetDX6Zi8jYaqTco3DK5oucL4MKdqqXvSC8wGcIrOEq7T49XQ89zr-XdZ0V-g41NpdhIsDt0oi97TJPWi0fdbNyuW5lcLgFChRqLi5dQOgmg9O-BkLfVkSaa_iejQe0ApYr-ASEdTUFG_BWlG9U70B9qdmobGIWHYv-fFp*; areaId=19; ipLoc-djd=19-1601-0-0; 3AB9D23F7A4B3CSS=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMP5NKXCPQAAAAADEXWQJFOS6MTNQX; rkv=1.0; __jda=143920055.17134908428041536521440.1713490843.1717553599.1717640026.8; __jdc=143920055; shshshfpb=BApXclwtd6OpA6EGcp9UfDKqqq-EXN_UyBlEID21s9xJ1MiXwPIC2; 3AB9D23F7A4B3C9B=TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4; avif=1; __jdb=143920055.5.17134908428041536521440|8.1717640026'
    product_ids = spider_product(cookie,
         '5G', 2)

    spider(cookie, '5G', 2)









