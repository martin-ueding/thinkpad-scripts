.. Copyright © 2015 Jim Turner <jturner314@gmail.com>

###############################
Hardware-Specific Configuration
###############################

Introduction
============

Most of the configuration parameters (described in the individual :doc:`man
pages <../man/index>`) depend on your own personal preferences. However, some
parameters depend on your specific model of computer. This page provides
recommended values for various computers.

Unlisted Hardware
=================

If your particular model of computer is not listed here, please submit a `pull
request <https://github.com/martin-ueding/thinkpad-scripts/pulls>`_ with the
correct configuration or create a report on the `issue tracker
<https://github.com/martin-ueding/thinkpad-scripts/issues>`_ with the name of
your computer and output of:

.. code-block:: console

    $ xinput
    $ xrandr

Recommended Configurations
==========================

Functional configurations for computers that users have reported so far are
listed below.

Lenovo Thinkpad X200 & Lenovo Thinkpad X200 Tablet
--------------------------------------------------

Some of the hardware devices are named differently from the defaults. These are
the necessary configuration parameters:

.. code-block:: ini

    [input]
    touchscreen_device = Serial Wacom Tablet touch

    [touch]
    regex = Serial Wacom Tablet.*id: (\d+).*

Lenovo Thinkpad X220 & Lenovo Thinkpad X220 Tablet
--------------------------------------------------

The defaults should work fine.

Lenovo Thinkpad X230 & Lenovo Thinkpad X230 Tablet
--------------------------------------------------

The defaults should work fine.

Lenovo Thinkpad Yoga
--------------------

Some of the hardware devices are named differently from the defaults. These are
the necessary configuration parameters:

.. code-block:: ini

    [input]
    touchscreen_device = ELAN Touchscreen

    [screen]
    internal = eDP1
