.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

############
think-rotate
############

Website
=======

Motivation for this project is on the `project website
<http://martin-ueding.de/en/projects/think-rotate#pk_campaign=git>`_. You will
find release ``.tar.gz`` archives there as well. Also, git URLs are provided on
the website.

Issues and pull requests are tracked on the `GitHub page
<https://github.com/martin-ueding/think-rotate>`_.

Installation
============

From Package
------------

On Ubuntu and its derivatives, you can install from `Martin's PPA`_::

    $ sudo -s
    # add-apt-repository ppa:martin-ueding/stable
    # apt-get update
    # apt-get install think-rotate

On Arch Linux, you can install the ``think-rotate`` package from the AUR_.

.. _Martin's PPA: https://launchpad.net/~martin-ueding/+archive/stable
.. _AUR: https://aur.archlinux.org/packages/think-rotate

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
``90-X2x0T-keyboard.hwdb``::

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

============== ================ ================== ===========================
Needed Program Debian package   Arch Linux package For                        
============== ================ ================== ===========================
kdialog        kde-baseapps-bin kdebase-kdialog    showing dialog boxes       
kvkbd          kvkbd            kvkbd              virtual keyboard           
nmcli          network-manager  networkmanager     changing wifi              
pactl          pulseaudio-utils libpulse           volume control when docking
qdbus          qdbus            qt4                showing dialog boxes       
xbacklight     xbacklight       xorg-xbacklight    adjusting brightness       
============== ================ ================== ===========================

Manual / How To Use
===================

We document the usage and configuration of the programs in their manual pages.
If you have the software installed, you can just use ``man <program-name>`` to
read the man page corresponding to ``<program-name>``.

In case that you want to read the manual pages online, you can use the
following links:

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

We also have a few guides in ``doc/guides`` for other topics, available at the
following links:

- `Configuring additional hardware keys
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/guides/additional-keys.rst>`_
- `Script drawer for KDE plasma panel
  <https://github.com/martin-ueding/think-rotate/blob/master/doc/guides/kde-script-drawer.rst>`_

Legal
=====

This program is licensed under GPLv2+. See `COPYING.rst`_ for more information.

.. _COPYING.rst: https://github.com/martin-ueding/think-rotate/blob/master/COPYING.rst

ThinkPad® is a trademark of Lenovo®. This project is not affiliated with,
sponsored by, or endorsed by Lenovo. Our use of the term “ThinkPad” is purely
descriptive since this collection of scripts is only applicable to said type of
computers.

.. vim: spell
