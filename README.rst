.. Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

This script is intended for the Lenovo ThinkPad X220 Tablet which features a
Wacom pen and touch screen. With this script, you can rotate the screen in any
direction you like and it will also rotate the pen and touch input.

It will also disable the trackpoint (the xinput id is automatically queried) so
that the back of the screen does not move your mouse if there is any force on
the side of the screen.

Installation
============

Type::

    # make install

This will install the scripts to ``/usr/bin/`` and add the necessary hooks so
that they are run automatically. It also installs a script in ``/etc/init.d/``
that fixes the key codes for the bezel keys so that you can use them for things
such as running ``think-rotate``.

If you want to have the manual pages installed, type ``make`` before you run
``make install``. This needs to have ``rst2man`` from ``python-docutils``
installed.

Usage
=====

Please see the individual manual pages for details on each program:

- think-dock.1.rst
- think-rotate.1.rst
- think-touchpad.1.rst
- think-touch.1.rst
- think-resume.1.rst

License
=======

I took this script from a `forums entry`_ where the original author said:

    “Put this in a file blah.sh anywhere, and do whatever you want with it!”

The changes that I made to that script are licensed unter the GPLv2+.

.. _`forums entry`: http://forum.thinkpads.com/viewtopic.php?p=676101#p676101

Contact
=======

I am Martin Ueding and you can contact me at dev@martin-ueding.de if you have
any questions.

Website
=======

There is also a project website at
http://martin-ueding.de/projects/think-rotate.
