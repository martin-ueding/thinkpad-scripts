..  Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
    Licensed under The GNU Public License Version 2 (or later)

###
API
###

:Date: 2014-03-03

There are a couple Bash library functions in ``lib``. They are sourced in some
of the scripts, providing common functionality. Attempting to write a library
in Bash is pretty weird, but it should be documented because of this.

All those functions have a horrible amount of global (environment) variables,
that it is crucial to keep track of all the side effects. At this point I
wish that Bash had named arguments and variable scoping.

File ``external.sh``
====================

Function ``find-external``
--------------------------

Tries to find the external screen using ``xrandr``. Since Jim Turner had some
race condition, it tries once every second for five seconds. After that, the
variable ``external`` is either empty (or not set?) or has the name of the
external screen set to it.

Environment variables needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: internal

    Identifier of the internal screen.

Environment variables provided
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: external

    Identifier of the external screen, when it was found.

File ``kdialog.sh``
===================

Function ``kdialog-init``
-------------------------

Opens a new progress bar.

Options
~~~~~~~

.. option:: $1

    Title text.

.. option:: $2

    Number of segments.

Environment variables needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: kdialog

    Determines whether kdialog is used.

    Values: ``true`` or other.

Environment variables provided
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: kdialog_handle

    Stores the D-Bus handle of the progress bar after initialisation.

.. envvar:: kdialog_number

    Set to 0, will used by other functions.

Function ``kdialog-update``
---------------------------

Updates text and percentage on the progress bar.

Options
~~~~~~~

.. option:: $1

    New label text.

Environment variables needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: kdialog

.. envvar:: kdialog_handle

.. envvar:: kdialog_number

    Current state of the progress bar. This will be incremented by 1 as a side
    effect.

Function ``kdialog-exit``
-------------------------

Closes the progress bar.

Environment variables needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: kdialog

.. envvar:: kdialog_handle

File ``upgrade.sh``
===================

Function ``run-upgrades``
-------------------------

Runs all the upgrades that are provided in this “Bash module”.

Function ``run-3.3-to-3.4``
---------------------------

Performs upgrade tasks from version 3.3 to 3.4. That was the version where the
project got renamed from “think-rotate” to “thinkpad-scripts”. It will change
the ``~/.config/think-rotate`` to ``~/.config/thinkpad-scripts``, unless the
new directories exist already. This should not overwrite anything.

.. vim: tw=79 spell
