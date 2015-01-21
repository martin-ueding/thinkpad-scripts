#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import tps.input

def main():
    '''
    Command line entry point for toggling the touch screen.

    :returns: None
    '''
    tps.input.state_change_ui('touchscreen_device', True)


if __name__ == '__main__':
    main()
