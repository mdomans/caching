#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import cached_factory

from hash_ring import MemcacheRing
mc = MemcacheRing(['127.0.0.1:11212'])

cached = cached_factory(mc)


def test_simple():
    def test(a, b):
        @cached('test_key_%s_%s' % (a, b), group_key='test')
        def _test(a, b):
            print 'function'
            return a + b

        print dir(_test)
        return _test(a, b)

    # check if function behaves properly
    4 == test(3, 1)
    4 == test(3, 1)
    3 == test(1, 2)
    5 == test(2, 3)
    4 == test(3, 1)
    expire_group('test')
    expire_key('test_key_3_1')
    expire_key('test_key_1_2')
    5 == test(2, 3)


def test_arg_cache():
    @arg_cached(group_keys=['test1', 'test2'])
    def test(a, b):
        print 'function'
        return a + b

    3 == test(1, 2)
    4 == test(2, 2)
    4 == test(2, 2)
    4 == test(2, 2)


def test_group_semantics():
    def func1(a, b):
        @cached('func1_key_%s_%s' % (a, b), group_key='test1')
        def _test(a, b):
            print 'function'
            return a + b

        return _test(a, b)

    def func2(a, b):
        @cached('func2_key_%s_%s' % (a, b), group_key='test2')
        def _test(a, b):
            print 'function'
            return a - b

        return _test(a, b)


    def func3(a, b):
        cg = CacheGroup(group_key='test_all', functions=[func1, func2])

        def _test(a, b):
            x = func1(a, b)
            y = func2(a, b)
            return x, y

        cg.expire()
        cg.in_cache()
        return _test(a, b)

    func3(4, 4)

