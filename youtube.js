
var website_name = 'Youtube';

var website_description = '\
    <p>Welcome to Youtube!<p>\
    <p>\
        Before using, you need to\
        <a href="plugin:set-api-key">set Youtube API Key</a>\
        first.\
    </p>\
    <p>\
        <a href="https://www.slickremix.com/docs/get-api-key-for-youtube/">How to get the API Key?</a>\
    </p>'

    
// Don't crash in old version
var api_key = moonplayer.get_configuration !== undefined ? moonplayer.get_configuration('api_key') : undefined;
var pageTokens = [];


function serialize(obj) {
  var str = [];
  for(var p in obj)
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
}


// Search
function search(key, page) {
    if (key === 'plugin:set-api-key') {
        set_api_key();
        return;
    }

    if (api_key === undefined) {
        moonplayer.warning('Please set the API key first!');
        return;
    }

    var qs = {
        'q': key,
        'maxResults': 25,
        'safeSearch': 'none',
        'part': 'id,snippet',
        'type': 'video',
        'key': api_key
    };
    if (page === 1)
        pageTokens = ['', ''];
    else if (page < pageTokens.length)
        qs['pageToken'] = pageTokens[page];
    else {
        moonplayer.warning("Cannot skip page due to the limitation of Youtube's API.");
        return;
    }
    var url = 'https://www.googleapis.com/youtube/v3/search?' + serialize(qs);
    moonplayer.get_content(url, function(content) {
        var data = JSON.parse(content);
        var result = [];
        for (var i in data.items) {
            var item = data.items[i];
            var t = {
                title: item.snippet.title,
                url: 'https://www.youtube.com/watch?v=' + item.id.videoId
            };
            result.push(t);
        }
        if (page + 1 === pageTokens.length && 'nextPageToken' in data)
            pageTokens.push(data.nextPageToken);
        moonplayer.show_result(result);
    });
}

// Set API key
function set_api_key() {
    if (api_key !== undefined) {
        if (!moonplayer.question('API Key is already set. Do you want to reset it?')) {
            return;
        }
    }
    var new_key = moonplayer.get_text('Please enter a new API Key:');
    if (new_key !== '') {
        api_key = new_key;
        moonplayer.set_configuration('api_key', api_key);
    }
}