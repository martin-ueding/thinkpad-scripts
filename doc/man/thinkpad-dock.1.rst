..  Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

#############
thinkpad-dock
#############

.. only:: html

    set the screens when going to and from the docking station

    :Author: Martin Ueding <dev@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-dock [on|off]

Description
===========

This program sets the screen resolution correctly when putting the ThinkPad
onto the docking station. It also sets the Wacom input devices to act on the
internal screen only.

It deduces what to do automatically, if no option is given. If it is docked, it
will perform the docking action. When you pressed the eject button on the
docking station, it will un-dock.

There will be an udev rule installed that will automatically dock it when set
onto the station and un-dock when you press the eject button. Technically, this
rule calls the ``thinkpad-dock-hook``.

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

Options
=======

on|off
    If you have it sitting on the docking station and want it to dock, use
    ``on``. Otherwise use ``off`` before you take the ThinkPad off the docking
    station.

    You can omit this option and the script will guess what to do.

Exit Status
===========

0
    Everything okay.
1
    Some error.

Files
=====

Config
------

You can create a config file in ``$HOME/.config/thinkpad-scripts/dock.sh``,
which is a simple Bash script that is going to be sourced from
``thinkpad-dock``.

A sample config would look like this::

    dock_loudness="50%"
    disable_wifi=false
    relative_position=left

You can set the following options:

``disable_wifi``
    Whether to set the wifi. *Default:
    true*.

``internal``
    The ``xrandr`` name for the internal monitor. *Default: LVDS1*.

``unmute``
    Whether to change the volume. *Default: true*.

``dock_loudness``
    Volume to set to when docking. *Default: 100%*.

``undock_loudness``
    Volume to set to when undocking. *Default: 50%*.

``set_brightness``
    Whether to change the brightness. *Default: true*.

``brightness``
    Brightness to set to when docking. *Default: 60%*.

``relative_position``
    Where to set the external monitor. Set it to ``right-of`` or ``left-of`` or
    anything else that ``xrandr`` supports with a ``--*`` argument. For
    compatibility reasons, you can also supply ``right`` or ``left``, but it is
    recommended to supply the ``-of`` as well. *Default: right-of*.

``kdialog``
    Please see the appropriate section in thinkpad-rotate(1), it has the same
    option. *Default:*.

Hooks
-----

There are hooks, called before and after the main script. It gets a single
command line argument, ``on`` or ``off``.

- ``~/.config/thinkpad-scripts/hooks/predock``
- ``~/.config/thinkpad-scripts/hooks/postdock``

Example
=======

You can just call ``thinkpad-dock`` and it will do the right thing probably.

If you want, you can tell the script what to do: When you have it sitting on
the docking station, call ``thinkpad-dock on`` to get the external screen
going. When you are done, call ``thinkpad-dock off`` before you disconnect to
get the internal screen back again.

..  vim: spell
