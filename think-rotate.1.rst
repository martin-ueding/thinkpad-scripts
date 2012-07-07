.. Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

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

If the screen is already rotated (say left) and you call ``think-rotate left``,
the screen will be reverted to the normal orientation. That way, you can use
this script as a toggle.

OPTIONS
=======

direction
    The direction can be any of:

    - flip
    - left
    - none
    - right

EXIT STATUS
===========

0
    Everything went okay.

2
    User specified a direction that is not known.

ENVIRONMENT
===========

The script relies on ``xrandr`` to get the information, so this has to work.

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
