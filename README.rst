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

To make the ACPI hooks take effect, you will need to restart ``acpid`` with the
following on SysVinit/Upstart systems::

    # service acpid restart

or on systemd systems::

    # systemctl restart acpid

Packagers will also need to add the following line, run as root, to their post
installation hook to update the udev hardware database with the information in
``90-X220T-keyboard.hwdb``::

    udevadm hwdb --update

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
msgfmt           gettext         gettext
xgettext         gettext         gettext
rst2man          python-docutils python-docutils
================ =============== ==================

Run
---

These programs are required for the execution of the scripts.

============== ======================== ================== =======
Needed Program Debian package           Arch Linux package Version
============== ======================== ================== =======
*acpid*        acpid                    acpid
amixer         alsa-utils               alsa-utils
*udev*         udev                     systemd            >= 196
xsetwacom      xserver-xorg-input-wacom xf86-input-wacom
xinput         xinput                   xorg-xinput
xrandr         x11-xserver-utils        xorg-xrandr
============== ======================== ================== =======

Optional
~~~~~~~~

These programs enhance the functionality of the scripts, but are not strictly
required.

=========================== ============== ================ ==================
For                         Needed Program Debian package   Arch Linux package
=========================== ============== ================ ==================
showing dialog boxes        kdialog        kde-baseapps-bin kdebase-kdialog
virtual keyboard            kvkbd          kvkbd            kvkbd
changing wifi               nmcli          network-manager  networkmanager
volume control when docking pactl          pulseaudio-utils libpulse
showing dialog boxes        qdbus          qdbus            qt4
adjusting brightness        xbacklight     xbacklight       xorg-xbacklight
=========================== ============== ================ ==================

Note: To use ``qdbus`` on Arch Linux, you should also install
``qtchooser`` and configure it to use Qt 4 (see the ArchWiki_) or
patch ``lib/kdialog.sh`` to call ``qdbus-qt4`` instead of ``qdbus``.
A patch is available as part of the AUR package (coming soon).

.. _ArchWiki: https://wiki.archlinux.org/index.php/Qt#Default_Qt_Toolkit

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
