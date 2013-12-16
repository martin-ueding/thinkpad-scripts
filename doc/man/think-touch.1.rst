..  Copyright © 2012 Jim Turner <jturner314@gmail.com>
    Licensed under The GNU Public License Version 2 (or later)

###########
think-touch
###########

*******************************
enable/disable the touch screen
*******************************

:Author: Jim Turner <jturner314@gmail.com>
:Manual section: 1

Synopsis
========

::

    think-touch [on|off]

Description
===========

This program enables/disables the touch screen of the ThinkPad tablet. If no
option is given, it toggles the touch screen on/off.

Options
=======

on|off
    If you want to enable the touch screen, use ``on``. Otherwise use ``off``.

    If you omit this option, the script will toggle the touch screen on/off.

Exit Status
===========

0
    Everything okay.
1
    Some error.

Files
=====

You can create a config file in ``$HOME/.config/think-rotate/touch.sh``, which
is a simple Bash script that is going to be sourced from ``think-touch``.

A sample config would look like this::

    id="Wacom ISDv4 E6 Finger touch"

You can set the following options:

``id``
    The ``xinput`` id of the touch screen device. The default is
    ``Wacom ISDv4 E6 Finger touch``

Examples
========

You can just call ``think-touch`` to toggle the touch screen; otherwise
state on/off explicitly with ``think-touch on`` or ``think-touch off``.

If you want to disable touch automatically on startup and resume of your system,
see the man page for ``think-resume``.
