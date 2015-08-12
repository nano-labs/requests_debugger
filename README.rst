requests.py
===========

This single file should be used to help in debugging your project that uses 'requests' lib


Why Should I Use This?
----------------------

Because you are tired of setting breakpoints or 'print's into your code to figure out what requests for what urls your project is making.
I did this cause I'm on a project that makes a lot o requests for lots of diferente places.
With this I figured that I make about 300 requests every time I run a full project 'behave' test and that some views make up to 25 requests to get done. Now I'm refactoring my abstractions to make less requests and everybody is happy :)

When Should I NOT Use This?
---------------------------

On your production environment. This guy is working fine but you dont need to insert this lame-hacking failure point into you production code.


How To
------

Just put this file on your project root directory and ALL your 'requests' imports will import this guy

But remeber:
""""""""""""

Remove it before commit to production. I love this little hack but IT'S NOT SAFE FOR PRODUCTION


Features
--------

- Print out EVERY request you make using 'requests' lib
