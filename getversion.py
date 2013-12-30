#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

import argparse
import re

__docformat__ = "restructuredtext en"

def get_version():
    filename = '../CHANGELOG.rst'

    pattern = re.compile(r'^v(\d+(?:\.\d+)+)$')

    with open(filename) as f:
        for line in f:
            m = pattern.match(line)
            if m:
                return(m.group(1))

    return None

def main():
    options = _parse_args()

    print(get_version())

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description="")

    return parser.parse_args()

if __name__ == "__main__":
    main()
