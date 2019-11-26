# -*- coding: utf-8 -*-
"""
Module et_micc.static_vars
==========================
A decorator for adding static variables to a function.
see https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
"""

def static_vars(**kwargs):
    """Add static variables to a method.
    
    To add the variable :py:obj:`counter` to :py:meth:`foo` :
    
    .. code-block:: python
    
       @static_vars(counter=0)
       def foo():
           foo.counter += 1 # foo.counter is incremented on every call to foo
    
    """
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

#eof