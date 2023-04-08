import requests
from bs4 import BeautifulSoup
import pymysql


def get_items(html, category_name, sub_category_name):
    best_item = html.select_one('div.best-list')
    for index, item in enumerate(best_item.select('li')):
        product_link = item.select_one('div.thumb > a')
        item_code = product_link.attrs['href'].split(
            '=')[1].replace('&ver', '')

        res = requests.get(product_link.attrs['href'])
        print(product_link.attrs['href'])
        soup = BeautifulSoup(res.content, 'html.parser')


def get_category(category_link, category_name):
    print(category_link, category_name)
    res = requests.get(category_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    get_items(soup, category_name, "ALL")

    sub_categories = soup.select('div.navi.group ul li > a')
    for sub_category in sub_categories:
        res = requests.get(
            'http://corners.gmarket.co.kr/' + sub_category['href'])
        soup = BeautifulSoup(res.content, 'html.parser')
        print(category_name, sub_category.get_text())
        get_items(soup, category_name, sub_category.get_text())


res = requests.get('http://corners.gmarket.co.kr/Bestsellers')
soup = BeautifulSoup(res.content, 'html.parser')

categories = soup.select('div.gbest-cate ul.by-group li a')
for category in categories:
    get_category('http://corners.gmarket.co.kr/' +
                 category['href'], category.get_text())
