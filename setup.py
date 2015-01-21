#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>

import sys

print('This is running on:')
print(sys.version)
print()

from setuptools import setup, find_packages

import getversion

if __name__ == '__main__':
    packages = find_packages()

    setup(
        author="Martin Ueding",
        author_email="dev@martin-ueding.de",
        description="Scripts for ThinkPad®",
        license="GNU GPLv2+",
        classifiers=[
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
            "Programming Language :: Python",

        ],
        name="thinkpad-scripts",
        packages=packages,
        entry_points={
            'console_scripts': [
                'thinkpad-config = tps.config:main',
                'thinkpad-dock = tps.dock:main',
                'thinkpad-dock-hook = tps.hooks:main_dock_hook',
                'thinkpad-mutemic = tps.sound:main_mutemic',
                'thinkpad-rotate = tps.rotate:main',
                'thinkpad-rotate-hook = tps.hooks:main_rotate_hook',
                'thinkpad-scripts-config-migration = tps.config:migrate_shell_config',
                'thinkpad-touch = tps.main_touchscreen:main',
                'thinkpad-touchpad = tps.main_touchpad:main',
                'thinkpad-trackpoint = tps.main_trackpoint:main',
            ],
        },
        test_suite='tps.testsuite',
        install_requires=[
            'termcolor',
        ],
        package_data={
            'tps': ['default.ini'],
        },
        url="https://github.com/martin-ueding/thinkpad-scripts",
        download_url="http://martin-ueding.de/download/thinkpad-scripts/",
        version=getversion.get_version(),
    )
