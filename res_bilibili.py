#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moonplayer
import json
import time

res_name = 'Bilibili - Bangumi'

tags = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
countries = ['All']

appkey = '75cd10da32ffff6db8092783baaeafac23140b9fce0c8558' # Caught from bilibili's uwp client

## Explore
bangumi_list = None

def explore(tag, country, page):
    if bangumi_list == None:
        url = 'http://bangumi.bilibili.com/jsonp/timeline_v2?appkey=' + appkey
        moonplayer.download_page(url, explore_cb, tag)
    else:
        result = bangumi_list[tags.index(tag)]
        moonplayer.res_show(result)

def explore_cb(content, tag):
    global bangumi_list
    bangumi_list = [[], [], [], [], [], [], []]
    items = json.loads(content)['list']
    try:
        if items[0]['cover'].startswith('//'):
            pr = 'http:'
        else:
            pr = ''
    except:
        pr = ''
    for item in items:
        day = item['weekday']
        bangumi_list[day].append({'name': item['title'], 'url': item['url'], 'pic_url': pr + item['cover']})
    result = bangumi_list[tags.index(tag)]
    moonplayer.res_show(result)


## Search
def search(key, page):
    url = 'http://app.bilibili.com/x/v2/search/type?pn=1&ps=20&type=1&build=10040700&keyword=' + key
    moonplayer.download_page(url, search_cb, None)

def search_cb(content, data):
    items = json.loads(content)['data']['items']
    try:
        if items[0]['cover'].startswith('//'):
            pr = 'http:'
        else:
            pr = ''
    except:
        pr = ''
    result = [{'name': i['title'], 'url': i['uri'], 'pic_url': pr + i['cover']} for i in items]
    moonplayer.res_show(result)


## Load item
def test():
    moonplayer.warn('Hello')

def load_item(url):
    if url.startswith('bilibili://bangumi/season/'):
        season = url.replace('bilibili://bangumi/season/', '')
    elif url.startswith('/bangumi/i/'):
        season = url.replace('/bangumi/i/', '')
    elif '/anime/' in url:
        season = url.split('/anime/')[1]
    else:
        moonplayer.warn('Bilibili: Cannot open url:' + url)
        return
    if season.endswith('/'):
        season = season[:-1]
    long_epoch = int(time.time() * 1000)
    url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/%s.ver?callback=seasonListCallback&jsonp=jsonp&_=%i' % (season, long_epoch)
    moonplayer.download_page(url, load_item_cb, None)
    
def load_item_cb(content, data):
    if content.startswith('seasonListCallback('):
        content = content.replace('seasonListCallback(', '')[:-2]
    data = json.loads(content)['result']
    srcs = []
    for item in data['episodes']:
        name = '[%s] %s' % (item['index'], item['index_title'])
        srcs.append(name)
        if 'av_id' in item:
            srcs.append('https://www.bilibili.com/video/av%s/' % item['av_id'])
        else:
            srcs.append(item['webplay_url'])
    try:
        for season in data['seasons']:
            srcs.append(season['title'])
            srcs.append('python:res_bilibili.load_item("bilibili://bangumi/season/%s")' % season['season_id'])
    except KeyError:
        pass
    result = {
        'name': data['bangumi_title'],
        'image': data['cover'],
        'summary': data['evaluate'],
        'players': [i['actor'] for i in data['actor']],
        'source': srcs
    }
    moonplayer.show_detail(result)
        
