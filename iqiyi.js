
var website_name = 'Iqiyi';

// Search
function search(key, page) {
    var url = 'https://so.iqiyi.com/so/q_' + key;
    moonplayer.get_content(url, function(content) {
        var result = list_links(content, "http://www.iqiyi.com/lib/m_");
        moonplayer.show_result(result);
    });
}


function list_links(content, prefix) {
    var re1 = /<a\s.*?href="(.+?)"\s.*?title="(.+?)"/g;
    var re2 = /<a\s.*?title="(.+?)"\s.*?href="(.+?)"/g;
    var match;
    var result = [];
    var urls = []

    while ((match = re1.exec(content)) !== null) {
        if (match[1].startsWith(prefix) && !urls.includes(match[1])) {
            urls.push(match[1]);
            result.push({ title: match[2], url: match[1] });
        }
    }
    
    while ((match = re2.exec(content)) !== null) {
        if (match[2].startsWith(prefix) && !urls.includes(match[2])) {
            urls.push(match[2]);
            result.push({ title: match[1], url: match[2] });
        }
    }

    return result;
}
