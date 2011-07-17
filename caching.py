# -*- coding: utf-8 -*-

"""

.. module:: decorators
   :platform: Unix, Windows, Linux
   :synopsis: Decorators for simpler work with cache
.. :moduleauthor: Michal Domanski <mdomans@gmail.com>

"""

from __future__ import absolute_import

from .backend import get_cache_backend
from .tools import make_key, make_group_value 

cache = get_cache_backend()

def cached(key, group_key='', exp_time=0):
    """

    Decorator for work with multiple groups for each key

    gives you the actual ability to make dependancies from group and key 
    to single value or set exp_time and still have expiration by key
        
    .. rubric:: Usage:
    
    You store in cache UserProfile instance. Since you want to expire it
    when user changes UserProfile models, you do::
                                           
    def get_userprofile(id=id):                  
        @cached('a', group_keys='b'):
        def _get_userprofile(id=id)
            return UserProfile.objects.get(id=id)
        return _get_userprofile(id=id)
    
    so::
    
    expire_mcached('a')
    expire_mcached('b')
    
    work, and while first one is very precise, second one will expire 
    everything with group key set to 'b'
    
    or::
    
    def get_userprofile(id=id):                  
        userprofile_key = 'userprofile_%s' % id
        @cached(userprofile_key, exp_time=60): # expires after 60 seconds
        def _get_userprofile(id=id)
            return UserProfile.objects.get(id=id)
        return _get_userprofile(id=id)
    
    
    
    
    """
    # we don't want to mix time based and event based expiration models
    if group_key: 
        assert exp_time == 0, "can't set expiration time for grouped keys"
        
    def f_wrapper(func):
        
        def arg_wrapper(*args, **kwargs):
            value = None  
            if group_key:
                data = cache.get_many([make_key(group_key)] + [make_key(key)]) 
                data_dict = data.get(make_key(key))  
                if data_dict:
                    value = data_dict['value']
                    group_value = data_dict['group_value']
                    if group_value != data[make_key(group_key)]:
                        value = None
            else:
                value = cache.get(key)
            if not value: 
                value = func(*args, **kwargs)
                if exp_time:
                    cache.set(make_key(key), value, exp_time)
                elif not group_key:
                    cache.set(make_key(key), value)
                else:  # exp_time not set and we have group_keys            
                    group_value = make_group_value(group_key)
                    data_dict = {'value': value, 'group_value': group_value}
                    cache.set_many({make_key(key): data_dict, make_key(group_key): group_value})
            return value
        arg_wrapper.__name__ = func.__name__
        return arg_wrapper 
    return f_wrapper

    
class mcached(object): 
    """

    Decorator for work with multiple groups for each key
     
    gives you the actual ability to make dependancies from multiple points to single value
        
    .. rubric:: Usage:
    
    You store in cache UserProfile instance. Since you want to expire it when user changes either User or UserProfile models, you do::
                                           
    def get_userprofile(id=id):                  
        userprofile_key = 'userprofile_%s' % id
        user_key = 'user_%s' % id
        @mcached(user_key, group_keys=[user_key,userprofile_key]):
        def _get_userprofile(id=id)
            return UserProfile.objects.get(id=id)
        return _get_userprofile(id=id)
    
    so now you can expire this function using key, or one of the group keys :)
    
    """
    group_keys = []  
    
    def __new__(typ, *attr_args, **attr_kwargs):
        
        def decorator(orig_func):
            self = object.__new__(typ)
            self.__init__(orig_func, *attr_args, **attr_kwargs)
            return self
        return decorator
                        
    def __init__(self, func, key, group_keys=[], group_key=None):
        self.func = func
        self.key = key
        self.group_keys = group_keys  
        self.__name__ = func.__name__
        if group_key:
            self.group_keys.append(group_key)
        
    def __call__(self, *args, **kwargs):   
        key = make_key(self.key)    
        group_keys = map(make_key, self.group_keys)
        value = None  
        evaluate = False
        if group_keys:  
            data = cache.get_many(group_keys + [key])
            data_dict = data.get(key)    
            if (not data) or (not data_dict):
                evaluate = True
            if data_dict:
                value = data_dict['value']
                for group_key in group_keys:
                    if not group_key in data or not group_key in data_dict or data[group_key] != data_dict[group_key]: 
                        evaluate = True
                    if group_key in data and not data[group_key]:
                        del data[group_key]
                        evaluate = True
        else:
            value = cache.get(key)
            if not value: 
                evaluate = True

        if evaluate:                  
#            print 'cache miss %s' % self.func,args, kwargs
            
            value = self.func(*args, **kwargs)
            if not group_keys:
                cache.set(key, value)
            else:   
                group_dict = {}
                for group_key in group_keys:
                    if group_key not in data:
                        group_dict[group_key] = make_group_value(group_key)
                    else:
                        group_dict[group_key] = data[group_key]
                data_dict = {}
                data_dict['value'] = value
                data_dict.update(group_dict)
                group_dict[key] = data_dict
                cache.set_many(group_dict)
        return value
