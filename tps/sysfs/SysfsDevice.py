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


class SysDevice(object):

    def __init__(self, path):
        self._path = path
        self._name = os.path.basename(path)

    @property
    def name(self):
        return self._name

    def _join(self, file_name):
        return os.path.join(self._path, file_name)

    def read(self, file_name):
        with open(self._join(file_name), 'r') as f:
            return f.read().strip()

    def read_int(self, file_name):
        return int(self.read(file_name))

    def read_bool(self, file_name):
        return bool(self.read_int(file_name))
