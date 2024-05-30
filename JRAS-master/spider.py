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


#spider_product函数用于爬取商品ID,参数为cookie,url,page_num, 返回值为商品ID列表(string)
def spider_product(cookie, url, page_num):

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


def start(page, product_id, score):
    """
    发起请求并获取指定商品评分、页码的评论数据

    参数:
    - page (int): 页码
    - product_id (int): 商品ID
    - score (int): 评论类型，4为全部评论

    返回:
    - dict: 解析后的JSON数据
    """
    url = f'https://club.jd.com/comment/productPageComments.action?&productId={product_id}&score={score}&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1'

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"
    }
    time.sleep(2)
    response = requests.get(url=url, headers=headers)
    data = json.loads(response.text)
    return data


def parse(data):
    """
    解析评论数据，生成包含用户昵称、评论ID、评论内容、创建时间的元组序列

    参数:
    - data (dict): JSON格式的评论数据

    返回:
    - generator: 包含用户昵称、评论ID、评论内容、创建时间的元组序列
    """
    items = data['comments']
    for i in items:
        yield (
            i['nickname'],
            i['id'],
            i['content'],
            i['creationTime']
        )


def excel(items, product_id):
    """
    将评论数据写入Excel文件（如不存在则创建）

    参数:
    - items (generator): 包含用户昵称、评论ID、评论内容、创建时间的元组序列
    - product_id (int): 商品ID
    """
    if not os.path.exists('output'):
        os.makedirs('output')
    new_table = f'output/original_data.xlsx'
    wb = Workbook()
    ws = wb.active

    # 设置表头
    head_data = ['nickname', 'id', '内容', '时间']
    for i in range(0, 4):
        ws.cell(row=1, column=i + 1).value = head_data[i]

    index = 2

    # 写入评论数据
    for data in items:
        for i in range(0, 4):
            print(data[i])
            ws.cell(row=index, column=i + 1).value = data[i]
        print('______________________')
        index += 1

    wb.save(new_table)


def another(items, j, product_id):
    """
    将评论数据追加到已存在的Excel文件中

    参数:
    - items (generator): 包含用户昵称、评论ID、评论内容、创建时间的元组序列
    - j (int): 当前页码
    - product_id (int): 商品ID
    """
    if not os.path.exists('output'):
        os.makedirs('output')
    new_table = f'output/original_data.xlsx'
    index = (j - 1) * 10 + 2  # 计算起始行索引

    data = openpyxl.load_workbook(new_table)
    ws = data.active

    # 追加评论数据
    for test in items:
        for i in range(0, 4):
            print(test[i])
            ws.cell(row=index, column=i + 1).value = test[i]
        print('_______________________')
        index += 1

    data.save(new_table)


def main():
    """
    主程序：解析命令行参数，获取商品评论数据，并将数据写入Excel文件
    """
    # parser = argparse.ArgumentParser(description="京东商品评论爬虫")
    # parser.add_argument('-p', '--product-id', required=True, type=int,
    #                     help="输入商品ID")

    # args = parser.parse_args()

    url = f'https://search.jd.com/Search?keyword=衣服&page='
    cookie = '__jdv=76161171|cn.bing.com|-|referral|-|1716946490937; __jdu=17169464909361480478240; areaId=19; ipLoc-djd=19-1601-0-0; shshshfpa=42e1df4c-a94f-b1c3-2ecf-83ec064150c0-1716946493; shshshfpx=42e1df4c-a94f-b1c3-2ecf-83ec064150c0-1716946493; TrackID=1NxGXWWnPCX4H8CRG961yABIGh3yfDeusGlJi967WC5JmONHuT_X58voW0q-EScSV0uXEGJmbLj_cefJSqJdcb4q6ZvVTX4C9lBFWBceZPm1JL9FzyqT_cR5Q0lCmenh2; thor=0154BEF7F3ABAD2AC9F8B853DF438E2DA2332B6EEBDE1EF9CABCA0BF63AC5077C4238DE713BB01ECF9B81E43713564F797923C2DB43E14A8D3D56EFD690090D732E369C65E0B130F3C89860BBA8C55E8D8FAB04853CCED7588ACBB46EA00FCB7D1F0DFDEBE47ECEB4309675D57CDDAAD989D28FC9EB50000C32FFECF5008EDE08EE189F0A4C3E6693E6E031068386C71710EC2AE98DBF00392D4EE54FAB0F49F; flash=2_l6PPtqplgaIHFow-fb5TQgWqBA4FzrgLgFT_lJCB_ETCaGTFxlK2lAipDNC-KSIJc5POwoxHdz98BJ8g6DcaHd9svSb-i9IDhK00KfQiOngifGfjlGxTSe4w6hQwYQnWO7vmomnCzep9cHgfLSfuWfdfU329GE5dgbvz0nxdY9D*; pinId=gpXgCqz9ZronTwmVTfLR3g; pin=jd_hoCgxwDRQSiQ; unick=jd_es2lk4sv85zfx8; ceshi3.com=000; _tp=ezZG5SVF%2BP5fpYqKEfdi1Q%3D%3D; _pst=jd_hoCgxwDRQSiQ; __jdc=143920055; shshshfpb=BApXcAqoAwepAF3FcWwhfd5wG6pu9h-EaBlTVY7xo9xJ1MtW9S4C2; 3AB9D23F7A4B3C9B=LRTNJGNAAT74MHWXM6PTBV6WGNCZ6VUI2QK5V5NXINTI7KIAL3BYO6U57LYWTIXJ6PLTDWIOWZ6VDWB4CVXBKKQE7A; token=0dcc5f0529d049da538be2e93f6a4699,3,953861; 3AB9D23F7A4B3CSS=jdd03LRTNJGNAAT74MHWXM6PTBV6WGNCZ6VUI2QK5V5NXINTI7KIAL3BYO6U57LYWTIXJ6PLTDWIOWZ6VDWB4CVXBKKQE7AAAAAMPYJIYDIYAAAAACLXSGU4YYJFZGIX; _gia_d=1; jsavif=1; __jda=143920055.17169464909361480478240.1716946491.1716946491.1716952073.2; __jdb=143920055.1.17169464909361480478240|2.1716952073'

    products_id = spider_product(cookie, url, 4)

    for product_id in products_id:

        score = 4
        page_amount = 5

        j = 1
        judge = True

        for i in range(0, page_amount):
            time.sleep(1.5)
            first = start(j, product_id, score)
            test = parse(first)

            if judge:
                excel(test, product_id)
                judge = False
            else:
                another(test, j, product_id)
            print(f'第{j}页抓取完毕')
            j += 1


if __name__ == '__main__':
    main()









