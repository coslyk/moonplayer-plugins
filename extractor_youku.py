#!/usr/bin/env python

import json

# Extractor version
extractor_version = 1

# Catch this url
url_pattern = r'.+?acs\.youku\.com/h5/mtop\.youku\.play\.ups\.appinfo\.get.+ckey.+'

# Parse the result
def parse(data):
    data = data[ data.find('(') + 1 : -1 ]
    data = json.loads(data)['data']['data']
    title = data['video']['title']
    streams = []
    for s in data['stream']:
        urls = []
        for seg in s['segs']:
            if 'cdn_url' in seg:
                urls.append(seg['cdn_url'])
        item = {
            'type': s['stream_type'],
            'srcs': urls
        }
        streams.append(item)
        
    result = {
        'title': title,
        'streams': streams
    }
    return result

