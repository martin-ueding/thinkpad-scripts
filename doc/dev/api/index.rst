.. Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

###
API
###

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

Options
~~~~~~~

.. options:: $1

    Label text

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

.. options:: $1

    Label text

.. envvar:: kdialog_number

    Current state of the progress bar.

.. envvar:: kdialog

.. vim: tw=79 spell
