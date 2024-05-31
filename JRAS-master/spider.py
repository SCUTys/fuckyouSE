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

#spider_product函数用于爬取商品ID,参数为cookie,url,page_num, 返回值为商品ID列表(string)
def spider_product(cookie, content, page_num):

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

        selector = parsel.Selector(html_data)

        goods.extend(selector.xpath('//div[@class="gl-i-wrap"]'))

    product_ids = []

    for good in goods:
        # price = good.xpath('string(.//div[@class="p-price"])').get("").strip()
        # title = good.xpath('string(.//div[@class="p-name p-name-type-2"])').get("").strip()
        # shop = good.xpath('string(.//div[@class="p-shop"])').get("").strip()
        detail_url = good.xpath('.//div[@class="p-name p-name-type-2"]/a/@href').get("").strip()


        product_ids.extend(re.findall(r'\d+', detail_url))

    return product_ids


def spider_data(page, product_id):
    """
    发起请求并获取指定商品评分、页码的评论数据

    参数:
    - product_id (int): 商品ID
    - score (int): 评论类型，4为全部评论

    返回:
    - dict: 解析后的JSON数据
    """

    score = 4
    page_amount = 3

    columns = ['nickname', 'id', '内容', '时间']
    df = pd.DataFrame(columns=columns)

    for i in tqdm(range(1, page_amount + 1)):
        time.sleep(0.5)
        url = f'https://club.jd.com/comment/productPageComments.action?&productId={product_id}&score={score}&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1'

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
        }

        time.sleep(1)
        response = requests.get(url=url, headers=headers)
        data = json.loads(response.text)

        for item in data['comments']:
            df.loc[len(df)] = [item['nickname'], item['id'], item['content'], item['creationTime']]

    return df







if __name__ == '__main__':
    print(1)
    # main('shshshfpa=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; shshshfpx=461eef8c-5592-f1b8-1863-c296acf144e8-1713490842; __jdu=17134908428041536521440; __jdv=76161171|www.bing.com|-|referral|-|1716431528090; areaId=19; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; ipLoc-djd=19-1601-50258-129167; 3AB9D23F7A4B3CSS=jdd03TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4AAAAMPZF4HXWYAAAAAC2MINHCUQT5OKUX; _gia_d=1; 3AB9D23F7A4B3C9B=TNWWNPEFMMCF3K34TQT4W2L7W2ENOCVPKMVTXU3VLXUIVJKPCXUAAGMBMZQ5ZR3YEUK7DYB4543KPOQHT4F3VEYRU4; TrackID=1eTKDQOFnNxPQGaszQJ7torU2Qqbg4mvGoH5prNMNLNIm71TXDBqLjxi78yUCPyDwa0pDT8mChvTco3Xst3YSEWEgWQFoeFaWA-CmXkK0gFqOiJJHKXJa6DQFSW9yuNM8; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC50772C4CE028EA18C2550B6EDD12A9510B9DB71B1A0EB13F0A7415C17FEAD235FF17DB3AC1D70F66C4FED351BC4E47D2FDC671664E42EAB6C140E1C8A7B1704898B5D433763206537128AC9359EA24D83CBBD8E0075E5E5208E30CE94F3D41DC9E047753B556FBF6D0CE2F46D9426B7250FE230EF6636AC5F02A70E2D946B2626A28; flash=2_3aLITYetDX6Zi8jYaqTco3DK5oucL4MKdqqXvSC8wGcIrOEq7T49XQ89zr-XdZ0V-g41NpdhIsDt0oi97TJPWi0fdbNyuW5lcLgFChRqLi5dQOgmg9O-BkLfVkSaa_iejQe0ApYr-ASEdTUFG_BWlG9U70B9qdmobGIWHYv-fFp*; ceshi3.com=000; __jda=76161171.17134908428041536521440.1713490843.1717035629.1717072068.5; __jdb=76161171.3.17134908428041536521440|5.1717072068; __jdc=76161171; shshshfpb=BApXchJlxyupA6EGcp9UfDKqqq-EXN_UyBlEID21p9xJ1MiXwPIC2',
    #      '5G')









