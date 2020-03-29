.. Copyright © 2015 Martin Ueding <mu@martin-ueding.de>
   Licensed under The GNU Public License Version 2 (or later)

###############
thinkpad-config
###############

.. only:: html

    Show the |project| configuration

    :Author: Martin Ueding <mu@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-config

Description
===========

The user configuration for |project| is stored in
``~/.config/thinkpad-scripts/config.ini`` in the INI format. There is a global
configuration that |project| will use as a basis and apply your configuration
over that, overriding default values. This program will show the config that
will be used in the program.

Options
=======

This program does not interpret any command line options.

Exit Status
===========

0
    Everything okay.

.. include:: ../man-epilogue.rst
