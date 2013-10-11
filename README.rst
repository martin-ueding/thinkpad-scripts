.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

Website
=======

Motivation for this project is on the `project website
<http://martin-ueding.de/en/projects/think-rotate#pk_campaign=git>`_.

Installation
============

From Package
------------

On Ubuntu and its derivatives, you can install from `Martin's PPA`_::

    $ sudo -s
    # add-apt-repository ppa:martin-ueding/stable
    # apt-get update
    # apt-get install think-rotate

On Arch Linux, you can install the ``think-rotate`` package from the AUR_
(coming soon).

.. _Martin's PPA: https://launchpad.net/~martin-ueding/+archive/stable
.. _AUR: http://aur.archlinux.org

Build Manually
--------------

First install all the dependencies, listed in the following section.  Then, you
can build and install with::

    $ make
    # make install

If you set a ``DESTDIR``, you will also need to run::

    # service acpid restart

Dependencies
============

These dependencies refer to Debian and Arch Linux packages, but should have
similar names in other distributions. ``yum`` in Fedora and ``zypper`` in
openSUSE have a search for “provides”. In openSUSE, you could use the ``cnf``
tool to find out the package.

Build
-----

These programs are needed during the build process.

================ =============== ==================
Needed Program   Debian package  Arch Linux package
================ =============== ==================
msgfmt, xgettext gettext         gettext
rst2man          python-docutils python-docutils
================ =============== ==================

Run
---

These programs are required for the execution of the scripts.

============== ======================== ==================
Needed Program Debian package           Arch Linux package
============== ======================== ==================
*acpid*        acpid                    acpid
amixer         alsa-utils               alsa-utils
nmcli          network-manager          networkmanager
*udev*         udev                     systemd
xsetwacom      xserver-xorg-input-wacom xf86-input-wacom
xbacklight     xbacklight               xorg-xbacklight
xinput         xinput                   xorg-xinput
xrandr         x11-xserver-utils        xorg-xrandr
setkeycodes    kbd                      *not applicable*
============== ======================== ==================

Optional
~~~~~~~~

These programs enhance the functionality of the scripts, but are not strictly
required.

=========================== ============== ================ ==================
For                         Needed Program Debian package   Arch Linux package
=========================== ============== ================ ==================
volume control when docking pactl          pulseaudio-utils libpulse
showing dialog boxes        kdialog        kde-baseapps-bin kdebase-kdialog
virtual keyboard            kvkbd          kvkbd            kvkbd
=========================== ============== ================ ==================

Manual / How To Use
===================

We document the usage and configuration of the programs in their manual pages.
If you have the software installed, you can just use ``man think-rotate`` to
read it.

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
