# -*- coding=utf-8 -*-
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import ssl
import os
import re
import json
import requests

url = 'https://fabiaoqing.com/search/search/keyword/%E6%9D%B0%E5%B0%BC%E9%BE%9F'
url_diy = 'https://fabiaoqing.com/diy/lists/page/1.html'

ssl._create_default_https_context = ssl._create_unverified_context


def get_links(url):
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    request = Request(url, headers=headers)
    html = urlopen(request)
    bsObj = BeautifulSoup(html)
    try:
        image_location = bsObj.findAll('img', {'class': 'ui image bqppsearch lazy'})
    except:
        print('http error')
    return image_location


def getlinks_diy(url):
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    request = Request(url, headers=headers)
    html = urlopen(request)
    bsObj = BeautifulSoup(html)
    try:
        image_location = bsObj.findAll('img', {'class': 'ui small bordered image bqpp lazy'})
    except:
        print('http error')
    return image_location


def get_links_diy_s(url):
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    r = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(r.text)
    tags = None
    try:
        tags = bsObj.findAll('img', {'class': 'ui small bordered image bqpp lazy'})
    except:
        print('http error')
    links = []
    for t in tags:
        links.append(t['data-original'])
    return links


def get_tags(url):
    headers = {}
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    r = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(r.text)
    tags = None
    try:
        tags = bsObj.findAll('img', {'class': 'ui small bordered image bqpp lazy'})
    except:
        print('http error')
    return tags


def links():
    temps = []
    for x in range(1, 40):
        url_ = 'https://fabiaoqing.com/diy/lists/page/' + str(x) + '.html'
        links = get_links_diy_s(url_)
        for link in links:
            dic = {}
            dic['filename'] = link.split('/')[-1]
            dic['url'] = link.replace('bmiddle', 'large')
            temps.append(dic)
    print(temps)
    print(len(temps))
    print(len(temps) / 30)
    print(len(temps) % 30)
    with open('data.json', 'w') as f:
        json.dump(temps, f, ensure_ascii=False, indent=4)


def download():
    with open('data_temp.json', 'r') as f:
        temps = json.load(f)
    for temp in temps:
        filename = temp['filename']
        url = temp['url']
        loc = 'test/temps/' + filename
        urlretrieve(url, loc)
# urlretrieve(image_location, 'text\jienigui.jpg')


def temp_tags():
    temps = []
    for x in range(1, 40):
        url1 = 'https://fabiaoqing.com/diy/lists/page/' + str(x) + '.html'
        imgs = get_tags(url1)
        for img in imgs:
            link = img['data-original']
            title = img['title']
            dic = {}
            dic['filename'] = link.split('/')[-1]
            dic['title'] = title.split('-')[0]
            temps.append(dic)
    print(temps)
    print(len(temps))
    with open('db/data_title.json', 'w', encoding='utf-8') as f:
        json.dump(temps, f, ensure_ascii=False, indent=4)

def main():
    temp_tags()


if __name__ == "__main__":
    main()