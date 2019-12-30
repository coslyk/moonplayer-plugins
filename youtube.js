
var website_name = 'Youtube';

var appkey = 'AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo';
var pageTokens = [];


function serialize(obj) {
  var str = [];
  for(var p in obj)
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
}


// Search
function search(key, page) {
    var qs = {
        'q': key,
        'maxResults': 25,
        'safeSearch': 'none',
        'part': 'id,snippet',
        'type': 'video',
        'key': appkey
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
