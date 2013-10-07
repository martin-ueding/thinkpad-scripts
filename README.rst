.. Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

Website
=======

All information about the scripts and what they do, is on my website:
http://martin-ueding.de/en/projects/think-rotate#pk_campaign=git.

Dependencies
============

Build
-----

- python-docutils

Run
---

- udev >= 196

Installation
============

You can build and install with::

    make
    make install

Packagers will also need to add the following line, run as root, to their post
installation hook to update the udev hardware database with the information in
``90-X220T-keyboard.hwdb``::

    udevadm hwdb --update

.. vim: spell
