..  Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
    Copyright © 2015 Jim Turner <jturner314@gmail.com>
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

    You can omit this option and the script will guess what to do by checking
    whether a dock is docked in ``/sys``.

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

You can create a config file in ``$HOME/.config/thinkpad-scripts/config.ini``,
which has standard INI format. The old config can be converted using the
``thinkpad-scripts-config-migrate`` script that was introduced in version 4.0.

A sample config would look like this:

.. code-block:: ini

    [sound]
    dock_loudness = 50%

    [network]
    disable_wifi = true

    [screen]
    relative_position = left-of

I will list all possible options in a moment. Since the INI format is
hierarchical, I will denote the options with a dot. The first one would be
``sound.dock_loudness`` for example.

Those are the possible options:

``hooks.postdock``
    Full path to postdock hook. *Default: ~/.config/thinkpad-scripts/hooks/postdock*

``hooks.predock``
    Full path to predock hook. *Default: ~/.config/thinkpad-scripts/hooks/predock*

``logging.syslog``
    Whether to log everything to syslog. *Default: true*

``network.disable_wifi``
    Whether to set the wifi. *Default: true*.

``network.restart_connection``
    If this is set, the given network connection will be restarted on startup.
    I (Martin Ueding) have seen the issue where my default DHCP connection
    would not work right away. Restarting that connection helped. *Default:
    true*

``network.connection_name``
    If the connection should be restarted, you can specify which one in case
    there is more than one wired connection. The default case is to use the
    lexicographically first connection name in the list provided by ``nmcli``
    that contains the case-insensitive string ``'ethernet'``.

``screen.internal``
    The ``xrandr`` name for the internal monitor. *Default: LVDS1*.

``screen.primary``
    The ``xrandr`` name for the primary monitor when docked or an empty string
    to guess a reasonable monitor. *Default: (empty string)*.

``screen.secondary``
    The ``xrandr`` name for the secondary monitor when docked or an empty
    string to guess a reasonable monitor. *Default: (empty string)*.

``screen.set_brightness``
    Whether to change the brightness. *Default: true*.

``screen.brightness``
    Brightness to set to when docking. *Default: 60%*.

``screen.relative_position``
    Where to set the primary monitor relative to the secondary monitor when
    docking. Set it to ``right-of`` or ``left-of`` or anything else that
    ``xrandr`` supports with a ``--*`` argument. *Default: right-of*.

``sound.unmute``
    Whether to change the volume. *Default: true*.

``sound.dock_loudness``
    Volume to set to when docking. *Default: 100%*.

``sound.undock_loudness``
    Volume to set to when undocking. *Default: 50%*.

``gui.kdialog``
    Please see the appropriate section in thinkpad-rotate(1), it has the same
    option. *Default:*.

Hooks
-----

There are hooks, called before and after the main script. It gets a single
command line argument, ``on`` or ``off``.

- ``~/.config/thinkpad-scripts/hooks/predock``
- ``~/.config/thinkpad-scripts/hooks/postdock``

You can change the path of those hooks in the configuration, see above.

Example
=======

You can just call ``thinkpad-dock`` and it will do the right thing probably.

If you want, you can tell the script what to do: When you have it sitting on
the docking station, call ``thinkpad-dock on`` to get the external screen
going. When you are done, call ``thinkpad-dock off`` before you disconnect to
get the internal screen back again.

..  vim: spell
