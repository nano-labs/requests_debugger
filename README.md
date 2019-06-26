# requests_debugger.py

This single file should be used to help in debugging your project that uses 'requests' lib


## Table of Contents
1. [Why Should I Use This?](#why-should-i-use-this?)
2. [When Should I NOT Use This?](#when-should-i-not-use-this)
3. [How To](#how-to)
4. [Features](#features)
5. [Usage](#usage)
    1. [Singleton module](#singleton-module)
    2. [Local module](#local-module)
    3. [Traceback feature](#traceback-feature)
    4. [Output formats](#output-formats)
    5. [Complex requests](#complex-requests)
    6. [Getting the standard 'requests' back](#getting-the-standard-requests-back)
6. [TODO](#todo)

## Why Should I Use This?

Because you are tired of setting breakpoints or 'print's into your code to figure out what requests for what urls your project is making.
I did this cause I'm on a project that makes a lot of requests for lots of diferente places using several layers of abstraction.
With this I figured that I make about 600 requests every time I run a full project test and that some views make up to 25 requests to get done. Now I'm refactoring my abstractions to make less requests and everybody is happy :)

## When Should I NOT Use This?

On your production environment. This guy is working fine but you dont need to insert this lame-hacking-failure-point into you production code, do you?


## How To
- Install with
```
pip install requests-debugger
```

-Then just import this lib with

```python
import requests_debugger
```
See the [Usage](#usage) section for more information

#### But remember:

Do not use it on production. I love this little hack but IT'S NOT NEEDED FOR PRODUCTION


## Features

- Print out EVERY request you make using 'requests' lib
- Print usable strings for debug
- Traceback every requests call

# Usage:

### Singleton module:
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

### Local module
- You also can import just for that namespace or when you already have 'requests' imported

```python
>>> from requests_debugger import requests
>>> requests.get("http://test.com")
/Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/terminal/interactiveshell.py Line: 431
  /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/core/interactiveshell.py Line: 2881
    <ipython-input-2-f2de511e6e5e> Line: 1
      2017-02-20 16:36:39 - GET: http://test.com ([], {}) {}
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
>>> import requests_debugger
>>> requests_debugger.set(max_depth=0)
>>> whatever()
2017-02-20 15:03:51 - GET: http://test.com ([], {}) {}
```

- Or make it deeper:

```python
>>> import requests_debugger
>>> requests_debugger.set(max_depth=10)
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

### Output formats
- The default output is 'LOG' format but you also have the useful python code output that you may just copy/paste to make that same request again.

```python
>>> import requests
>>> import requests_debugger
>>> requests_debugger.set(output_format=requests_debugger.PYTHON, max_depth=0)
>>> from example.do_something import whatever
>>> whatever()
requests.get("http://test.com", )
# Copy that output then just paste it back on python console
>>> response = requests.get("http://test.com", )
requests.get("http://test.com", )
>>> response
<Response [463]>
```

- Or cURL command that you may past on your terminal

```python
>>> import requests_debugger
>>> from example.do_something import whatever
>>> requests_debugger.set(output_format=requests_debugger.CURL, max_depth=0)
>>> whatever()
curl -i -X GET    'http://test.com'
```
Then past on your terminal:
```shell
$ curl -i -X GET    'http://test.com'
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.9.15
Date: Mon, 20 Feb 2017 18:31:08 GMT
Content-Type: text/html
Content-Length: 161
Connection: keep-alive
Keep-Alive: timeout=20
Location: https://www.test.com/

<html>
<head><title>302 Found</title></head>
<body bgcolor="white">
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.9.15</center>
</body>
</html>
```

### Complex requests
- More complex requests are also translated to cURL ou python code
```python
>>> import requests_debugger
>>> import requests
>>> requests_debugger.set(output_format=requests_debugger.CURL, max_depth=0)
>>> requests.post("http://test.com", data={"foo": "bar"}, headers={"Authorization": "Basic IUYihda", 'content-type': 'application/json'}, proxies={"http": "http://proxy.com"}, cookies={"bar": "foo"})
curl -i -X POST --proxy http://http://proxy.com -H "content-type:application/json" -H "Authorization:Basic IUYihda" -H "Cookie:bar=foo" -d '{"foo": "bar"}' 'http://test.com'
<Response [200]>
>>> requests_debugger.set(output_format=requests_debugger.PYTHON)
>>> requests.post("http://test.com", data={"foo": "bar"}, headers={"Authorization": "Basic IUYihda", 'content-type': 'application/json'}, proxies={"http": "http://proxy.com"}, cookies={"bar": "foo"})
requests.post("http://test.com", headers={'content-type': 'application/json', 'Authorization': 'Basic IUYihda'}, cookies={'bar': 'foo'}, proxies={'http': 'http://proxy.com'}, data={'foo': 'bar'})
<Response [200]>
```

### Getting the standard 'requests' back
- use unload() method
```python
>>> import requests_debugger
>>> import requests
>>> requests.get("http://test.com")
/Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/terminal/interactiveshell.py Line: 431
  /Users/nano/envs/bbb/lib/python2.7/site-packages/IPython/core/interactiveshell.py Line: 2881
    <ipython-input-3-f2de511e6e5e> Line: 1
      2017-02-20 15:37:36 - GET: http://test.com ([], {}) {}
<Response [463]>
>>> requests_debugger.unload()
>>> requests.get("http://test.com")
<Response [463]>
```

## TODO:
- Translate requests' 'auth' argument to cURL headers
