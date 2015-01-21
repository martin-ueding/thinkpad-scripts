..  Copyright © 2012-2015 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

#################
thinkpad-touchpad
#################

.. only:: html

    ThinkPad TouchPad toggle script

    :Author: Martin Ueding <dev@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-touchpad

Description
===========

This scripts toggles the TrackPad. It is designed to work on ThinkPads, but it
will probably work on almost all laptops.

Options
=======

on|off
    If you want to enable the touchpad, use ``on``. Otherwise use ``off``.

    If you omit this option, the script will toggle the touchpad on/off.

Config
======

In the configuration file, you can set the ``xinput`` name of the touchpad. The
ThinkPad X220 Tablet has ``SynPS/2 Synaptics TouchPad`` for instance. The
default configuration option is just ``TouchPad`` to be rather general. This is
how you change it in the configuration:

.. code-block:: ini

    [input]
    touchpad_device = TouchPad

.. include:: ../man-epilogue.rst
