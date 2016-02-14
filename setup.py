#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>

import imp
import os
import sys

print('This is running on:')
print(sys.version)
print()

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from setuptools import find_packages

meta_pathname = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "tps", "__meta__.py"
)
__meta__ = imp.load_source("tps.__meta__", meta_pathname)


setup(
    # distutils.dist.DistributionMetaData options
    name                = __meta__.name,
    version             = __meta__.short,
    author              = __meta__.author,
    author_email        = __meta__.author_email,
    maintainer          = __meta__.maintainer,
    maintainer_email    = __meta__.maintainer_email,
    url                 = __meta__.url,
    license             = __meta__.license,
    description         = __meta__.description,
    long_description    = __meta__.text,
    keywords            = __meta__.keywords,
    platforms           = __meta__.platforms,
    classifiers         = __meta__.classifiers,
    download_url        = __meta__.download_url,
    # PEP 314 (metadata_version == '1.1')
    #requires            = __meta__.requires,
    #provides            = __meta__.provides,
    #obsoletes           = __meta__.obsoletes,
    # Options specific to distutils/setuptools/distribute commands
    packages            = find_packages(exclude = [ 'ez_setup' , 'distribute_setup', 'examples', 'tests' ]),
    namespace_packages  = __meta__.namespace_packages,
    package_dir         = __meta__.package_dir,
    package_data        = __meta__.package_data,
    include_package_data= __meta__.include_package_data,
    exclude_package_data= __meta__.exclude_package_data,
    py_modules          = __meta__.py_modules,
    scripts             = __meta__.scripts,
    zip_safe            = __meta__.zip_safe,
    test_suite          = __meta__.test_suite,
    entry_points        = __meta__.entry_points,
    setup_requires      = __meta__.setup_requires,
    install_requires    = __meta__.install_requires,
    extras_require      = __meta__.extras_require,
    tests_require       = __meta__.tests_require,
    dependency_links    = __meta__.dependency_links,
    data_files          = __meta__.data_files
)
