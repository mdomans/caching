# -*- coding: utf-8 -*-

import datetime
from hashlib import md5                   
from backend import get_cache_backend

cache = get_cache_backend()

def make_key(key, constructor = md5):
    return constructor(str(key)).hexdigest()


def expire_mcached(key):    
    cache.set(make_key(key), None)


def make_group_value(group_key, constructor=md5):
    return constructor(str(datetime.datetime.now()) + group_key).hexdigest()
