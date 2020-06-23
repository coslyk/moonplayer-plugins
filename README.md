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
* Iqiyi (iqiyi.js)
* Youtube (youtube.js)

For developers
----

You can easily write plugins for MoonPlayer. This is the basic structure:

```
// You need to specify the website name. This will be shown in MoonPlayer.
var website_name = 'Youtube';


// You need to define this function for video search
function search(keyword, page) {
    do_something();

    // At least, you need to call show_result() to show the seach result on MoonPlayer:
    var result = [
        { title: "item 1", url: "url 1" },
        { title: "item 2", url: "url 2" }
    ];
    moonplayer.show_result(result);
}
```

For details please visit [API Reference](https://github.com/coslyk/moonplayer-plugins/wiki/API-Reference).

To publish your plugins, just make a pull request to this repository. Your plugins will be pushed to all MoonPlayer users.
