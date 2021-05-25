# -*- coding: utf-8 -*-
"""
Debug snipet for requests library.

Replaces the requests library adding some debug code on it.
"""

import sys
import json
from functools import wraps
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
import inspect
import requests

MAX_DEPTH = 3
LOG = "log"
CURL = "curl"
REQUESTS = PYTHON = "python"
VERBOSE_FORMAT = LOG


if sys.version_info.major >= 3:

    def reload(MODULE):
        import importlib

        importlib.reload(MODULE)


def requests_to_curl(method, url, *args, **kwargs):
    """Return the request as cURL string."""
    kwargs = args[1]
    headers = ['-H "%s:%s"' % (k, v) for k, v in list(kwargs.get("headers", {}).items())]
    cookies = ['-H "Cookie:%s=%s"' % (k, v) for k, v in list(kwargs.get("cookies", {}).items())]
    headers = " ".join(headers + cookies)
    params = urllib.parse.urlencode(kwargs.get("params", ""))

    body = kwargs.get("data") or kwargs.get("json")
    if isinstance(body, dict):
        body = json.dumps(body)
    body = "-d '%s'" % body if body else ""

    proxies = kwargs.get("proxies") or {}
    proxies = " ".join(["--proxy %s://%s" % (proto, uri) for proto, uri in list(proxies.items())])

    if params:
        url = "%s%s%s" % (url, "&" if "?" in url else "?", params)

    curl = """curl -i -X %(method)s %(proxies)s %(headers)s %(body)s '%(url)s'""" % {
        "url": url,
        "method": method.upper(),
        "headers": headers,
        "body": body,
        "proxies": proxies,
    }

    return curl


def requests_string(method, url, *args, **kwargs):
    """Return a string that contains a python requests call."""
    kwargs = args[1]
    args = args[0]
    args_string = (", %s" % ", ".join([i for i in args])) if args else ""
    kwargs_string = ", ".join(["%s=%s" % (k, v) for k, v in list(kwargs.items())])
    line = 'requests.%s("%s"%s, %s)' % (method, url, args_string, kwargs_string)
    return line


def log_string(method, url, *args, **kwargs):
    """Return a simple log string."""
    line = '%s - %s: %s %s %s' % (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        method.upper(),
        url,
        str(args),
        kwargs,
    )
    return line


def cprint(string, color):
    """Print a colored line."""
    color_code = {"red": 1, "gray": 0}.get(color, 0)
    print("\033[9%sm%s\033[0m" % (color_code, string))


def add_logger(func, output_format, max_depth):
    """Adiciona o print ao método."""

    @wraps(func)
    def logger(*args, **kwargs):
        """Printa de modo amigável todos os requests feitos."""
        _args = list(args)
        url = kwargs.get("url") or _args.pop(0)
        log_format = {
            "python": requests_string,
            "curl": requests_to_curl,
            "log": log_string,
        }.get(output_format) or log_string
        request_line = log_format(func.__name__, url, _args, kwargs)

        tabbing = ""
        if max_depth:
            code_point = inspect.currentframe().f_back
            arquivo = code_point.f_code.co_filename
            arquivo_linha = code_point.f_lineno
            track = [(arquivo, arquivo_linha)]
            while len(track) < max_depth:
                code_point = code_point.f_back
                if not code_point:
                    break
                arquivo = code_point.f_code.co_filename
                arquivo_linha = code_point.f_lineno
                if arquivo not in [i for i, j in track]:
                    track = [(arquivo, arquivo_linha)] + track

            for a, l in track:
                cprint("%s%s Line: %s" % (tabbing, a, l), "gray")
                tabbing += "  "

        cprint("%s%s" % (tabbing, request_line), "red")
        return func(*args, **kwargs)

    return logger


def _apply(output_format, max_depth):
    for inject_point in [requests, requests.Session]:
        for method in ["get", "post", "put", "patch", "delete"]:
            func = getattr(inject_point, "_%s" % method, getattr(inject_point, method))
            setattr(inject_point, "_%s" % method, func)
            logged_func = add_logger(func, output_format=output_format, max_depth=max_depth)
            setattr(inject_point, method, logged_func)


def set(output_format=VERBOSE_FORMAT, max_depth=MAX_DEPTH):
    """Defines output format and max depth.

    Args:
        output_format (str): Options are:
            requests_debugger.LOG
            requests_debugger.CURL
            requests_debugger.PYTHON
        max_depth (int): Defines how deep the file traceback should go.
            0 to disable.

    """
    _apply(output_format=output_format, max_depth=max_depth)


def unload():
    """Remove this debugger from requests lib by reloading it to its original."""
    reload(requests)


_apply(VERBOSE_FORMAT, MAX_DEPTH)
