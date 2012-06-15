##########
think-dock
##########

**********************************************************
set the screens when going to and from the docking station
**********************************************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Date: 2012-02-27
:Manual section: 1

SYNOPSIS
========

::

    think-dock on|off

DESCRIPTION
===========

This program sets the screen resolution correctly when putting the ThinkPad
onto the docking station. It also sets the Wacom input devices to act on the
internal screen only.

OPTIONS
=======



EXIT STATUS
===========

0
    Everything okay.
2
    User did not specify ``on`` or ``off``.

EXAMPLE
=======

When you have it sitting on the docking station, call ``think-dock on`` to get
the external screen going.

When you are done, call ``think-dock off`` before you disconnect to get
internal screen back again.
