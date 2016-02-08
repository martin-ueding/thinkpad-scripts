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

from tps.utils import fileRead

class SysDevice(object):

    def __init__(self, path):
        self._path = path
        self._name = os.path.basename(path)

    @property
    def name(self):
        return self._name

    def read(self, file_name):
        try:
            return fileRead(self._join(file_name), \
                'Unable to read PS property: %s' % file_name)
        except (IOError, OSError) as e:
            raise AttributeError(e)

    def read_int(self, file_name):
        return int(self.read(file_name))

    def read_bool(self, file_name):
        return bool(self.read_int(file_name))

    def _join(self, file_name):
        return os.path.join(self._path, file_name)
        
    def __str__(self):
        sb = [self.name]
        properties = [ p for p in dir(self.__class__) \
            if isinstance(getattr(self.__class__,p), property) ]
        for prop in properties:
            sb.append("\t{prop}='{value}'".format(prop=prop, value=getattr(self, prop)))
        return '\n'.join(sb)
