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

- udev

Installation
============

You can build and install with::

    make
    make install

If you set a ``DESTDIR``, you will also need to run::

    service acpid restart

.. vim: spell
