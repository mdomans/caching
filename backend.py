#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GenericCacheBackend(object):

    def get(self, *args, **kwargs):
        pass

    def set(self, *args, **kwargs):
        pass

    def get_many(self, *args, **kwargs):
        pass

    def set_many(self, *args, **kwargs):
        pass


class MemcachedBackend(GenericCacheBackend):
    pass

class DjangoBackend(GenericCacheBackend):
    pass

