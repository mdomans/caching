#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factories import cached_factory

import unittest
from memcache import Client
from ultramemcache import Client as UClient


class TestMemcacheClient(unittest.TestCase):
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

        cache.expire_key("simple")

    def test_params(self):
        cache = self.cache_decorator

        cache.expire_key("test_params")

        @cache("test_params")
        def func(argument):
            return argument

        self.assertEqual(func(1), 1)
        self.assertEqual(func(2), 2)

        cache.expire_key("more_params")

        @cache("more_params")
        def func2(argument, *args, **kwargs):
            return argument, args, kwargs

        self.assertEqual(func2(1, 2, test=3), (1, (2,), {"test": 3}))
        self.assertEqual(func2(1, 45), (1, (45,), {}))
        self.assertEqual(func2(1), (1, (), {}))

        cache.expire_key("test_params")
        cache.expire_key("more_params")

    def test_groups(self):
        cache = self.cache_decorator

        cache.expire_key("test_params")
        cache.expire_key("a")
        cache.expire_key("b")
        self.call_count = 0

        @cache("test_params", group_keys=["a", "b"])
        def func(argument):
            self.call_count += 1
            return argument

        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 1)

        cache.expire_key("a")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 2)
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 2)

        cache.expire_key("a")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 3)

        cache.expire_key("b")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 4)

        cache.expire_key("test_params")


class TestUMemcacheClient(unittest.TestCase):

    def setUp(self):
        mc = UClient(['0.0.0.0:11211'])
        self.cache_decorator = cached_factory(mc)

    def test_groups(self):
        cache = self.cache_decorator

        cache.expire_key("test_params")
        cache.expire_key("a")
        cache.expire_key("b")
        self.call_count = 0

        @cache("test_params", group_keys=["a", "b"])
        def func(argument):
            self.call_count += 1
            return argument

        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 1)

        cache.expire_key("a")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 2)
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 2)

        cache.expire_key("a")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 3)

        cache.expire_key("b")
        self.assertEqual(func(1), 1)
        self.assertEqual(self.call_count, 4)

        cache.expire_key("test_params")
        cache.expire_key("a")
        cache.expire_key("b")