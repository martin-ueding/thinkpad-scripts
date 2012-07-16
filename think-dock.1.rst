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

EXIT STATUS
===========

0
    Everything okay.
1
    Some error, probably because there was no external monitor connected.
2
    User did not specify ``on`` or ``off``.

FILES
=====

You can create a config file in ``$HOME/.config/think-rotate/dock.sh``, which
is a simple Bash script that is going to be sourced from ``think-dock``. You
can set the following options:

``disable_wifi``
    Whether to set the wifi. Set it to ``true`` or something else.

``internal``
    The ``xrandr`` name for the internal monitor.

``unmute``
    Whether to change the volume. Set it to ``true`` or something else.

``dock_loudness``
    Volume to set to when docking. Set it to a percentage like ``100%``.

``undock_loundess``
    Volume to set to when undocking. Set it to a percentage like ``50%``.

``set_brightness``
    Whether to change the brightness. Set it to ``true`` or something else.

``brightness``
    Brightness to set to when docking. Set it to a percentage like ``60%``.

``relative_positon``
    Where to set the external monitor. Set it to ``right`` or ``left`` or
    anything else that ``xrandr`` supports with a ``--*-of`` argument.

EXAMPLE
=======

When you have it sitting on the docking station, call ``think-dock on`` to get
the external screen going.

When you are done, call ``think-dock off`` before you disconnect to get the
internal screen back again.
