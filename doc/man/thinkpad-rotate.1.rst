..  Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

###############
thinkpad-rotate
###############

.. only:: html

    ThinkPad X220 Tablet screen rotation script

    :Author: Martin Ueding <dev@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-rotate [direction]

Description
===========

If you want to use your X220 Tablet as a tablet, you might want to rotate the
screen. You can use this script for that and it will ensure that the pen and
touch interface know about the rotated screen.

It will also disable the trackpoint (the xinput id is automatically queried) so
that the back of the screen does not move your mouse if there is any force on
the side of the screen.

Finally, it will start the virtual keyboard (``kvkbd`` by default) when the
screen is rotated and kill it when the screen is rotated back to normal.

If the screen is already rotated (say left) and you call ``thinkpad-rotate
left``, the screen will be reverted to the normal orientation. That way, you
can use this script as a toggle.

A udev hook is installed as well that picks up the ACPI event when rotating the
screen.

Options
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

Exit Status
===========

0
    Everything went okay.

2
    User specified a direction that is not known.

Environment
===========

The script relies on ``xrandr`` to get the information, so this has to work.

Files
=====

Config
------

You can create a config file in ``$HOME/.config/thinkpad-scripts/config.ini``,
which is a simple INI configuration file. The old config can be converted using
the ``thinkpad-scripts-config-migrate`` script that was introduced in version
4.0. A sample config would look like this:

.. code-block:: ini

    [rotate]
    default_rotation = flip

    [sound]
    undock_loudness = 0%

    [screen]
    relative_position = left-of

You can set the following option:

``rotate.default_rotation``
    Default rotation if device is in normal rotation and no arguments are
    given. *Default: right*

``rotate.subpixels``
    Rotate subpixel orientation when rotating the screen. *Default: true*

``rotate.subpixels_with_external``
    Rotate the subpixel orientation if a second screen is attached. *Default:
    false*.

``screen.internal``
    The ``xrandr`` name for the internal monitor. *Default: LVDS1*

``touch.regex``
    Regular expression to match Wacom devices against. If your devices do not
    start with ``Wacom ISD``, change this appropriately. *Default:* ``Wacom
    ISD.*id: (\d+).*``

``unity.toggle_launcher``
    The Unity Launcher on the left side is only shown if you excert pressure
    with the mouse. That means that you do not only have to put the mouse to
    the left edge of the screen, but push it beyond that edge. This is not
    possible to do with touchscreen or the pen, so you need to show the
    launcher by default.

    With this option set to *true*, the hide mode will be toggled. That way,
    you have a hidden launcher on normal rotation, and a always-shown launcher
    with any rotation. *Default: false*

``vkeyboard.program``
    Command to start the virtual keyboard. Choices are (among others) ``kvkbd``
    for KDE, ``cellwriter``, ``onboard``. *Default: kvkbd*

Hooks
-----

You can add scripts to be called before and/or after rotation by placing them
at the following paths. The ``postrotate`` hook gets the new rotation
(``left``, ``right``, ``inverted``, or ``normal``) as a command line argument.

The default paths are:

- ``~/.config/thinkpad-scripts/hooks/prerotate``
- ``~/.config/thinkpad-scripts/hooks/postrotate``

Example
=======

To rotate the screen to the right (and later back again), use::

    thinkpad-rotate

To specify the direction, you can use::

    thinkpad-rotate left
    thinkpad-rotate right
    thinkpad-rotate inverted
    thinkpad-rotate normal

See Also
========

- `GitHub Repository <http://github.com/martin-ueding/thinkpad-scripts>`_
