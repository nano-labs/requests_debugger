# -*- coding: utf-8 -*-
u"""Arquivo de debug da biblioteca 'requests'.

Substitui a biblioteca requests em todo o projeto adicionando um _log_it()
aos metodos get, post, put e update.

Por se tratar de um hack apenas para debug sugiro remover esse arquivo de
produção.
"""

from sys import path
import imp

SHORT = 0  # Se diferente de 0 irá truncar a saída do log em X caracteres

# Varre todo o sys.path em busca da biblioteca requests
for i in path:
    try:
        r = imp.load_package("requests", i + "/requests")
        # Caso consiga achar a biblioteca salva uma cópia dos metodos
        # post, get, put e update
        _post = r.__getattribute__("post")
        _get = r.__getattribute__("get")
        _put = r.__getattribute__("put")
        _update = r.__getattribute__("update")
        # Pára a busca ao encontrar
        break
    except:
        pass


def _log_it(method, args, kwargs):
    u"""Printa de modo amigável todos os requests feitos."""
    url = kwargs.get("url")
    if not url:
        url = args[0]
        args = args[1:]
    args = ", " + ", ".join([str(i) for i in args]) if args else None
    kwargs = ", " + ", ".join(["%s=%s" % (str(i), str(j))
                               for i, j in kwargs.items()]) if args else None
    linha = '%s: %s%s%s' % (
             method.upper(), url, args or '', kwargs or '')
    if SHORT:
        linha = linha[:SHORT]
    print u"\033[91m%s\033[0m" % linha


def get(*args, **kwargs):
    u"""Printa os parametros de chama a cópia original do get."""
    _log_it("get", args, kwargs)
    return _get(*args, **kwargs)


def post(*args, **kwargs):
    u"""Printa os parametros de chama a cópia original do post."""
    _log_it("post", args, kwargs)
    return _post(*args, **kwargs)


def update(*args, **kwargs):
    u"""Printa os parametros de chama a cópia original do update."""
    _log_it("update", args, kwargs)
    return _update(*args, **kwargs)


def put(*args, **kwargs):
    u"""Printa os parametros de chama a cópia original do put."""
    _log_it("put", args, kwargs)
    return _put(*args, **kwargs)
