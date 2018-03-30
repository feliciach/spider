#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json

import math
import requests
import time
from bs4 import BeautifulSoup

def urlReq(url):
    r=requests.get(url)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text, "lxml")
    ll={}
    link_list=[]
    soup_class=soup.find_all("ul",class_= "type-list")
    for line in soup_class:
        for link in line.find_all("a"):
            lin=link['href']
            text=link.text
            ll[text]=lin
            link_list.append(lin)
    return link_list

def child_urlReq(c_url):
    res=page_info(c_url,1)
    print(res)
    # movie_list=[]
    # for i in result:
    #     year=i['year']
    #     title=i['title']
    #     murl=i['url']
    #     movie_list.append([title,year,murl])
    # return

def page_info(child_url,page_num):
    r = urllib.request.urlopen(child_url).read()
    # r.encoding='utf-8'
    c_soup = BeautifulSoup(r, "lxml")
    c_soup_h = c_soup.find_all("script")
    x = str(c_soup_h[3]).split('\n')
    y1, y2 = x[2], x[3]
    movie_tag = y1.lstrip('var TYPE = \'').rstrip('\';')
    LOC_ID = y2.lstrip('var LOC_ID = \'').rstrip('\';')
    t = time.time()
    temp_i=1
    while temp_i<=page_num:
        resource_url = "https://m.douban.com/rexxar/api/v2/subject_collection/" + movie_tag + "/items?os=ios&for_mobile=1&callback=jsonp" + str(page_num) + "&start=0&count=18&loc_id=" + LOC_ID + "&_=" + str(int(round(t * 1000)))
        header = {
            "Acceptl": "*/*",
            "Referer": child_url,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        r2 = requests.get(resource_url, headers=header)
        print(r2, type(r2.text))
        jsonp = r2.text.lstrip(';jsonp1(').rstrip(');')
        j = json.loads(jsonp)
        result = j['subject_collection_items']
        total_num = j["total"]
        page_num = math.ceil(total_num / 18)
        print(total_num, page_num)

    return page_num

if __name__=='__main__':
    requestUrl="https://m.douban.com/movie"
    tag_list=urlReq(requestUrl)
    for list in tag_list:
        cild_rUrl="https://m.douban.com"+str(list)
        print(cild_rUrl)
        movie_dict=child_urlReq(cild_rUrl)
        print(movie_dict)
