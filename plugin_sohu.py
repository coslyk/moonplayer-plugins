#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import json
from moonplayer_utils import convert_to_utf8, list_links
import moonplayer

## hosts
hosts = ('tv.sohu.com', 'my.tv.sohu.com')

pp_re = re.compile(r'&\\#(\d+);')
def json_pre_process(page):
    match = pp_re.search(page)
    while match:
        i = int(match.group(1))
        s = chr(i).decode('utf-8').encode('unicode-escape')
        page = page.replace(match.group(0), s)
        match = pp_re.search(page)
    return page


def parse(url, options):
    if url.startswith('http://tv.sohu.com/2'): #videos
        moonplayer.get_url(url, parse_cb, options)
    elif url.startswith('http://my.tv.sohu.com/'):
        vid = url.split('/')[-1].split('.')[0]
        url = 'http://my.tv.sohu.com/play/videonew.do?af=1&out=0&g=8&vid=' + vid
        moonplayer.get_url(url, parse_my_cb, (vid, options))
    else:
        moonplayer.warn('Wrong url')
        
## parse videos
vid_re = re.compile(r'vid\s?=\s?"(\d+)"')
plid_re = re.compile(r'playlistId="(\d*)"')
def parse_cb(page, options):
    vid_match = vid_re.search(page)
    plid_match = plid_re.search(page)
    if vid_match and plid_match:
        vid = vid_match.group(1)
        plid = plid_match.group(1)
        url = 'http://hot.vrs.sohu.com/vrs_flash.action?out=0&g=8&r=1&vid=%s&plid=%s' % (vid, plid)
        moonplayer.get_url(url, parse_cb2, (vid, plid, options))
    else:
        moonplayer.warn('Fail')

def parse_cb2(page, msg):
    vid, plid, options = msg
    page = json_pre_process(page)
    page = json.loads(page)
    data = page[u'data']
    #try other quality
    try:
        if not data:
            moonplayer.warn('解析失败！换个清晰度试试？')
            return
        elif options & moonplayer.OPT_QL_1080P and data[u'oriVid'] != 0:
            newvid = str(data[u'oriVid'])
        elif options & moonplayer.OPT_QL_SUPER and data[u'superVid'] != 0:
            newvid = str(data[u'superVid'])
        elif options & moonplayer.OPT_QL_HIGH and data[u'highVid'] != 0:
            newvid = str(data[u'highVid'])
        else:
            newvid = str(data[u'norVid'])
        if newvid != vid:
            vid = newvid
            url = 'http://hot.vrs.sohu.com/vrs_flash.action?out=0&g=8&r=1&vid=%s&plid=%s' % (vid, plid)
            moonplayer.get_url(url, parse_cb2, (vid, plid, options))
            return
    except KeyError:
        pass
    #parse
    su = data[u'su']
    ck = data[u'ck']
    ip = page[u'allot']
    name = data[u'tvName'].encode('UTF-8')
    tvid = page[u'tvid']
    files = [s.replace('http://data.vod.itc.cn', '') for s in data[u'clipsURL']]
    result = []
    i = 0
    #make cdnlist
    cdnlist = []
    for i in xrange(len(su)):
        cdnlist.append('http://%s/?prot=9&prod=flash&pt=1&file=%s&new=%s&key=%s&vid=%s&tvid=%s&rb=1' % (ip, files[i], su[i], ck[i], vid, tvid))
    data = {'result': [], 'cdnlist': cdnlist, 'name': name, 'options': msg[2]}
    moonplayer.get_url(cdnlist[0], parse_cdnlist, data)
    
# parse personal videos
def parse_my_cb(page, msg):
    vid, options = msg
    page = json_pre_process(page)
    page = json.loads(page)
    data = page[u'data']
    #try other quality
    try:
        if not data:
            moonplayer.warn('解析失败！换个清晰度试试？')
            return
        elif options & moonplayer.OPT_QL_1080P and data[u'oriVid'] != 0:
            newvid = str(data[u'oriVid'])
        elif options & moonplayer.OPT_QL_SUPER and data[u'superVid'] != 0:
            newvid = str(data[u'superVid'])
        elif options & moonplayer.OPT_QL_HIGH and data[u'highVid'] != 0:
            newvid = str(data[u'highVid'])
        else:
            newvid = str(data[u'norVid'])
        if newvid != vid:
            vid = newvid
            url = 'http://my.tv.sohu.com/play/videonew.do?af=1&out=0&g=8&vid=' + newvid
            moonplayer.get_url(url, parse_my_cb, (vid, options))
            return
    except KeyError:
        pass
    #parse
    su = data[u'su']
    ck = data[u'ck']
    ip = page[u'allot']
    tvid = page[u'tvid']
    name = data[u'tvName'].encode('UTF-8')
    files = [s.replace('http://data.vod.itc.cn', '') for s in data[u'clipsURL']]
    result = []
    i = 0
    #make cdnlist
    cdnlist = []
    for i in xrange(len(su)):
        cdnlist.append('http://%s/?prot=9&prod=flash&pt=1&file=%s&new=%s&key=%s&vid=%s&tvid=%s&rb=1' % (ip, files[i], su[i], ck[i], vid, tvid))
    data = {'result': [], 'cdnlist': cdnlist, 'name': name, 'options': msg[1]}
    moonplayer.get_url(cdnlist[0], parse_cdnlist, data)
    
def parse_cdnlist(page, data):
    result = data['result']
    cdnlist = data['cdnlist']
    url = str(json.loads(page)[u'url'])
    i = len(result) / 2
    result.append(data['name'] + '_' + str(i) + '.mp4') 
    result.append(url)
    i += 1
    if i < len(cdnlist):
        moonplayer.get_url(cdnlist[i], parse_cdnlist, data)
    elif data['options'] & moonplayer.OPT_DOWNLOAD:
        moonplayer.download(result, data['name'] + '.mp4')
    else:
        moonplayer.play(result)
        
