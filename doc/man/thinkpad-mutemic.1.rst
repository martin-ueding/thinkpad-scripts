..  Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

################
thinkpad-mutemic
################

.. only:: html

    toggle the microphone mute status

    :Author: Martin Ueding <dev@martin-ueding.de>
    :Manual section: 1

Synopsis
========

::

    thinkpad-mutemic

Description
===========

Toggles the microphone mute status. It will also turn the power LED into a
blinking mode to signal that the microphone is muted. The mute light itself can
only be accessed with a patched kernel module, so we do not do that yet.
