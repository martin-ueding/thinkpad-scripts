# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#
# Initial implementation comes from:
#     LaptopControlPanel - A Laptop Control Panel 
#     Copyright (C) 2014 Fabrice Salvaire
# The original author has given conscent to use this code within this project.
#

import os

from tps.utils import fileExists, fileRead, fileWrite

class SysDevice(object):

    def __init__(self, path):
        self._path = path
        self._name = os.path.basename(path)

    @property
    def name(self):
        return self._name
        
    def exists(self, fileName):
        return fileExists(self._join(fileName))

    def read(self, fileName):
        try:
            return fileRead(self._join(fileName), \
                'Unable to read %s property: %s' \
                % (self._path, fileName))
        except (IOError, OSError) as e:
            raise AttributeError(e)
    
    def write(self, fileName, value):
        try:
            return fileWrite(self._join(fileName), \
                'Unable to write %s property: %s' % \
                (self._path, fileName), value)
        except (IOError, OSError) as e:
            raise AttributeError(e)

    def readInt(self, fileName):
        value = self.read(fileName)
        return int(value) if value != None else value
        
    def readFloat(self, fileName, div=0, rounding=3):
        return self.roundFloat(self.read(fileName), div, rounding)
        
    def roundFloat(self, value, div=0, rounding=3):
        if value is not None:
            if div > 0:
                return round(int(value) / (10**div), rounding)
            return float(value)
        return value

    def readBool(self, fileName):
        return bool(self.readInt(fileName))
        
    def list(self):
        return os.listdir(self._path)

    def _join(self, fileName):
        return os.path.join(self._path, fileName)
        
    def __str__(self):
        sb = [self.name]
        properties = [ p for p in dir(self.__class__) \
            if isinstance(getattr(self.__class__,p), property) ]
        for name in sorted(properties):
            if not name.startswith('_'):
                sb.append("\t{name}='{value}'".format(name=name, value=getattr(self, name)))
        return '\n'.join(sb)
