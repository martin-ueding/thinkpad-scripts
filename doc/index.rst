..  Copyright © 2013 Jim Turner <jturner314@gmail.com>
    Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

###################################################################
|project|: Scripts for ThinkPad X220 Tablet rotation, docking, etc.
###################################################################

Welcome to the documentation for |project|, a set of scripts to automate a
variety of tasks on the ThinkPad X220 Tablet.

If you want to get |project| up an running, then check out the
:doc:`guides/getting-started` guide.

In case you already have |project| set up and just want a quick reference, see
the :doc:`manual pages <man/index>`.

Should there be something working unlike it should on your system and you can't
figure out a solution from the documentation, check the `issue tracker
<https://github.com/martin-ueding/thinkpad-scripts/issues>`_ to see if it is a
known problem. If it's not there, please create a new issue on the issue
tracker.

.. seealso::

    `Project website <http://martin-ueding.de/en/projects/thinkpad-scripts>`_
        - Tar archives with source checkouts
    `GitHub page <https://github.com/martin-ueding/thinkpad-scripts/issues>`_
        - Issue tracker
        - git repository
    `Mailing list <http://chaos.stw-bonn.de/cgi-bin/mailman/listinfo/thinkpad-scripts>`_
        - General help
        - Developer discussion
        - Announcements

Short introduction
==================

This collection of scripts is intended for the Lenovo ThinkPad X220 Tablet. You
can still use them with the regular X220 machine, but only ``thinkpad-rotate``
will probably be useless for you then. I think that most scripts will also be
handy for other ThinkPad models, I have not tested them though.

In short, this script fixes or improves the following:

#. Rotation of the internal screen and any Wacom touch and pen input devices
   using the bezel buttons or physical screen rotation

#. Get the microphone mute button to work.

#. Automatically use any external monitor, speakers and LAN connection when
   docking onto an UltraBase or similar.

#. Ability to disable touch pad or touch screen.

Contents of the documentation
=============================

.. toctree::
    :glob:
    :maxdepth: 2
    :titlesonly:

    guides/index
    man/index
    changelog
    legal
    dev/index

.. vim: spell
