# -*- coding=utf-8 -*-
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
url = 'https://fabiaoqing.com/search/search/keyword/%E6%9D%B0%E5%B0%BC%E9%BE%9F'

def getlinks(url):
    headers = {}
    headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    request = Request(url ,headers=headers)
    html = urlopen(request)
    bsObj = BeautifulSoup(html)
    try:
        image_location = bsObj.findAll('img', {'class' : 'ui image bqppsearch lazy'})
    except:
        print('http error')
    return image_location

list = []
links = getlinks(url)
for t in links:
    list.append(t['data-original'])
print(list)

# urlretrieve(image_location, 'text\jienigui.jpg')

