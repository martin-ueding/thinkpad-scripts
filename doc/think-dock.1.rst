..  Copyright © 2013 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

##########
think-dock
##########

**********************************************************
set the screens when going to and from the docking station
**********************************************************

:Author: Martin Ueding <dev@martin-ueding.de>
:Manual section: 1

SYNOPSIS
========

::

    think-dock [on|off]

DESCRIPTION
===========

This program sets the screen resolution correctly when putting the ThinkPad
onto the docking station. It also sets the Wacom input devices to act on the
internal screen only.

It deduces what to do automatically, if no option is given. If it is docked, it
will perform the docking action. When you pressed the eject button on the
docking station, it will un-dock.

There will be an udev rule installed that will automatically dock it when set
onto the station and un-dock when you press the eject button.

what it does
------------

When docking, the following things are done:

- Activating the external monitor.
- Setting the external monitor as primary monitor.
- Deactivate the wireless connection.
- Set the Wacom devices to the internal screen only.
- Set the brightness to a fixed value, currently 60%.
- Unmute the speakers and set the volume to 100%.

When undocking, the following things are done:

- Deactivating external monitor.
- Setting the internal monitor as primary monitor.
- Activating the wireless connection.
- Set the speakers to some medium volume, currently 50%.

OPTIONS
=======

on|off
    If you have it sitting on the docking station and want it to dock, use
    ``on``. Otherwise use ``off`` before you take the ThinkPad off the docking
    station.

    You can omit this option and the script will guess what to do.

EXIT STATUS
===========

0
    Everything okay.
1
    Some error.

FILES
=====

Config
------

You can create a config file in ``$HOME/.config/think-rotate/dock.sh``, which
is a simple Bash script that is going to be sourced from ``think-dock``.

A sample config would look like this::

    dock_loudness="50%"
    disable_wifi=false
    relative_position=left

You can set the following options:

``disable_wifi``
    Whether to set the wifi. Set it to ``true`` or something else.

``internal``
    The ``xrandr`` name for the internal monitor.

``unmute``
    Whether to change the volume. Set it to ``true`` or something else.

``dock_loudness``
    Volume to set to when docking. Set it to a percentage like ``100%``.

``undock_loudness``
    Volume to set to when undocking. Set it to a percentage like ``50%``.

``set_brightness``
    Whether to change the brightness. Set it to ``true`` or something else.

``brightness``
    Brightness to set to when docking. Set it to a percentage like ``60%``.

``relative_position``
    Where to set the external monitor. Set it to ``right`` or ``left`` or
    anything else that ``xrandr`` supports with a ``--*-of`` argument.

Hooks
-----

There are hooks, called before and after the main script. It gets a single command line argument, ``on`` or ``off``.

- ``~/.config/think-rotate/hooks/predock``
- ``~/.config/think-rotate/hooks/postdock``

EXAMPLE
=======

You can just call ``think-dock`` and it will do the right think probably.

If you want, you can tell the script what to do: When you have it sitting on
the docking station, call ``think-dock on`` to get the external screen going.
When you are done, call ``think-dock off`` before you disconnect to get the
internal screen back again.
