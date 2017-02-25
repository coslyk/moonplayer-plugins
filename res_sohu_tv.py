#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moonplayer
import re
import json
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
countries_table = {'全部': '', '内地': '5', '香港': '6', '台湾': '7', '韩国': '8',
                          '美国': '9', '英国': '10', '泰国': '11', '日本': '15', '其他': '100'}
countries = ['全部', '内地', '香港', '台湾', '韩国', '美国', '英国', '泰国', '日本', '其它']


sohu_apikey = '1820c56b9d16bbe3381766192e134811' # caught from sohu's uwp client
sohu_partner = 419


def explore(tag, country, page):
    tag_id = tags_table[tag]
    country_id = countries_table[country]
    if page == 1:
        url = 'http://api.tv.sohu.com/v6/mobile/classificationScreening/list.json?sub_channel_id=1010000&cid=2&cursor=0&page_size=10&ugc=1&plat=12&sver=3.7.0&partner=419&api_key=%s&o=1&cat=%s&area=%s&year=' % \
           (sohu_apikey, tag_id, country_id)
    else:
        url = '%soffset=%i&page_size=20&ugc=1&plat=12&sver=3.7.0&partner=419&api_key=%s' % (sohu_more_list, sohu_offset + (page-2)*20, sohu_apikey)
    moonplayer.download_page(url, explore_cb, None)

def explore_cb(page, data):
    global sohu_cached_info
    global sohu_more_list
    global sohu_offset
    data = json.loads(page)['data']
    try: # first page
        data_list = data['columns'][0]['data_list']
        sohu_offset = len(data_list)
        sohu_more_list = data['columns'][0]['more_list']
    except KeyError: # not first page
        data_list = data['videos']
    sohu_cached_info = {str(i['aid']): i for i in data_list}
    result = [{'name': i['album_name'], 'url': str(i['aid']), 'pic_url': i['ver_big_pic']} for i in data_list]
    moonplayer.res_show(result)



def search(key, page):
    key = key.replace(' ', '+')
    url = 'http://m.so.tv.sohu.com/search/keyword?key=%s&page=%i&page_size=30&pay=1&pgc=1&plat=12&sver=3.7.0&partner=419&api_key=%s' % (key, page, sohu_apikey)
    moonplayer.download_page(url, search_cb, None)

def search_cb(content, data):
    global sohu_cached_info
    items = json.loads(content)['data']['items']
    albums = []
    for i in items:
        if 'aid' in i and 'is_album' in i and i['is_album'] == 1:
            albums.append(i)
    sohu_cached_info = {str(i['aid']): i for i in albums}
    result = [{'name': i['album_name'], 'url': str(i['aid']), 'pic_url': i['ver_big_pic']} for i in albums]
    moonplayer.res_show(result)

    
def load_item(aid):
    info = sohu_cached_info[aid]
    result = {
        'name':      info['album_name'],
        'summary':   info['album_desc'] if 'album_desc' in info else info['desc'] if 'desc' in info else '',
        'rating':    info['score'] if 'score' in info else '',
        'image':     info['ver_high_pic'],
        'nations':   info['area'].split(',') if 'area' in info else '',
        'directors': info['director'].split(',') if 'director' in info else '',
        'players':   info['main_actor'].split(',') if 'main_actor' in info else ''
    }
    url = 'http://s1.api.tv.itc.cn/v4/album/videos/%s.json?page=1&page_size=500&site=1&plat=12&sver=3.7.0&partner=419&api_key=%s' % (aid, sohu_apikey)
    moonplayer.download_page(url, load_item_cb, result)
    
def load_item_cb(page, result):
    videos = json.loads(page)['data']['videos']
    srcs = []
    for i in videos:
        srcs.append(i['video_name'])
        srcs.append(i['url_html5'])
    result['source'] = srcs
    moonplayer.show_detail(result)
    
