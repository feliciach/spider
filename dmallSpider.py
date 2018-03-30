#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import csv
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
    movie_dict=res_info(c_url)
    return movie_dict

def res_pagenum(c_url):
    temp_j=trans_url(c_url,0,1,18)
    total_num=temp_j["total"]
    page_num=math.ceil(total_num/18)
    print(total_num,page_num)
    return page_num

def res_info(c_url):
    temp_p=res_pagenum(c_url)
    temp_c=1
    movie_list = []
    while temp_c<=temp_p:
        temp_start=18*(temp_c-1)
        temp_j=trans_url(c_url,temp_start,temp_c,18)
        result=temp_j['subject_collection_items']
        for i in result:
            year=i['year']
            title=i['title']
            murl=i['url']
            movie_list.append([title,year,murl])
        temp_c=temp_c+1
    writecsv(movie_list)
    return movie_list

def trans_url(c_url,start_num,page_num,count):
    r = urllib.request.urlopen(c_url).read()
    # r.encoding='utf-8'
    c_soup=BeautifulSoup(r, "lxml")
    c_soup_h=c_soup.find_all("script")
    x=str(c_soup_h[3]).split('\n')
    y1,y2=x[2],x[3]
    movie_tag=y1.lstrip('var TYPE = \'').rstrip('\';')
    LOC_ID=y2.lstrip('var LOC_ID = \'').rstrip('\';')
    t=time.time()
    resource_url="https://m.douban.com/rexxar/api/v2/subject_collection/"+movie_tag+"/items?os=ios&for_mobile=1&callback=jsonp"+str(page_num)+"&start="+str(start_num)+"&count="+str(count)+"&loc_id="+LOC_ID+"&_="+str(int(round(t * 1000)))
    header={
        "Acceptl":"*/*",
        "Referer":c_url,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
    r2=requests.get(resource_url,headers=header)
    temp_str=";jsonp"+str(page_num)+"("
    jsonp=r2.text.lstrip(temp_str).rstrip(');')
    jsonpx=json.loads(jsonp)
    return jsonpx

def writecsv(movie_list):
    csvFile=open('D:\douban.csv','w',newline='')
    writer=csv.writer(csvFile)
    m =len(movie_list)
    writer.writerow(movie_list)
    return
if __name__=='__main__':
    requestUrl="https://m.douban.com/movie"
    tag_list=urlReq(requestUrl)
    cild_rUrl = "https://m.douban.com/movie/comedy"
    print(cild_rUrl)
    movie_list=child_urlReq(cild_rUrl)
    print(movie_list)
    # for list in tag_list:
    #     cild_rUrl="https://m.douban.com"+str(list)
    #     print(cild_rUrl)
    #     movie_list=child_urlReq(cild_rUrl)
    #     print(movie_list)
