#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
import subprocess
import re

__docformat__ = "restructuredtext en"

def main():
    internal = "LVDS1"

    options = _parse_args()

    external, resolution, is_enabled = find_external(internal)

    print external, resolution, is_enabled

    if is_enabled:
        pass

def find_external(internal):
    """
    Finds the port which has the external monitor attached.

    :return: Name of the interface, maximum resolution and whether the screen
        is enabled.
    :rtype: Tuple
    """
    xrandr = subprocess.check_output(["xrandr"]).split("\n")

    regex = re.compile(r"^(\S+) (disconnected|connected).*$")

    word_list = []
    interfaces = []

    for line in xrandr:
        words = line.split()
        word_list.append(words)

    for lineno in range(len(word_list)):
        if len(word_list[lineno]) < 2:
            continue

        if word_list[lineno][1] == 'connected':
            port = word_list[lineno][0]
            if port == internal:
                continue

            resolution = word_list[lineno+1][0]
            selected_frequency = word_list[lineno+1][1]

            is_enabled = "*" in selected_frequency

            return port, resolution, is_enabled

    return None, None

def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(usage="", description="")
    #parser.add_argument("action", metavar="action", type=str, nargs=1, help="on|off")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")

    return parser.parse_args()


if __name__ == "__main__":
    main()
