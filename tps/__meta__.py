# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>


# nifty necessity
def _get_version_from_changelog():
    import builtins
    import gzip
    import os
    import re
    import sys
    
    filename = '../CHANGELOG.rst'
    if not os.path.isfile(filename):
        filename = os.path.basename(filename)
        if not os.path.isfile(filename):
            filename = os.path.join(sys.prefix, 'share', 'doc', \
                'thinkpad-scripts', filename)
            if not os.path.isfile(filename):
                filename += '.gz'
    
    if os.path.isfile(filename):
        pattern = re.compile(r'^v(\d+(?:\.\d+)+)$')
        open = gzip.open if filename.endswith('.gz') else builtins.open
        with open(filename) as f:
            for line in f:
                if isinstance(line, bytes):
                    line = line.decode()
                m = pattern.match(line)
                if m:
                    return list(map(int, m.group(1).lstrip('v').split('.')))

    raise ValueError('Unable to obtain version from changelog!')

# package info
name                    = "thinkpad-scripts"
package                 = "tps"
software                = "Scripts for ThinkPad®"
component               = "Main"
author                  = "Martin Ueding"
author_email            = "dev@martin-ueding.de"
maintainer              = author
maintainer_email        = author_email
vendor                  = "Martin Ueding"
copyright               = "Copyright (c) 2010-2016 " + vendor
url                     = "https://github.com/martin-ueding/thinkpad-scripts"
license                 = "GNU GPLv2+"
description             = "%s - %s" % (software, component)
text                    = """%s""" % description
keywords                = [
    "thinkpad",
    "lenovo",
    "ibm",
    "scripts",
    "rotate",
    "hdaps",
    "thinkfan",
    "thinklight",
    "tpacpi",
    "thinkpad_acpi",
    "thinkpad_hwmon",
    "tp_smapi",
    "acpi_call"
]
# platform strings: http://docs.python.org/library/sys.html#sys.platform
platforms               = [ "linux2" ]
# Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers             = [ f.strip() for f in """
    Environment :: Console,
    License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
    Programming Language :: Python""".splitlines() if f.strip()
]
download_url            = "http://martin-ueding.de/download/thinkpad-scripts/"
# PEP 314 (metadata_version == '1.1')
requires                = []
provides                = []
obsoletes               = []
# Options specific to distutils/setuptools/distribute commands
namespace_packages      = []
package_dir             = { '' : '.' }
package_data            = {
    'tps' : [
        'default.ini',
        'i18n/*/LC_MESSAGES/*.mo'
    ]
}
include_package_data    = True
exclude_package_data    = None
py_modules              = []
scripts                 = []
zip_safe                = False
test_suite              = "tps.tests"
entry_points            = {
    'console_scripts': [
        'thinkpad = tps.thinkpad:main',
        # legacy EPs - use 'thinkpad' for all purposes
        'thinkpad-config = tps.thinkpad:main_legacy',
        'thinkpad-dock = tps.thinkpad:main_legacy',
        'thinkpad-dock-hook = tps.thinkpad:main_legacy',
        'thinkpad-mutemic = tps.thinkpad:main_legacy',
        'thinkpad-rotate = tps.thinkpad:main_legacy',
        'thinkpad-rotate-hook = tps.thinkpad:main_legacy',
        'thinkpad-scripts-config-migration = tps.thinkpad:main_legacy',
        'thinkpad-touch = tps.thinkpad:main_legacy',
        'thinkpad-touchpad = tps.thinkpad:main_legacy',
        'thinkpad-trackpoint = tps.thinkpad:main_legacy',
    ]
}
setup_requires          = []
install_requires        = []
extras_require          = {}
tests_require           = []
# where to find dependant packages (urls or dirs following file:// syntax)
dependency_links        = []
data_files              = []

# version definition
_version = _get_version_from_changelog()
major                   = _version[0]
minor                   = _version[1]
micro                   = _version[2]
releaselevel            = 0xF
serial                  = 0
date                    = "01-Jan-2016"

# version helpers
version                 = (major, minor)
level                   = "alfa" if releaselevel == 0xA else \
                          "beta" if releaselevel == 0xB else \
                          "candidate" if releaselevel == 0xC else \
                          "final" if releaselevel == 0xF else \
                          "unknown"
version_info            = major, minor, micro, level, serial
hex                     = ((major << 24) | \
                          (minor << 16) | \
                          (micro <<  8) | \
                          (releaselevel <<  4) | \
                          (serial << 0))
short                   = "%d.%d.%d" % (major, minor, micro)
long                    = "%s (%s)" % (short, date)
tex                     = "This is %s, Version %s" % (package, long)
gnu                     = "%s %s" % (package, long)
web                     = "%s/%s" % (package, short)
sccs                    = "@(#)%s %s" % (package, long)
rcs                     = "$Id: %s %s $" % (package, long)
