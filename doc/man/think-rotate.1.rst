..  Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

############
thinkpad-rotate
############

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

You can create a config file in ``$HOME/.config/thinkpad-scripts/rotate.sh``,
which is a simple Bash script that is going to be sourced from
``thinkpad-rotate``.

A sample config would look like this::

    virtual_kbd="cellwriter"

You can set the following option:

``kdialog``
    If this is set to ``true``, a GUI progress bar will be shown. This needs
    ``kdialog`` installed. When this script is called from
    ``thinkpad-rotate-hook``, ``kdialog`` has some problem. Therefore,
    ``thinkpad-rotate-hook`` disables kdialog by settings ``kdialog=false``
    when calling the script. If you define it in you configuration file, make
    sure not to overwrite an already set value. You can do this with the
    following line::

        kdialog="${kdialog:-true}"

    *Default:*.

``virtual_kbd``
    Command to start the virtual keyboard. Choices are (among others) ``kvkbd``
    for KDE, ``cellwriter``, ``onboard``. *Default: kvkbd*.

``internal``
    The ``xrandr`` name for the internal monitor. *Default: LVDS1*.

``default_rotation``
    Default rotation if device is in normal rotation and no arguments are
    given. *Default: right*.

Hooks
-----

You can add scripts to be called before and/or after rotation by placing them
at the following paths. The ``postrotate`` hook gets the new rotation
(``left``, ``right``, ``inverted``, or ``normal``) as a command line argument.

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
