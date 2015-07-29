#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import tps.input


def main():
    '''
    Command line entry point for toggling the touchpad.

    :returns: None
    '''
    tps.input.state_change_ui('touchpad_device')


if __name__ == '__main__':
    main()
