#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import cached_factory

from hash_ring import MemcacheRing
mc = MemcacheRing(['127.0.0.1:11212'])

cached = cached_factory(mc)
