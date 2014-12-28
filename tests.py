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
        # this will pull old value from cache, since we provided key explicitly
        self.assertEqual(func(2), 1)

        cache.expire_key("more_params")

        # but this will work nicely
        @cache()
        def no_explicit_key_func(argument):
            return argument

        self.assertEqual(no_explicit_key_func(1), 1)
        self.assertEqual(no_explicit_key_func(2), 2)

        # with more params
        @cache()
        def func2(argument, *args, **kwargs):
            return argument, args, kwargs

        self.assertEqual(func2(1, 2, test=3), (1, (2,), {"test": 3}))
        self.assertEqual(func2(1, 45), (1, (45,), {}))
        self.assertEqual(func2(1), (1, (), {}))

        # but how do we expire such cache?

        self.call_count = 0

        # better cache, because now you can expire whole group
        @cache(group_keys=["group_key_1"])
        def func2_with_group(argument, *args, **kwargs):
            self.call_count += 1
            return argument, args, kwargs

        self.assertEqual(func2_with_group(1), (1, (), {}))
        self.assertEqual(func2_with_group(1), (1, (), {}))
        self.assertEqual(func2_with_group(1), (1, (), {}))
        self.assertEqual(self.call_count, 1)
        cache.expire_key("group_key_1")
        self.assertEqual(func2_with_group(1), (1, (), {}))
        self.assertEqual(self.call_count, 2)

        # but it still doesn't expire one value well, yes?
        # yes, so...

        cache.expire_key("group_key_1")
        self.call_count = 0

        def func2_with_group_and_master_key(argument, *args, **kwargs):
            @cache("master_key_%s" % argument, group_keys=["group_key_1"])
            def _inner(inner_arg, *inner_args, **inner_kwargs):
                self.call_count += 1
                return inner_arg, inner_args, inner_kwargs
            return _inner(argument, *args, **kwargs)

        self.assertEqual(func2_with_group_and_master_key(1), (1, (), {}))
        self.assertEqual(func2_with_group_and_master_key(1), (1, (), {}))
        self.assertEqual(self.call_count, 1)
        # so now we can expire whole group
        cache.expire_key("group_key_1")
        # but
        func2_with_group_and_master_key(1)
        # we can also expire single key
        cache.expire_key("master_key_%s" % 1)
        func2_with_group_and_master_key(1)
        self.assertEqual(self.call_count, 3)


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

    def test_sample_usage(self):

        cache = self.cache_decorator

        @cache("user_data_main_key", group_keys=['user_data_1', 'users_under_test'])
        def func_under_test(arg):
            return arg

        self.assertEqual(func_under_test(1), 1)
