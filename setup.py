#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

if __name__ == '__main__':
    packages = find_packages()

    setup(
        author="Martin Ueding",
        author_email="dev@martin-ueding.de",
        description="Scripts for ThinkPad®",
        license="GPL2",
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
                'thinkpad-rotate = tps.rotate:main',
                'thinkpad-touch = tps.input:main_touchscreen',
                'thinkpad-touchpad = tps.input:main_touchpad',
                'thinkpad-trackpoint = tps.input:main_trackpoint',
                'thinkpad-scripts-config-migration = tps.config:migrate_shell_config',
            ],
        },
        install_requires=[
            'termcolor',
        ],
        url="https://github.com/martin-ueding/thinkpad-scripts",
        download_url="http://martin-ueding.de/download/thinkpad-scripts/",
        version="4.0",
    )
