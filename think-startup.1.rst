#############
think-startup
#############

**********************************************************
run docking- and tablet-related commands on system startup
**********************************************************

:Author: Jim Turner <jturner314@gmail.com>
:Date: 2012-12-26
:Manual section: 1

SYNOPSIS
========

::

    think-startup

DESCRIPTION
===========

This program runs various commands on system startup. It sets the key codes of
the bezel keys on the Thinkpad X220 Tablet so that they are assignable for
various things, such as rotating the screen. It also allows the user to disable
the touch screen on startup.

There will be a line installed in ``/etc/rc.local`` that will automatically run
``think-startup`` when the system starts.

what it does
------------

When called, the following things are done:

- Set the key codes of the bezel keys so that they are assignable.
- Depending on the value of ``disable_touch``, enable/disable the touch screen.

EXIT STATUS
===========

0
    Everything okay.
1
    Some error.

FILES
=====

You can create a config file in ``$HOME/.config/think-rotate/startup.sh``, which
is a simple Bash script that is going to be sourced from ``think-startup``.

A sample config would look like this::

    disable_touch=true

You can set the following option:

``disable_touch``
    Whether to enable/disable the touch screen. Set it to ``true`` or something
    else.

EXAMPLE
=======

You can just call ``think-startup``.
