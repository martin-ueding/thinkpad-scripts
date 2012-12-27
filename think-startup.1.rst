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

This program runs various commands on system startup. At this time, it sets
the key codes of the bezel keys on the Thinkpad X220 Tablet so that they are
assignable for various things, such as rotating the screen.

There will be an line installed in ``/etc/rc.local`` that will automatically run
``think-startup`` when the system starts.

what it does
------------

When called, the following thing is done:

- Set the key codes of the bezel keys so that they are assignable.


EXIT STATUS
===========

0
    Everything okay.
1
    Some error.

EXAMPLE
=======

You can just call ``think-startup``.
