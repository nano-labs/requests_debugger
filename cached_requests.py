# -*- coding: utf-8 -*-
u"""Camada de cache para requests."""

import requests
from requests import *
import cPickle as Pickle
from hashlib import md5
from config import CACHEDB
from pyutils.default_config import API_CACHE_TIME


def get_data(function, args, kwargs):
    u"""Abstração para pegar dados do cache ou remoto."""
    parametros = "%s_%s" % (args, sorted(kwargs.items()))
    cache_key = "%s_%s" % (function.__name__,
                           md5(parametros).hexdigest())
    cached_data = CACHEDB.get(cache_key)
    if cached_data:
        data = Pickle.loads(cached_data)
        return data
    data = function(*args, **kwargs)
    transaction = CACHEDB.pipeline()
    transaction.set(cache_key, Pickle.dumps(data))
    transaction.expire(cache_key, API_CACHE_TIME)
    transaction.execute()
    return data


def get(*args, **kwargs):
    u"""Post com cache."""
    return get_data(requests.get, args, kwargs)
