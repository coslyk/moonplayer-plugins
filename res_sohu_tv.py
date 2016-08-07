#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moonplayer
import re
from moonplayer_utils import list_links

res_name = '电视剧 - 搜狐'

tags_table = {'全部': '',    '偶像': '101100', '家庭': '101101', '历史': '101102',
            '年代': '101103', '言情': '101104', '武侠': '101105', '古装': '101106',
            '都市': '101107', '农村': '101108', '军旅': '101109', '刑侦': '101110',
            '喜剧': '101111', '悬疑': '101112', '情景': '101113', '传记': '101114',
            '科幻': '101115', '动画': '101116', '动作': '101117', '真人': '101118',
            '栏目': '101119', '谍战': '101120', '伦理': '101121', '战争': '101122',
            '神话': '101123', '惊悚': '101124', '剧情': '101127'}
tags = ['全部', '偶像', '家庭', '历史', '年代', '言情', '武侠', '古装', '都市', '农村',
              '军旅', '刑侦', '喜剧', '悬疑', '情景', '传记', '科幻', '动画', '动作', '真人',
              '栏目', '谍战', '伦理', '战争', '神话', '惊悚', '剧情']

countries_table = {'全部': '', '内地': '1000', '香港': '1001', '台湾': '1002', '美国': '1003',
                          '日本': '1004', '韩国': '1015', '英国': '1007', '泰国': '1006', '其他': '1014'}
countries = ['全部', '内地', '香港', '台湾', '美国', '日本', '韩国', '英国', '泰国', '其它']

def explore(tag, country, page):
    tag_id = tags_table[tag]
    country_id = countries_table[country]
    url = 'http://so.tv.sohu.com/list_p1101_p2%s_p3%s_p40_p5_p6_p77_p80_p9_2d1_p10%i_p11_p12_p13.html' % \
           (tag_id, country_id, page)
    moonplayer.download_page(url, explore_cb, None)
    
img_re = re.compile(r'''<a\s[^>]*?href=['"](http://tv.sohu.com/item/.+?)['"][^>]*?>\s*<img\s[^>]*?src=['"](.+?)['"]''')
def explore_cb(page, data):
    #page = page.replace('\n', '')
    dict_url_img = {}
    match = img_re.search(page)
    while match:
        url, img = match.group(1, 2)
        dict_url_img[url] = img
        match = img_re.search(page, match.end(0))
    result = list_links(page, 'http://tv.sohu.com/item/')
    items = []
    for i in xrange(0, len(result), 2):
        name = result[i]
        url = result[i+1]
        pic_url = dict_url_img[url]
        item = {'name': name, 'url': url, 'pic_url': pic_url}
        items.append(item)
    moonplayer.res_show(items)

def search(key, page):
    url = 'http://so.tv.sohu.com/mts?box=1&wd=' + key
    moonplayer.download_page(url, search_cb, None)
    
search_cb = explore_cb
    
def load_item(url):
    moonplayer.download_page(url, load_item_cb, None)
    
pic_re = re.compile(r'''<img src=['"](.+?)['"]''')
name_re = re.compile(r'''<span class=['"]vname['"]>(.+?)</span>''')
name_re2 = re.compile(r'''电影：(.+?)<span>''')
date_re = re.compile(r'''<span>上映时间：</span>(.+?)</li>''')
alt_name_re = re.compile(r'''<span>别名：</span>(.+?)</li>''')
director_re = re.compile(r'''<span>导演：</span><a href=['"].+?['"][^>]*?>(.+?)</a>''')
nation_re = re.compile(r'''<span>地区：</span><a href=['"].+?['"][^>]*?>(.+?)</a>''')
rating_re = re.compile(r'''<strong class=['"]score['"]>(.+?)</strong>''')
summary_re = re.compile(r'''<span class=['"]full_intro\s*['"][^>]*>(.+?)</span>''')
def load_item_cb(page, data):
    result = {}
    # Picture
    try:
        match = pic_re.search(page.split('drama-pic')[1])
    except IndexError:
        match = pic_re.search(page.split('movie-pic')[1])
    if match:
        result['image'] = match.group(1)
    # Name
    match = name_re.search(page)
    if match:
        result['name'] = match.group(1)
    # Rating
    match = rating_re.search(page)
    if match:
        result['rating'] = float(match.group(1))
    # Nation / Region
    match = nation_re.search(page)
    if match:
        result['nations'] = [match.group(1)]
    # Date
    match = date_re.search(page)
    if match:
        result['dates'] = match.group(1).split('/')
    # Director
    match = director_re.search(page)
    if match:
        result['directors'] = match.group(1).split('/')
    # Alternative names
    match = alt_name_re.search(page)
    if match:
        result['alt_names'] = match.group(1).split('/')
    # Summary
    match = summary_re.search(page)
    if match:
        result['summary'] = match.group(1).replace('&nbsp;', ' ')
    # Videos' urls
    result['source'] = list_links(page, 'http://tv.sohu.com/2')
    moonplayer.show_detail(result)
