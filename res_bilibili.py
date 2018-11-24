#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moonplayer
import json
import re

res_name = 'Bilibili - Bangumi'

tags = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
countries = ['All']

#appkey = '75cd10da32ffff6db8092783baaeafac23140b9fce0c8558'
appkey = '75cd10da32ffff6d39eb427d211acdcaca03a6866000e771' # Caught from bilibili's uwp client
appkey_short = '75cd10da32ffff6d'

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
    url = 'http://app.bilibili.com/x/v2/search/type?pn=1&ps=20&type=1&build=10110100&keyword=' + key
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
    url = 'https://www.bilibili.com/bangumi/play/ss' + season
    moonplayer.download_page(url, load_item_cb, None)

info_re = re.compile(r'"mediaInfo":{.*?"actors":"(.+?)".*?"cover":"(.+?)".*?"evaluate":"(.+?)".*?"title":"(.+?)"')
srcs_re = re.compile(r'"epList":(\[.+?\])')
def load_item_cb(content, data):
    # Infos
    match = info_re.search(content)
    if not match:
        moonplayer.warn('Bilibili: Fails to get bangumi info!')
        return
    actors, cover, summary, title = match.group(1, 2, 3, 4)
    actors = actors.split(r'\n')
    cover = cover.replace('\u002F', '/')

    # Urls
    match = srcs_re.search(content)
    if not match:
        moonplayer.warn('Bilibili: Parsing fails!')
        return
    data = json.loads(match.group(1))
    srcs = []
    for item in data:
        name = '[%s] %s' % (item['index'], item['index_title'])
        url = 'https://www.bilibili.com/bangumi/play/ep' + str(item['ep_id'])
        srcs.append(name)
        srcs.append(url)

    result = {
        'name': title,
        'image': cover,
        'summary': summary,
        'players': actors,
        'source': srcs
    }
    moonplayer.show_detail(result)
        
