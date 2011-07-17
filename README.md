Caching
=======

<div style="float: right; padding: 0px 0px 2em 2em"></div>

For news, bugs and documentation visit [home].

  [wsgi]: http://www.wsgi.org/wsgi/
  [home]: http://mdomans.com/
  [py]: http://python.org/

Installation and Dependencies
-----------------------------

You can install caching with `python setup.py install` or `easy_install caching` 

Example
-------

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

Licence (MIT)
-------------

    Copyright (c) 2011, Michal Domanski.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

