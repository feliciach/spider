#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.request
import requests
import json

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
    # print(soup_class)

    for line in soup_class:
        for link in line.find_all("a"):
            # name=link.find("a")
            lin=link['href']
            text=link.text
            ll[text]=lin
            link_list.append(lin)
    # print(ll)
    # print(soup.prettify())
    # b=re.findall(r'<li.*?>(.*?)<\/li>',r'\1',soup)
    # for c in b:
    #     print(c)
    print(time.time)
    return link_list

def child_urlReq(c_url):
    r = urllib.request.urlopen(c_url).read()
    # r.encoding='utf-8'
    c_soup=BeautifulSoup(r, "lxml")
    # print(c_soup)
    c_soup_h=c_soup.find("div",id="app")
    # https: // m.douban.com / rexxar / api / v2 / subject_collection / filter_movie_comedy_hot / items?os = ios & for_mobile = 1 & callback = jsonp1 & start = 0 & count = 18 & loc_id = 108288 & _ = 1522228776531
    # https: // m.douban.com / rexxar / api / v2 / subject_collection / filter_movie_comedy_hot / items?os = ios & for_mobile = 1 & callback = jsonp2 & start = 18 & count = 18 & loc_id = 108288 & _ = 1522228781100
    resource_url="https://m.douban.com/rexxar/api/v2/subject_collection/filter_movie_comedy_hot/items?os=ios&for_mobile=1&callback=jsonp1&start=0&count=18&loc_id=108288&_=1522228776531"
    header={
        "Acceptl":"*/*",
        "Referer":"https://m.douban.com/movie/comedy",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
    t=time.time()
    print(int(round(t * 1000)))
    r2=requests.get(resource_url,headers=header)
    print(type(r2.text))
    jsonp=r2.text.lstrip(';jsonp1(').rstrip(');')
    j=json.loads(jsonp)
    print(type(j))
    print(j)
    result=j['subject_collection_items']
    print(type(result),result)
    movie_list=[]
    for i in result:
        print(type(i),i)
        year=i['year']
        title=i['title']
        murl=i['url']
        movie_list.append([title,year,murl])
    return movie_list

if __name__=='__main__':
    requestUrl="https://m.douban.com/movie"
    # requestHeader={"Cookie":"updateTime=1521784425574; tempid=C7EBA193067000024FDF187BD9B09E80; inited=true; Hm_lvt_e8b95084d523b4cfd0ab55c7bee08f2c=1520824660,1520956353,1521185631,1521782885; Hm_lpvt_e8b95084d523b4cfd0ab55c7bee08f2c=1521784426; _digger_uuid=f9bfabbf88e3adc4; cookie_id=1521784425890f9bfa; wxLocName=%u5929%u5E9C%u5927%u9053%u4E2D%u6BB5666%u53F7%u5E0C%u987F%u56FD%u9645%u5E7F%u573AA%u5EA7%20%u6210%u90FD%u5E0C%u5C14%u987F%u9152%u5E97; wxLoc=104.068016%2C30.549033; wxDc=7%2C10%2C11%2C12%2C17%2C63%2C220%2C291%2C342%2C343%2C346%2C395%2C10082%2C10181%2C10258%2C10330%2C10359%2C10390%2C10392%2C10395%2C10396%2C10404%2C12259; wxShops=73-0-10396%2C73-0-10395%2C73-0-10404%2C8-0-10181%2C71-0-10392%2C53-0-12259%2C28-0-10258%2C70-0-10390%2C6-0-10082%2C54-0-10359%2C2-0-395%2C27-0-10330%2C1-17-12%2C1-17-291%2C1-17-10%2C1-17-342%2C1-17-63%2C1-17-7%2C1-17-11%2C1-17-17%2C1-17-343%2C1-17-346%2C1-19-220; wxIsUpdateConsign=false; storeGroup=1-291-1%2C2-291-1%2C5-291-1%2C7-10359-54; hasBind=true; ticketLoginId=a9751b74-0677-42d2-911f-2a02f8738351; ticketName=166AFB1BFFB41B59550FE2A9EB237F3F218EDF76297768496BF5F79CF185AC5917DF9CA908D0DECE97502713F91A6107FFA3A5465B48C8B675A4A7BECF715AA9CC26471CA533B6608D6291161EA2409C2C4D7000B1280D46B70FF0ACD80863394E8F172AB6F275EC749D39D8B52C43FB9D795531089BF4CE2FEDD86E9038DC11; ticketWeChat=166AFB1BFFB41B59550FE2A9EB237F3F218EDF76297768496BF5F79CF185AC5917DF9CA908D0DECE97502713F91A6107FFA3A5465B48C8B675A4A7BECF715AA9CC26471CA533B6608D6291161EA2409C2C4D7000B1280D46B70FF0ACD80863394E8F172AB6F275EC749D39D8B52C43FB9D795531089BF4CE2FEDD86E9038DC11; token=46506bfd-f814-4770-8961-0980aba9595c; ismerge=true","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
    tag_list=urlReq(requestUrl)
    for list in tag_list:
        cild_rUrl="https://m.douban.com"+str(list)
        print(cild_rUrl)
    movie_dict=child_urlReq("https://m.douban.com/movie/comedy")
    print(movie_dict)
