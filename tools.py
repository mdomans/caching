# -*- coding: utf-8 -*-

import datetime
from hashlib import md5


def make_key(key, *args, **kwargs):
    constructor = kwargs.pop('constructor', md5)
    for elem in args:
        key += str(elem)
    return constructor(str(key)).hexdigest()

def make_group_value(group_key, constructor=md5):
    return constructor(str(datetime.datetime.now()) + group_key).hexdigest()
