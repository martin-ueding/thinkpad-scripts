#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

import argparse
import re
import sys

__docformat__ = "restructuredtext en"

def main():
    options = _parse_args()

    filename = 'CHANGELOG.rst'

    pattern = re.compile(r'^v(\d+(?:\.\d+)+)$')

    with open(filename) as f:
        for line in f:
            m = pattern.match(line)
            if m:
                print(m.group(1))
                sys.exit(0)

    sys.exit(1)


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
