..  Copyright © 2013-2015, 2017 Martin Ueding <dev@martin-ueding.de>
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

What it does
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

``dock.lsusb_indicator_regex``
    Some docks might not have a docking indicator in the sysfs. In `Issue 129
    <https://github.com/martin-ueding/thinkpad-scripts/issues/129>`_ it has
    been discussed to use a particular USB device that is attached only at the
    dock to function as an indicator. If this option is set to a non-zero
    length string, it will be used as a regular expression. The output of
    ``lsusb`` is searched for that regular expression. If a match is found, the
    laptop is assumed to be on the docking station.

    .. admonition:: Example

        The output of ``lsusb`` might contain lines like the following::

            Bus 002 Device 003: ID 056a:00e6 Wacom Co., Ltd TPCE6
            Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
            Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
            Bus 001 Device 003: ID 04f2:b217 Chicony Electronics Co., Ltd Lenovo Integrated Camera (0.3MP)
            Bus 001 Device 006: ID 046d:c05a Logitech, Inc. M90/M100 Optical Mouse
            Bus 001 Device 008: ID 273f:1007  
            Bus 001 Device 005: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
            Bus 001 Device 004: ID 0424:2514 Standard Microsystems Corp. USB 2.0 Hub
            Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
            Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

        Some of these devices might be integrated in the docking station. One
        of the USB hubs is the one in my external screen. That does not help
        much because its ID is not unique. The unnamed device with ID
        ``273f:1007`` is only present on the docking station. Therefore I would
        set the configuration value to ``273f:1007``.

        At the office, I have a second docking station. There I have some other
        device, say ID ``1234:1234``. Since this configuration option is a
        regular expression, I could specify the following:
        ``273f:1007|1234:1234``. Then both devices can trigger the docking
        state.

``gui.kdialog``
    Please see the appropriate section in thinkpad-rotate(1), it has the same
    option. *Default:*.

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

``screen.internal_regex``
    Regular expression to match the ``xrandr`` name for the internal monitor.
    *Default: LVDS-?1|eDP-?1*

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

``screen.internal_docked_on``
    Whether to keep the internal screen on while docking. *Default: true*

``sound.unmute``
    Whether to change the volume. *Default: true*.

``sound.dock_loudness``
    Volume to set to when docking. *Default: 100%*.

``sound.undock_loudness``
    Volume to set to when undocking. *Default: 50%*.

``trigger.dock_triggers``
    Whitespace-delimited list of the enabled hardware triggers to execute
    docking/undocking. The available triggers are ``udev1_on``, ``udev1_off``,
    ``acpi1_on``, ``acpi1_off``, and ``acpi2``.
    *Default:* ``udev1_on udev1_off``

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

.. include:: ../man-epilogue.rst

..  vim: spell
