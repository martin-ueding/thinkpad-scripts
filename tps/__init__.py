# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2014 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Main module for thinkpad-scripts.
'''

__all__ = []

import sys

from tps.i18n import application, install

# setup i18n app wide
install(application)


'''
Asserts that this is running with Python 3
'''
assert sys.version_info >= (3, 0), 'You need Python 3 to run this!'
