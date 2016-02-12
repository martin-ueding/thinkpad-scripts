# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import time

class cached_property(property):
    "Emulate PyProperty_Type() in Objects/descrobject.c with added cache"
    
    CACHE_TTL = 300

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, ttl=CACHE_TTL):
        super().__init__(fget, fset, fdel, doc)
        self.ttl = ttl
        
    def __call__(self, fget, doc=None, ttl=CACHE_TTL):
        self.__init__(fget, self.fset, self.fdel, doc, ttl)
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        now = time.time()
        try:
            value, last_update = obj._cache[self.fget.__name__]
            if self.ttl > 0 and now - last_update > self.ttl:
                raise AttributeError
        except (KeyError, AttributeError):
            value = super().__get__(obj, objtype)
            try:
                cache = obj._cache
            except AttributeError:
                cache = obj._cache = {}
            cache[self.fget.__name__] = (value, now)
        return value
        
    def __set__(self, obj, value):
        self._remove_cache(obj)
        super().__set__(obj, value)

    def __delete__(self, obj):
        self._remove_cache(obj)
        super().__delete__(obj, value)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__, self.ttl)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__, self.ttl)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__, self.ttl)
        
    def _remove_cache(self, obj):
        if self.fget is not None:
            try:
                del obj._cache[self.fget.__name__]
            except KeyError:
                pass
