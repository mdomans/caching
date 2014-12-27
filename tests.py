#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factories import cached_factory

import unittest
# from hash_ring import MemcacheRing
from memcache import Client


class Basic(unittest.TestCase):
    def setUp(self):
        mc = Client(['0.0.0.0:11211'])
        self.cache_decorator = cached_factory(mc)

    def test_simple(self):
        cache = self.cache_decorator
        self.call_count = 0

        @cache("simple")
        def func():
            self.call_count += 1
            return 1

        cache.expire_key("simple")
        self.assertEqual(func(), 1)
        self.assertEqual(func(), 1)
        self.assertEqual(self.call_count, 1)

    def test_params(self):
        cache = self.cache_decorator

        @cache("test_params")
        def func(argument):
            return argument

        self.assertEqual(func(1), 1)
        self.assertEqual(func(2), 2)

        @cache("more_params")
        def func2(argument, *args, **kwargs):
            return argument, args, kwargs

        self.assertEqual(func2(1, 2, test=3), (1, (2,), {"test": 3}))
        self.assertEqual(func2(1, 45), (1, (45,), {}))
        self.assertEqual(func2(1), (1, (), {}))

    def test_groups(self):
        pass




