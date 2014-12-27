# Caching
[![Build Status](https://travis-ci.org/mdomans/caching.svg?branch=master)](https://travis-ci.org/mdomans/caching)
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

