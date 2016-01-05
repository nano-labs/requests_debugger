# -*- coding: utf-8 -*-
u"""Arquivo de debug da biblioteca 'requests'.

Substitui a biblioteca requests em todo o projeto adicionando um _log_it()
aos metodos get, post, put.
"""

import hashlib
import requests
import inspect
import simplejson as json
import pickle
from functools import wraps
from redis import Redis

try:
    from custom_config import REQUEST_DEBUGGER_SHORT as SHORT
except:
    SHORT = 160
MAX_DEPTH = 2
TRACK = True
ENABLE_CACHE = False
DEFAULT_EXPIRE_TIME = 300  # Segundos. Usado caso não exista de cache-control
cache = Redis(host="127.0.0.1", port=6379, db=1, socket_timeout=1)


def add_logger(func):
    u"""Adiciona o print ao método."""
    @wraps(func)
    def logger(*args, **kwargs):
        u"""Printa de modo amigável todos os requests feitos."""
        _args = args
        url = kwargs.get("url")
        if not url:
            url = _args[0]
            _args = _args[1:]
        linha = '%s: %s %s %s' % (
                 func.func_name.upper(), url, str(_args), kwargs)
        if SHORT:
            linha = linha[:SHORT]

        tabbing = ""
        if TRACK:
            code_point = inspect.currentframe().f_back
            arquivo = code_point.f_code.co_filename
            arquivo_linha = code_point.f_lineno
            track = [(arquivo, arquivo_linha)]
            while len(track) < MAX_DEPTH:
                code_point = code_point.f_back
                arquivo = code_point.f_code.co_filename
                arquivo_linha = code_point.f_lineno
                if arquivo not in [i for i, j in track]:
                    track = [(arquivo, arquivo_linha)] + track
                if arquivo.endswith("app.py"):
                    break

            for a, l in track:
                print "\033[90m%s'%s' Linha: %s\033[0m" % (tabbing, a, l)
                tabbing += "  "

        if ENABLE_CACHE and func.func_name == "get":
            cache_key = hashlib.md5(json.dumps([args, kwargs])).hexdigest()
            data = cache.get(cache_key)
            if data:
                print u"%s\033[91mCACHED %s\033[0m" % (tabbing, linha)
                data = pickle.loads(data)
            else:
                print u"%s\033[91m%s\033[0m" % (tabbing, linha)
                data = func(*args, **kwargs)
                cache.set(cache_key, pickle.dumps(data))
                cache_time = DEFAULT_EXPIRE_TIME
                cache_control = data.headers.get('cache-control')
                if cache_control and "max-age" in cache_control:
                    cache_time = int(cache_control.split("max-age=")[1].split(",")[0])
                cache.expire(cache_key, cache_time)
            return data

        print u"%s\033[91m%s\033[0m" % (tabbing, linha)
        return func(*args, **kwargs)

    return logger


for method in ["get", "post", "put"]:
    func = getattr(requests, method)
    logged_func = add_logger(func)
    setattr(requests, method, logged_func)
