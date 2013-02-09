.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

:License (Code): GPLv2_
:License (Text): CC-BY_
:Tags: Bash, Python, ThinkPad

.. contents::
    :local:

This collection of scripts is intended for the Lenovo ThinkPad X220 Tablet. You
can still use them with the regular X220 machine, but only ``think-rotate``
will probably be useless for you then. I think that most scripts will also be
handy for other ThinkPad models, I have not tested them though.

The buttons on the front of the screen are mapped, so that you can use them. I
have ``think-rotate`` on that 90° button and ``think-rotate flip`` on that 270°
button.

In short, this script fixes or improves the following:

#. Rotation of the internal screen and any Wacom touch and pen input devices
   using the bezel buttons.

#. Get the microphone mute button to work. 
#. Automatically use any external monitor, speakers and LAN connection when
   docking onto an UltraBase or similar.

#. Ability to disable touch pad or touch screen.

the scripts
===========

think-dock
----------

There is also a script that will enable an external monitor and correctly sets
the Wacom input devices onto the internal screen only. This is very handy if
you use the docking station (UltraBase) with an external monitor.

It will also set the volume to full when docking and to half when un-docking,
disable and enable the wireless LAN if a LAN cable is attached. And it sets the
brightness to a fixed value. You can set this value in a config file to match
your external monitor.

``udev`` is instructed to call ``think-dock on`` when you set your laptop into
the docking station, and ``think-dock off`` when you press the eject-button.
That way, you do not have to worry about managing screens. Just set your laptop
and it will take care of everything.

think-keycodes
--------------

You will not need to call this manually, it will be called on system startup.
It sets the key codes for the bezel keys in order for you to use them.

think-mutemic
-------------

This script will be called when you press the microphone mute button. It will
mute the microphone and toggle the LED. It currently uses the power button LED
for status in order to avoid a kernel module patch. [mutemic]_

think-rotate
------------

With this script, you can rotate the screen in any direction you like and it
will also rotate the pen and touch input.

It will also disable the track point (the xinput id is automatically queried)
so that the back of the screen does not move your mouse if there is any force
on the side of the screen.

think-touch
-----------

This script toggles the (finger) touch screen. This might be handy, if you are
taking notes with the pen only.

think-touchpad
--------------

This script toggles the touch pad.

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

.. vim: spell
