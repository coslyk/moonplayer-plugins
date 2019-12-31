MoonPlayer plugins
==========
Plugins used in MoonPlayer.

Usage
----
Right click in MoonPlayer window, and click "Upgrade plugins". Plugins will be automatically downloaded / upgraded.

The plugins are stored under:
 * Windows: `C:\Users\username\AppData\Local\MoonPlayer\plugins`
 * macOS: `~/Library/Application Support/MoonPlayer/plugins`
 * Linux: `~/.local/share/moonplayer/plugins`
 

Supported video websites
----
* Bilibili (bilibili.js)
* Youtube (youtube.js)

For developers
----
You can easily write plugins for MoonPlayer. This is the basic structure:
```
// You need to specify the website name. This will be shown in MoonPlayer.
var website_name = 'Youtube';


// You need to define this function for video search
function search(key, page) {

    // You can use following APIs provided by moonplayer:
    
    // get_content() can be used to download data:
    moonplayer.get_content(url, function(content){
        // do something.
        // "content" is the downloaded data.
    });
    
    // post_content() can be used to upload data:
    moonplayer.post_content(url, data, function(content){
        // do something...
        // "content" is the data returned by server.
    });
    
    // warning() shows a warning dialog:
    moonplayer.warning("Naive!");
    
    // question() shows a question dialog with yes/no button:
    if (moonplayer.question("Are you ok?")) {
        // do something...
    }
    
    // At least, you need to call show_result() to show the seach result on MoonPlayer:
    var result = [
        { title: "item 1", url: "url 1" },
        { title: "item 2", url: "url 2" }
    ];
    moonplayer.show_result(result);
}
```
