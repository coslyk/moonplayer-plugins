
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
            result.push({title: items[i].title, url: items[i].uri});
        moonplayer.show_result(result);
    });
}


// Load item
/*
var title_re = /"mediaInfo":{.*?"title":"(.+?)"/
var summary_re = /"evaluate":"(.+?)"/
var cover_re = /"cover":(".+?")/
var srcs_re = /"epList":(\[.*?\])/

function load_item(url) {
    var season;
    if (url.startsWith('bilibili://bangumi/season/'))
        season = url.replace('bilibili://bangumi/season/', '');
    else if (url.startsWith('/bangumi/i/'))
        season = url.replace('/bangumi/i/', '');
    else if (url.includes('/anime/'))
        season = url.split('/anime/')[1];
    else {
        moonplayer.warning('Bilibili: Cannot open url:' + url);
        return;
    }
    season = season.replace(/\/$/, '');
    url = 'https://www.bilibili.com/bangumi/play/ss' + season;
    moonplayer.get_content(url, function(content){
        // Infos
        var match;
        if ((match = title_re.exec(content)) === null) {
            moonplayer.warning('Bilibili: Fails to get bangumi info!');
            return;
        }
        var title = match[1];
        if ((match = summary_re.exec(content)) === null) {
            moonplayer.warning('Bilibili: Fails to get bangumi info!');
            return;
        }
        var summary = match[1];
        if ((match = cover_re.exec(content)) === null) {
            moonplayer.warning('Bilibili: Fails to get bangumi info!');
            return;
        }
        var cover = JSON.parse(match[1]);
        if (!cover.startsWith('http'))
            cover = 'http:' + cover;
        // Urls
        if ((match = srcs_re.exec(content)) === null) {
            moonplayer.warning('Bilibili: Parsing fails!');
            return;
        }
        var items = JSON.parse(match[1]);
        var srcs = [];
        for (i in items) {
            var name = "[" + items[i].title + "] " + items[i].longTitle;
            var url = 'https://www.bilibili.com/bangumi/play/ep' + items[i].id;
            srcs.push(name);
            srcs.push(url);
        }
        
        // Result
        var result = {
            name: title,
            image: cover,
            summary: summary,
            source: srcs
        };
        moonplayer.show_detail(result);
    });
}*/

