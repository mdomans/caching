#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factories import cached_factory

import unittest
from hash_ring import MemcacheRing

class Basic(unittest.TestCase):

    def setUp(self):
        mc = MemcacheRing(['127.0.0.1:11212'])
        self.cache_decorator = cached_factory(mc)

    def test_decoration(self):

        cached = self.cache_decorator

        @cached
        def func():
            return 1

