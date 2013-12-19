.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
.. Copyright © 2013 Jim Turner <jturner314@gmail.com>

###############
Getting Started
###############

Installation
============

The easiest way to install think-rotate on Ubuntu or Arch Linux is with your
package manager, as described in :ref:`installation-from-package`. If you are on
another distribution, then you can build and install it manually using the
instructions in :ref:`installation-build-manually`.

.. _installation-from-package:

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

.. _installation-build-manually:

Build Manually
--------------

First install all the dependencies, listed in :ref:`installation-dependencies`.
Then, you can build and install with::

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

.. _installation-dependencies:

Dependencies
------------

These dependencies refer to Debian and Arch Linux packages, but should have
similar names in other distributions. ``yum`` in Fedora and ``zypper`` in
openSUSE have a search for “provides”. In openSUSE, you could use the ``cnf``
tool to find out the package.

Build
'''''

These programs are needed during the build process.

============== ============== ==================
Needed Program Debian package Arch Linux package
============== ============== ==================
msgfmt         gettext        gettext
xgettext       gettext        gettext
sphinx-build   python3-sphinx python-sphinx
============== ============== ==================

Run
'''

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
````````

These programs enhance the functionality of the scripts, but are not strictly
required.

============== ================== ================== ===========================
Needed Program Debian package     Arch Linux package For
============== ================== ================== ===========================
kdialog        kde-baseapps-bin   kdebase-kdialog    showing dialog boxes
kvkbd          kvkbd              kvkbd              virtual keyboard
nmcli          network-manager    networkmanager     changing wifi
pactl          pulseaudio-utils   libpulse           volume control when docking
qdbus          qdbus, qt4-default qt4                showing dialog boxes
xbacklight     xbacklight         xorg-xbacklight    adjusting brightness
============== ================== ================== ===========================

Setup
=====

think-rotate includes files that hook into various hardware events:

* a udeb hwdb file that allows proper operation of the bezel buttons on ThinkPad
  X220 and X230 Tablet computers

* udev rules to automatically run think-dock when docking and undocking

* ACPI hooks to automatically call think-rotate when the screen is
  rotated/unrotated

All of these files should be installed as part of the installation process. If
acpid is not enabled by default on your computer (which is the case for Arch
Linux), you need to enable and start it for the ACPI hooks to work.
Additionally, after installing think-rotate, you may need to restart udev and
acpid for the new rules and hooks to take effect.

Usage
=====

After following the configuration instructions above, you generally will not
need to call any of the scripts manually. However, in case you do, this is a
synopsis of each command::

    think-dock [on|off]
    think-mutemic
    think-rotate [direction]
    think-touch [on|off]
    think-touchpad

See the :doc:`manual pages <../man/index>` for more details.

Configuration
=============

You can modify the default configuration for things such as the screen
brightness to set when docking, the relative positions of displays, and the
direction of screen rotation by placing configuration scripts in
``$HOME/.config/think-rotate``. See the :doc:`manual pages <../man/index>` for
more details.

You can also add scripts that will be called before/after docking or rotating
the display. See the man pages for :doc:`../man/think-dock.1` and
:doc:`../man/think-rotate.1` for more details.

Tips
====

think-rotate fixes the bezel buttons so that they work, but it does not bind
anything to them by default. If you'd like, you can bind the think-rotate script
(or any other program for that matter) to one of the bezel buttons using your
desktop environment. For example, under GNOME, go to Settings > Keyboard >
Shortcuts > Custom Shortcuts and add a new "shortcut".

think-rotate includes a script, think-touch, to make it easy to toggle the
touchscreen of the X220 Tablet on/off. If you want to disable your touch screen
on startup, use your desktop environment to call ``think-touch off`` when
starting.

Under KDE, it is convenient to place all of the scripts in a drawer so that you
can access them quickly. See :doc:`kde-script-drawer` for instructions to do
this.
