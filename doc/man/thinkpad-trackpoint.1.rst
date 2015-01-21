..  Copyright © 2015 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

###################
thinkpad-trackpoint
###################

.. only:: html

    enable/disable the TrackPoint

    :Author: Martin Ueding <dev@martin-ueding.de>
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

.. include:: ../man-epilogue.rst
