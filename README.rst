.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

Website
=======

Motivation for this project is on the `project website
<http://martin-ueding.de/en/projects/think-rotate#pk_campaign=git>`_.

Dependencies
============

These dependencies refer to Debian and Arch Linux packages, but should have
similar names in other distributions.

Build
-----

=============== ==================
Debian package  Arch Linux package
=============== ==================
gettext         gettext
python-docutils python-docutils
=============== ==================

Run
---

======================== ==================
Debian package           Arch Linux package
======================== ==================
acpid                    acpid
alsa-utils               alsa-utils
network-manager          networkmanager
udev                     systemd
xserver-xorg-input-wacom xf86-input-wacom
xbacklight               xorg-xbacklight
xinput                   xorg-xinput
xrandr                   xorg-xrandr
======================== ==================

Optional
--------

=========================== ================ ==================
For                         Debian package   Arch Linux package
=========================== ================ ==================
volume control when docking pulseaudio-utils libpulse
showing dialog boxes        kde-baseapps-bin kdebase-kdialog
virtual keyboard            kvkbd            kvkbd
=========================== ================ ==================

Installation
============

You can build and install with::

    make
    make install

If you set a ``DESTDIR``, you will also need to run::

    service acpid restart

Manual / How To Use
===================

We document the usage and configuration of the programs in their manual pages. If you have the software installed, you can just use ``man think-rotate`` to read it.

In case that you want it read online, you can use the following links:

- `think-dock
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/think-dock.1.rst>`_
- `think-mutemic
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/think-mutemic.1.rst>`_
- `think-rotate
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/think-rotate.1.rst>`_
- `think-touch
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/think-touch.1.rst>`_
- `think-touchpad
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/think-touchpad.1.rst>`_

.. vim: spell
