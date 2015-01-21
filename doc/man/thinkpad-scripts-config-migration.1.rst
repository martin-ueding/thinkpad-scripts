..  Copyright © 2015 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

#################################
thinkpad-scripts-config-migration
#################################

.. only:: html

    migrates the config from versions 3.x to 4.x

    :Author: Martin Ueding <dev@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-scripts-config-migration

Description
===========

The versions 3.x and before of |project| were Bash shell scripts. The
configuration files also were shell scripts that the main script would
``source`` (execute within the main script) to set the configuration values.

With version 4.0, the complete project was rewritten in Python 3. The
configuration format was changed to INI since the Python standard library ships
the ``configparser`` module to handle those easily.

Users of the old version with configurations should be able to convert this
into the new format with this tool. Since the 3.x configuration files could be
programs really, there is no perfect way to parse them and turn them into INI
files. This program tries to parse it and should work fine if your
configuration file consists of simple variable assignments.

It will read the files ``~/.config/thinkpad-scripts/rotate.sh`` and
``~/.config/thinkpad-scripts/dock.sh`` and interpret them. All the errors will
be shown as well as the configuration that is understood. You will be prompted
whether to actually save the new configuration.

Options
=======

This program does not take any options.

.. include:: ../man-epilogue.rst

.. vim: spell tw=79
