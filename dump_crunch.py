#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#author: yangrui
#date: 2015.4.19
#connect: fadeblack@163.com
#dump some news from http://techcrunch.cn/ but maybe fucking frobiden by china


from bs4 import BeautifulSoup
import lxml
import requests
import sys, time, os
from magic3 import syscommand
from urllib.parse import urlparse

class DumpCrunch(object):
    def __init__(self):
        pass
        
    def run(self, url, path, tag):
        url_list = self._get_url(url)
        self._dump_new(url_list, path, tag)

    def _get_url(self, url):
        """get top 20 new from page"""
        try:
            r = requests.get(url, timeout = 15)
            r.raise_for_status()
        except requests.RequestException as e:
            print(e)
        else:
            url_list = [] 
            web = r.content.decode('utf-8', 'ignore')
            try:
                bs = BeautifulSoup(web, 'lxml')
                litags = bs.find_all('li', class_ = "river-block")
                for litag in litags:
                    if litag:
                        url = litag.get('data-permalink')
                        url_list.append(url)
                return url_list
            except Exception as e:
                print(e)
    
    def _today(self):
        return time.strftime('%Y-%m-%d')
    
    def _make_dir(self, path, tag):
        path = path + '/' + tag + '/' + self._today()
        if os.path.exists(path):
            return path
        else:
            os.makedirs(path)
            return path
    
    def _dump_new(self, url_list, path, tag):
        dst_path = self._make_dir(path, tag)
        for url in url_list:
            info = syscommand.SysCommand.execute('wget -t 5 -T 20 -P ' + dst_path + ' ' + url)
            print(info)
        self._rename(dst_path)
    
    def _rename(self, path):
        count = 1
        for root, dis, files in os.walk(path):
            for filename in files:
                print(os.path.join(root, filename))
                os.rename(os.path.join(root, filename), os.path.join(root, str(count) + '.html'))
                count += 1



if __name__ == '__main__':
    print('爬取开始 .cn: ')
    t1 = time.time()
    dc = DumpCrunch() 
    dc.run('http://techcrunch.cn/', '/home/workpro/spidernews/dump_crunch', 'crunch.cn')
    print('爬取分析结束 .cn: ', time.time() - t1)

    print('爬取开始 .com: ')
    t1 = time.time()
    dc.run('http://techcrunch.com/', '/home/workpro/spidernews/dump_crunch', 'crunch.com')
    print('爬取分析结束 .com: ', time.time() - t1)









