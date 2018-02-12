.. Copyright © 2012-2015, 2017-2018 Martin Ueding <dev@martin-ueding.de>
.. Copyright © 2013 Jim Turner <jturner314@gmail.com>

###############
Getting Started
###############

Installation
============

The easiest way to install |project| on Ubuntu, Arch Linux, Fedora and openSUSE
is with your package manager, as described in :ref:`installation-from-package`.
If you are on another distribution, then you can build and install it manually
using the instructions in :ref:`installation-build-manually`.

.. _installation-from-package:

From Package
------------

Ubuntu
~~~~~~

On Ubuntu and its derivatives, you can install from `Martin's PPA
<https://launchpad.net/~martin-ueding/+archive/stable>`_:

.. code-block:: console

    $ sudo -s
    # add-apt-repository ppa:martin-ueding/stable
    # apt-get update
    # apt-get install thinkpad-scripts

Arch Linux
~~~~~~~~~~

On Arch Linux, you can install the ``thinkpad-scripts`` package from the `AUR
<https://aur.archlinux.org/packages/thinkpad-scripts>`_.

Fedora
~~~~~~

For Fedora, there is a RPM repository via
the `Open Build Service <https://build.opensuse.org/>`_.

You have to download the ``home:martinueding.repo`` file from the `list of
repositories <https://build.opensuse.org/repositories/home:martinueding>`_ into
``/etc/yum.repos.d/``. Then you can use ``dnf`` to install |project|.

The following commands will do these steps. Just be careful to have the correct
Fedora version in the URL.

.. code-block:: console

    $ sudo -s
    # wget http://download.opensuse.org/repositories/home:/martinueding/Fedora_27/home:martinueding.repo -O /etc/yum.repos.d/home:martinueding.repo
    # dnf install thinkpad-scripts

openSUSE
~~~~~~~~

Currently not packaged, but if you need it, I can try to tweak the Fedora RPM
such that it works on openSUSE.

.. _installation-build-manually:

Build Manually
--------------

First install all the dependencies, listed in :ref:`installation-dependencies`.
Then, you can build and install with:

.. code-block:: console

    $ make
    # make install
    # ./setup.py install

To make the ACPI hooks take effect, you will need to restart ``acpid`` with the
following on SysVinit/Upstart systems:

.. code-block:: console

    # service acpid restart

or on systemd systems:

.. code-block:: console

    # systemctl restart acpid

Packagers will also need to add the following line, run as root, to their post
installation hook to update the udev hardware database with the information in
``90-X2x0T-keyboard.hwdb``:

.. code-block:: console

    # udevadm hwdb --update

Alternatively, you can use ``make full-install`` which does that restarting for
you. However, this does not work when ``DESTDIR`` is set to something! For a
direct installation, use ``make full-install``, for packaging, just use
``make install``.

.. _installation-dependencies:

Dependencies
------------

These dependencies refer to Debian and Arch Linux packages, but should have
similar names in other distributions. ``yum`` in Fedora and ``zypper`` in
openSUSE have a search for “provides”. In openSUSE, you could use the ``cnf``
tool to find out the package.

Build
~~~~~

These programs are needed during the build process.

============== ====================== ================== ================== ==================
Needed Program Debian package         Arch Linux package Fedora package     openSUSE package
============== ====================== ================== ================== ==================
msgfmt         gettext                gettext            gettext            gettext
python3        python3                python             python3-devel      python3-devel
*setuptools*   python3-setuptools     python-setuptools  python3-setuptools python3-setuptools
sphinx-build   python3-sphinx         python-sphinx      python3-sphinx     python3-Sphinx
xgettext       gettext                gettext            gettext            gettext
============== ====================== ================== ================== ==================

Run
~~~

These programs are required for the execution of the scripts.

============== ======================== ================== ===================== ================== =================
Needed Program Debian package           Arch Linux package Fedora package        openSUSE package   Version
============== ======================== ================== ===================== ================== =================
*acpid*        acpid                    acpid              acpid                 acpid
amixer         alsa-utils               alsa-utils         alsa-utils            alsa-utils
linux                                                                                               >= 3.11.0-17 [1]_
python3        python3                  python
*setuptools*   python3-setuptools       python-setuptools  python3-setuptools    python3-setuptools
*udev*         udev                     systemd                                  systemd            >= 196
xinput         xinput                   xorg-xinput        xinput                xinput
xrandr         x11-xserver-utils        xorg-xrandr        xorg-x11-server-utils xrandr
============== ======================== ================== ===================== ================== =================

----

.. [1]

    The Ubuntu Kernel with version ``3.11.0-17`` has a patched
    ``thinkpad-acpi`` module which allows it to control the LED in the
    microphone mute button. Previous versions of |project| would flash the
    power LED to signal a muted microphone. This branch of |project| does not
    flash the power LED anymore, therefore requiring that version of the
    kernel.

    openSUSE and other distributions are not patching the 3.?.0 kernel, but
    ship a 3.?.? kernel. So users of distributions other than Ubuntu (maybe
    even Debian) would have to check whether their kernel has the acpi patch.

Optional
^^^^^^^^

These programs enhance the functionality of the scripts, but are not strictly
required.

============== ======================== ================== =========================================
Needed Program Debian package           Arch Linux package For
============== ======================== ================== =========================================
gsettings      libglib2.0-bin           glib2              subpixel anti-alias order with GNOME/XFCE
kvkbd          kvkbd                    kvkbd              virtual keyboard
lsusb          usbutils                 usbutils           docking detection with a USB device
nmcli          network-manager          networkmanager     changing wifi
pactl          pulseaudio-utils         libpulse           volume control when docking
xbacklight     xbacklight               xorg-xbacklight    adjusting brightness
xsetwacom      xserver-xorg-input-wacom xf86-input-wacom   Wacom device rotation
============== ======================== ================== =========================================

Setup
=====

|project| includes files that hook into various hardware events:

* a udeb hwdb file that allows proper operation of the bezel buttons on ThinkPad
  X220 and X230 Tablet computers

* udev rules to automatically run thinkpad-dock when docking and undocking

* ACPI hooks to automatically call thinkpad-rotate when the screen is
  rotated/unrotated

All of these files should be installed as part of the installation process. If
acpid is not enabled by default on your computer (which is the case for Arch
Linux), you need to enable and start it for the ACPI hooks to work.
Additionally, after installing |project|, you may need to restart udev and
acpid for the new rules and hooks to take effect.

Usage
=====

After following the configuration instructions above, you generally will not
need to call any of the scripts manually. However, in case you do, this is a
synopsis of each command::

    thinkpad-dock [on|off]
    thinkpad-mutemic
    thinkpad-rotate [direction]
    thinkpad-touch [on|off]
    thinkpad-touchpad

See the :doc:`../man/index` for more details.

Configuration
=============

You can modify the default configuration for things such as the screen
brightness to set when docking, the relative positions of displays, and the
direction of screen rotation by placing configuration scripts in
``$HOME/.config/thinkpad-scripts``. See the :doc:`../man/index` for
more details.

You may need to modify some of the parameters depending on your hardware. See
:doc:`hw-specific-config` for more details.

You can also add scripts that will be called before/after docking or rotating
the display. See the man pages for :doc:`../man/thinkpad-dock.1` and
:doc:`../man/thinkpad-rotate.1` for more details.

Tips
====

|project| fixes the bezel buttons so that they work, but it does not bind
anything to them by default. If you'd like, you can bind the ``thinkpad-rotate``
script (or any other program for that matter) to one of the bezel buttons using
your desktop environment. For example, under GNOME, go to “Settings” →
“Keyboard” → “Shortcuts” → “Custom Shortcuts” and add a new “shortcut”.

|project| includes a script, ``thinkpad-touch``, to make it easy to toggle the
touchscreen of the X220 Tablet on/off. If you want to disable your touch screen
on startup, use your desktop environment to call ``thinkpad-touch off`` when
starting.

Under KDE, it is convenient to place all of the scripts in a drawer so that you
can access them quickly. See :doc:`kde-script-drawer` for instructions to do
this.

.. vim: spell
