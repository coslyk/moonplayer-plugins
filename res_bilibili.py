#!/usr/bin/env python
# -*- coding: utf-8 -*-

import moonplayer
import re
from HTMLParser import HTMLParser
from moonplayer_utils import list_links

res_name = 'Bilibili - Bangumi'

tags = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
countries = ['All']

## Explore
class ExploreResultParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [[], [], [], [], [], [], []]
        self.in_valid_link = False
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = {k:v for (k, v) in attrs}
        # Get the current day
        if tag == 'span' and 'class' in attrs and 'week-day-' in attrs['class']:
            self.day = int(attrs['class'].split('-')[-1])
        # Append a new item
        elif tag == 'a' and 'href' in attrs and 'bangumi.bilibili.com/anime' in attrs['href'] and 'class' in attrs:
            name = attrs['title']
            url = attrs['href']
            if url.startswith('//'):
                url = 'http:' + url
            if not url in self.urls:
                self.in_valid_link = True
                self.result[self.day].append({'name': name, 'url': url})
        # Add preview image
        elif self.in_valid_link and tag == 'img':
            url = attrs['src']
            if url.startswith('//'):
                url = 'http:' + url
            self.result[self.day][-1]['pic_url'] = url

    def handle_endtag(self, tag):
        if self.in_valid_link and tag == 'a':
            self.in_valid_link = False
            if 'pic_url' in self.result[self.day][-1]: # Add an item successfully
                self.urls.append(self.result[self.day][-1]['url'])
            else:
                del self.result[self.day][-1]

bangumi_list = None

def explore(tag, country, page):
    if bangumi_list == None:
        url = 'http://bangumi.bilibili.com/anime/timeline'
        moonplayer.download_page(url, explore_cb, tag)
    else:
        result = bangumi_list[tags.index(tag)]
        moonplayer.res_show(result)

def explore_cb(content, tag):
    global bangumi_list
    parser = ExploreResultParser()
    parser.feed(content.decode('UTF-8'))
    bangumi_list = parser.result
    result = bangumi_list[tags.index(tag)]
    moonplayer.res_show(result)


## Search
class SearchResultParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []
        self.left_img_div = False

    def handle_starttag(self, tag, attrs):
        attrs = {k:v for (k, v) in attrs}
        if tag == 'div' and 'class' in attrs and attrs['class'] == 'left-img':
            self.left_img_div = True
        elif self.left_img_div and tag == 'a' and 'bangumi.bilibili.com' in attrs['href']:
            name = attrs['title']
            url = attrs['href']
            if url.startswith('//'):
                url = 'http:' + url
            self.result.append({'name': name, 'url': url, 'pic_url': ''})
        elif self.left_img_div and tag == 'img':
            url = attrs['src']
            if url.startswith('//'):
                url = 'http:' + url
            self.result[-1]['pic_url'] = url

    def handle_endtag(self, tag):
        if self.left_img_div and tag == 'div':
            self.left_img_div = False

def search(key, page):
    key = key.replace(' ', '%20')
    url = 'http://search.bilibili.com/all?keyword=' + key
    moonplayer.download_page(url, search_cb, None)

def search_cb(content, data):
    parser = SearchResultParser()
    parser.feed(content)
    moonplayer.res_show(parser.result)


## Load item
def load_item(url):
    moonplayer.download_page(url, load_item_cb, None)

name_re = re.compile(r'''<meta property="og:title" content="(.+?)">''')
summary_re = re.compile(r'''<div class="info-desc">([^<]+?)</div>''')
image_re = re.compile(r'''<div class="bangumi-preview">\s*<img src="(.+?)"''')
def load_item_cb(content, data):
    result = {}
    match = name_re.search(content)
    if match:
        result['name'] = match.group(1)
    match = summary_re.search(content)
    if match:
        result['summary'] = match.group(1)
    match = image_re.search(content)
    if match:
        image = match.group(1)
        if image.startswith('//'):
            image = "http:" + image
        result['image'] = image
    # Get sources
    srcs = list_links(content, '//bangumi.bilibili.com/anime')
    for i in xrange(1, len(srcs), 2):
        srcs[i] = 'http:' + srcs[i]
    result['source'] = srcs
    moonplayer.show_detail(result)
