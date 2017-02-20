# requests_debugger.py

This single file should be used to help in debugging your project that uses 'requests' lib


## Why Should I Use This?

Because you are tired of setting breakpoints or 'print's into your code to figure out what requests for what urls your project is making.
I did this cause I'm on a project that makes a lot of requests for lots of diferente places using several layers of abstraction.
With this I figured that I make about 600 requests every time I run a full project test and that some views make up to 25 requests to get done. Now I'm refactoring my abstractions to make less requests and everybody is happy :)

## When Should I NOT Use This?

On your production environment. This guy is working fine but you dont need to insert this lame-hacking failure point into you production code.


## How To

Just put this file on your project root directory and ALL your 'requests' imports will import this guy

### But remeber:

Remove it before commit to production. I love this little hack but IT'S NOT SAFE FOR PRODUCTION


## Features

- Print out EVERY request you make using 'requests' lib
- Print usable strings for debug
- Traceback every requests call

# Usage:

### Singleton requests:
- As Python's modules are singleton if you import 'requests_debbuger' and then import 'requests' it will not re-import 'requests' but just set the requests_debugger's 'request' module into your namespace. Therefore all your requests will have the debugger feature.

```python
>>> import requests_debugger
>>> import requests
>>> requests.get("http://test.com")
/Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/terminal/interactiveshell.py Line: 431
  /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/core/interactiveshell.py Line: 2881
    <ipython-input-3-f2de511e6e5e> Line: 1
      2017-02-20 14:48:16 - GET: http://test.com ([], {}) {}
<Response [463]>
```
