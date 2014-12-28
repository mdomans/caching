#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

.. module:: decorators
   :platform: Unix, Windows, Linux
   :synopsis: Decorators for simpler work with cache
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""

import functools
from tools import make_key, make_group_value


class CacheDecorator(object):
    """

    Decorator for work with multiple groups for each key
     
    cached = cached_factory(cache_client)

    @cached
    def something():
        return 1

    or

    @cached(timeout=10)
    def something():
        return 1

    @cached(timeout=10, jitter=True)
    def something():
        return 1

    supports every possible cache client
    
    """
    group_keys = []

    def __call__(self, key=None, group_keys=None, group_key=None):
        def decorate_func(fn):
            @functools.wraps(fn)
            def decorates_args(*args, **kwargs):
                self.key = key
                self.group_keys = group_keys or []
                if group_key:
                    self.group_keys.append(group_key)
                result = self.run_decorated(fn, *args, **kwargs)
                return result

            return decorates_args

        return decorate_func


    def __init__(self, cache_client):
        self.cache = cache_client
        self.key = ''

    def expire_key(self, key):
        self.cache.set(make_key(key), None)

    def run_decorated(self, func, *args, **kwargs):
        if self.key:
            key = make_key(self.key)
        else:
            key = make_key(repr(func), repr(args), repr(kwargs))
        group_keys = map(make_key, self.group_keys)
        cache = self.cache
        value = None
        evaluate = False
        if group_keys:
            data = cache.get_multi(group_keys + [key])
            data_dict = data.get(key)
            if (not data) or (not data_dict):
                evaluate = True
            if data_dict:
                value = data_dict['value']
                for group_key in group_keys:
                    if group_key not in data or group_key not in data_dict or data[group_key] != data_dict[group_key]:
                        evaluate = True
                    if group_key in data and not data[group_key]:
                        del data[group_key]
                        evaluate = True
        else:
            value = cache.get(key)
            if not value:
                evaluate = True
            if isinstance(value, dict) and 'is_multigroup' in value:
                evaluate = True

        if evaluate:
            value = func(*args, **kwargs)
            if not group_keys:
                cache.set(key, value)
            else:
                group_dict = {}
                for group_key in group_keys:
                    if group_key not in data:
                        group_dict[group_key] = make_group_value(group_key)
                    else:
                        group_dict[group_key] = data[group_key]
                data_dict = {}
                data_dict['value'] = value
                data_dict['is_multigroup'] = True
                data_dict.update(group_dict)
                group_dict[key] = data_dict
                cache.set_multi(group_dict)
        return value


def cached_factory(client):
    return CacheDecorator(client)

