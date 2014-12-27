# -*- coding: utf-8 -*-

import datetime
from hashlib import md5


def make_key(key, *args, **kwargs):
    """

    :param key: basic key to transform into cache key
    :param args: positional arguments to add to key
    :param kwargs: keyword arguments to add to key
    :return: key
    :rtype str:

    """
    constructor = kwargs.pop('constructor', md5)
    for elem in args:
        key += str(elem)
    return constructor(str(key)).hexdigest()


def make_group_value(group_key, constructor=md5):
    return constructor(str(datetime.datetime.now()) + group_key).hexdigest()
