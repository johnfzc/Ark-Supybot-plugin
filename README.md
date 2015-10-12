# Installation

Install the python-valve library using pip. Be sure to use the appropriate version of pip/python for your Supybot instance:

```
pip3 install git+https://github.com/PhilipCammarata/python-valve.git
```

Download the plugin from github and place in your Supybot / Limnoria plugins directory.

# Configuration

You need to configure the serverDetails variable with the DNS name or IP of your Ark server in plugin.py, line 59:

```
serverDetails=("arkserver.example.com",34001)
```

# Known Issues

Some Ark servers do not response to the ServerQuerier A2S request. I do not know why this is but the server I use doesn't have this issue. If you know why this happens or how to fix it please let me know.

# ToDo

* Configuration should be implemented using a proper configuration server
* Users should be able to query an arbitrary ark server by specifying the name and IP on the command line