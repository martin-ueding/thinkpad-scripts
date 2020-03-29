..  Copyright © 2015 Martin Ueding <mu@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

###################
thinkpad-trackpoint
###################

.. only:: html

    enable/disable the TrackPoint

    :Author: Martin Ueding <mu@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-trackpoint [on|off]

Description
===========

This program enables/disables the TrackPoint of the ThinkPad. If no option is
given, it toggles the TrackPoint on/off.

Options
=======

on|off
    If you want to enable the touch screen, use ``on``. Otherwise use ``off``.

    If you omit this option, the script will toggle the TrackPoint on/off.

Exit Status
===========

0
    Everything okay.
1
    Some error.

Config
======

In the configuration file, you can set the ``xinput`` name of the TrackPoint.
The ThinkPad X220 Tablet has ``TPPS/2 IBM TrackPoint`` for instance. The
default configuration option is just ``TrackPoint`` to be rather general. This
is how you change it in the configuration:

.. code-block:: ini

    [input]
    trackpoint_device = TrackPoint

.. include:: ../man-epilogue.rst
