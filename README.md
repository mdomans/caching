# Caching
[![Build Status](https://travis-ci.org/mdomans/caching.svg?branch=master)](https://travis-ci.org/mdomans/caching)

## Purpose and logic for this code

Most common problem with any cache is proper invalidation.

This package approaches this problem by enabling the programmer to manage cache keys as logical groups.

For example, in a Django app I often have data for user cache under key "user_1", but I also cache, for granularity purposes, user profile data under "user_profile_1". From experience, I can say this is often done by others as well. Normally, invalidating both those keys requires us to invalidate each explicitly.

With this package, one can group **"user_1"** and **"user_profile_1"** into cache groups, e.g. 
**"user_group_1"** and **"users"**. Therefore, when I'd like to expire all data I've bound to that user, I can expire key **"user_group_1"** and all the key in this group will become invalid. Similarly, if I expire group **"users"** I only invalidated keys in that group.

Example of usage:

```
@cache("user_data_main_key", group_keys=['user_data_1', 'users_under_test'])
def func_under_test(arg):
    return arg
```
And a real world usage example, where we actually build keys based on model data:

```
def func_with_group_and_master_key(argument, *args, **kwargs):
    # here we explicitly build the key for direct invalidation and we pass a group key
    @cache("master_key_%s" % argument, group_keys=["group_key_1"])
    def _inner(inner_arg, *inner_args, **inner_kwargs):
        return inner_arg, inner_args, inner_kwargs
    return _inner(argument, *args, **kwargs)
```

Data in cache can become stale for a number of reasons, but to this day, we use either key by key invalidation (**direct**) or time based invalidation(**expiration**).

Direct invalidation means that at each step the developer is responsible for managing cache keys, which in companies employing more that one person is increasingly difficult. 

On the other hand expiration based on time requires programmer to forecast how long data is valid. In most cases that is impossible and programmers choose low, safe number. Real life proves that it is neither safe, as data may become invalid much faster, nor efficient, as certain blocks of data are valid much longer (orders of mangnitude) than the programmer was originally able to predict.



## Installation and Dependencies

You can install caching with `python setup.py install` or `easy_install caching` 

## Example

    mcached

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

