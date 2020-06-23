
var website_name = 'Bilibili';

var website_description = '\
    <p>哔哩哔哩 ~ 干杯！<p>\
    <p>浏览最新番剧：</p>\
    <p>\
        <a href="plugin:bangumi-latest">最新</a>&nbsp;\
        <a href="plugin:bangumi-sun">周日</a>&nbsp;\
        <a href="plugin:bangumi-mon">周一</a>&nbsp;\
        <a href="plugin:bangumi-tue">周二</a>&nbsp;\
        <a href="plugin:bangumi-wed">周三</a>&nbsp;\
        <a href="plugin:bangumi-thu">周四</a>&nbsp;\
        <a href="plugin:bangumi-fri">周五</a>&nbsp;\
        <a href="plugin:bangumi-sat">周六</a>&nbsp;\
    </p>'


// Search
function search(key, page) {
    // Show bangumi list
    if (key.startsWith('plugin:')) {
        explore(key);
        return;
    }

    var url = 'http://app.bilibili.com/x/v2/search/type?pn=1&ps=20&type=1&build=10110100&keyword=' + key;
    moonplayer.get_content(url, function(content) {
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


// Bangumi list
var bangumi_list = null;
var latest_bangumis = [];

function explore(command) {
    var day;
    switch (command) {
        case 'plugin:bangumi-latest': day = -1; break;
        case 'plugin:bangumi-sun': day = 0; break;
        case 'plugin:bangumi-mon': day = 1; break;
        case 'plugin:bangumi-tue': day = 2; break;
        case 'plugin:bangumi-wed': day = 3; break;
        case 'plugin:bangumi-thu': day = 4; break;
        case 'plugin:bangumi-fri': day = 5; break;
        case 'plugin:bangumi-sat': day = 6; break;
        default: moonplayer.warning('Unknown command.'); return;
    }

    if (bangumi_list !== null) {
        // Show list
        if (day === -1) {
            moonplayer.show_result(latest_bangumis);
        } else {
            moonplayer.show_result(bangumi_list[day]);
        }
    } else {
        // Init bangumi list
        url = 'https://api.bilibili.com/pgc/web/timeline/v2?season_type=1';
        moonplayer.get_content(url, function(content) {
            var data = JSON.parse(content).result;
            var weekdays = data.timeline;
            var latest = data.latest;
            bangumi_list = [[], [], [], [], [], [], []];
            
            for (var i in weekdays) {
                var episodes = weekdays[i].episodes;
                for (var j in episodes) {
                    bangumi_list[i].push({
                        title: episodes[j].title,
                        url: 'https://www.bilibili.com/bangumi/play/ss' + episodes[j].season_id
                    });
                }
            }

            for (var i in latest) {
                latest_bangumis.push({
                    title: latest[i].title,
                    url: 'https://www.bilibili.com/bangumi/play/ss' + latest[i].season_id
                });
            }

            // Show list
            if (day === -1) {
                moonplayer.show_result(latest_bangumis);
            } else {
                moonplayer.show_result(bangumi_list[day]);
            }
        });
    }
}

