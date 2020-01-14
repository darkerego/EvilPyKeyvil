# EvilPyKeyvil
Badass Python3 Keylogger With Live WebSocket Stream &amp; HTTP Uploader

<p>This program is a pure python3 powered keylogger, which supports both live websocket streaming of keypresses back to a specified server, and periodic uploads of captchured keystrokes via HTTP post requests to a sprunge like server (included is a sample HTTP server for catching post requests as well as websocket client for captchuring live stream of keys.)
</p>

<p> EvilPyKeyvil is badass because you can see the victim type in real time via websocket. Because it is written purely in Python3, it can be packed into an executable with pyinstaller or py2exe for easy distribution.
</p>

* For Educational Use Only, of course *

## Check back soon for more info ... 

Readme is a WIP. Code is solid. 


### Features:
- Cross platform (linux/nt/darwin)
- Live key stream over websocket
- Periodic HTTP post uploader 
- Log to local file


### WebSocket Live KeyLog Stream

<pre>
{'time': '2020-01-13_15:29:32', 'key': "'t'"}
{'time': '2020-01-13_15:29:32', 'key': "'e'"}
{'time': '2020-01-13_15:29:32', 'key': "'s'"}
{'time': '2020-01-13_15:29:32', 'key': "'t'"}
{'time': '2020-01-13_15:29:32', 'key': "'t'"}
{'time': '2020-01-13_15:29:33', 'key': "'e'"}
{'time': '2020-01-13_15:29:33', 'key': "'s'"}
{'time': '2020-01-13_15:29:33', 'key': "'t'"}
{'time': '2020-01-13_15:29:38', 'key': "'l'"}
{'time': '2020-01-13_15:29:38', 'key': "'l'"}
{'time': '2020-01-13_15:29:39', 'key': "'o'"}
{'time': '2020-01-13_15:29:39', 'key': "'l'"}
{'time': '2020-01-13_15:30:06', 'key': 'Key.space'}
{'time': '2020-01-13_15:30:07', 'key': 'Key.space'}
{'time': '2020-01-13_15:30:08', 'key': 'Key.backspace'}
{'time': '2020-01-13_15:30:09', 'key': 'Key.left'}
{'time': '2020-01-13_15:30:09', 'key': 'Key.space'}
</pre>
