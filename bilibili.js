
var website_name = 'Bilibili';

var appkey = '75cd10da32ffff6d39eb427d211acdcaca03a6866000e771'; // Caught from bilibili's uwp client
var appkey_short = '75cd10da32ffff6d';


// Search
function search(key, page) {
    var url = 'http://app.bilibili.com/x/v2/search/type?pn=1&ps=20&type=1&build=10110100&keyword=' + key;
    moonplayer.get_content(url, function(content){
        var items = JSON.parse(content).data.items;
        var pr;
        try {
            if (items[0].cover.startsWith('//'))
                pr = 'http:';
            else
                pr = '';
        }
        catch (e) {
            pr = '';
        }
        var result = [];
        for (var i in items)
            result.push({title: items[i].title, url: convert_to_album_url(items[i].uri)});
        moonplayer.show_result(result);
    });
}


function convert_to_album_url(url) {
    var season;
    if (url.startsWith('bilibili://bangumi/season/'))
        season = url.replace('bilibili://bangumi/season/', '');
    else if (url.startsWith('/bangumi/i/'))
        season = url.replace('/bangumi/i/', '');
    else if (url.includes('/anime/'))
        season = url.split('/anime/')[1];
    else
        return url;
    season = season.replace(/\/$/, '');
    return 'https://www.bilibili.com/bangumi/play/ss' + season;
}

