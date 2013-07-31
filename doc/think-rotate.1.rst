.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

############
think-rotate
############

*******************************************
ThinkPad X220 Tablet screen rotation script
*******************************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Date: 2012-06-08
:Manual section: 1

SYNOPSIS
========

::

    think-rotate [direction]

DESCRIPTION
===========

If you want to use your X220 Tablet as a tablet, you might want to rotate the
screen. You can use this script for that and it will ensure that the pen and
touch interface know about the rotated screen.

It will also disable the trackpoint (the xinput id is automatically queried) so
that the back of the screen does not move your mouse if there is any force on
the side of the screen.

Finally, it will start the virtual keyboard (``kvkbd`` by default) when the
screen is rotated and kill it when the screen is rotated back to normal.

If the screen is already rotated (say left) and you call ``think-rotate left``,
the screen will be reverted to the normal orientation. That way, you can use
this script as a toggle.

OPTIONS
=======

direction
    The direction can be any of:

    - ccw
    - cw
    - flip
    - half
    - left
    - none
    - normal
    - right

    Since the Wacom tools and ``xrandr`` have different names, this program
    accepts all of them, so that you do not have to learn yet another set of
    directions.

EXIT STATUS
===========

0
    Everything went okay.

2
    User specified a direction that is not known.

ENVIRONMENT
===========

The script relies on ``xrandr`` to get the information, so this has to work.

FILES
=====

Config
------

You can create a config file in ``$HOME/.config/think-rotate/rotate.sh``, which
is a simple Bash script that is going to be sourced from ``think-rotate``.

A sample config would look like this::

    virtual_kbd="cellwriter"

You can set the following option:

``virtual_kbd``
    Command to start the virtual keyboard.

Hooks
-----

You can add scripts to be called before and after with the following files:

- ``~/.config/think-rotate/hooks/prerotate``
- ``~/.config/think-rotate/hooks/postrotate``

EXAMPLE
=======

To rotate the screen to the right (and later back again), use::

    think-rotate

To specify the direction, you can use::

    think-rotate left
    think-rotate right
    think-rotate flip
    think-rotate normal

SEE ALSO
========

- `GitHub Repository`_

.. _`GitHub Repository`: https://github.com/martin-ueding/think-rotate
