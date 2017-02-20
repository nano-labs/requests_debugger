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

### Traceback feature
- Let's say that you have some models, APIs, libs, etc that internally uses 'requests' lib. You don't know when, where or why but it does. Just import the requests_debugger before anything else and it will traceback the request to you.

```python
>>> import requests_debugger
>>> from example.do_something import whatever
>>> whatever()
example/do_something.py Line: 8
  example/file_b.py Line: 8
    example/file_a.py Line: 10
      2017-02-20 15:01:03 - GET: http://test.com ([], {}) {}
```

- But you may disable this, if you want:

```python
>>> requests_debugger.MAX_DEPTH = 0
>>> whatever()
2017-02-20 15:03:51 - GET: http://test.com ([], {}) {}
```

- Or make it deeper:

```pycon
>>> requests_debugger.MAX_DEPTH = 10
>>> whatever()
/Users/nano/envs/bbb/bin/ipython Line: 11
  /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/__init__.py Line: 119
    /Users/nano/envs/bbb/lib/python2.7/site-packages/traitlets/config/application.py Line: 658
      /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/terminal/ipapp.py Line: 348
        /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/terminal/interactiveshell.py Line: 431
          /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/core/interactiveshell.py Line: 2881
            <ipython-input-7-ad0274cf4d97> Line: 1
              example/do_something.py Line: 8
                example/file_b.py Line: 8
                  example/file_a.py Line: 10
                    2017-02-20 15:05:09 - GET: http://test.com ([], {}) {}

```
