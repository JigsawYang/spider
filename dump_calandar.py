#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#author: yangrui
#date: 2015.4.15
#connect: fadeblack@163.com
#python3.4
#dump some info from 
#http://www.31huiyi.com/eventlist/type/15/time/2015-04-01t2015-04-30/province/11_0/page/1

from bs4 import BeautifulSoup
import lxml
import requests
import getpass
import simplejson as json
import sys, time
import pymysql.cursors

__all__ = ['get_news', 'insertdb', 'run']


def logprint(title):
    '''print log info'''
    def _wrapper(func):
        def _call(*args,**kwargs):
            print(time.ctime(), '%s : %s started...' % (title, func.__name__))
            ret = func(*args,**kwargs)
            print(time.ctime(), '%s : %s finished...'% (title, func.__name__))
            return ret
        return _call
    return _wrapper

def get_news(url, info_dict):
    """analysis page get title and time"""
    try:
        r = requests.get(url, timeout = 5)
        r.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        web = r.content.decode('utf-8', 'ignore')
        pos = web.find('已结束')
        web = web[:pos]
        try:
            bs = BeautifulSoup(web, 'lxml')
            links = bs.find_all('li', class_="list_dd1")
            for link in links:
                if link:
                    atag = link.find_next('a')
                    url = atag.get('href')
                    title = atag.string
                    spantag1 = link.find_next('span')
                    spantag2 = spantag1.find_next('span')
                    st_time = spantag2.string
                    # print(url, title, st_time)
                    info_dict[url] = [title, st_time]
        except Exception as e:
            print(e)


def insertdb(info_dict, pwd):
    conn = pymysql.connect('127.0.0.1', 'root', pwd, 'calandar', charset='utf8')
    try:
        with conn.cursor() as cur:
            for i in info_dict:
                cur.execute("insert into news_calandar (title, url, st_time) values (%s, %s, %s)", (info_dict[i][0], i, info_dict[i][1]))
        conn.commit()
    finally:
        conn.close()


@logprint(__name__)
def run(info_dict, config, pwd):
    with open(config, 'r') as f:
        urls = json.load(f, encoding = 'utf-8')
        for url in urls:
            get_news(url, info_dict)
    insertdb(info_dict, pwd)
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('请正确的参数, 输入配置文件')
    else:
        pw = getpass.getpass('输入数据库的root密码： ')
        info = {}
        run(info, sys.argv[1], pw)















