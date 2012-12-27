############
think-resume
############

**************************************************************
run docking- and tablet-related commands on system resume/thaw
**************************************************************

:Author: Jim Turner <jturner314@gmail.com>
:Date: 2012-12-27
:Manual section: 1

SYNOPSIS
========

::

    think-resume

DESCRIPTION
===========

This program runs various commands on resume from sleep or thaw from hibernate.
It allows the user to disable the touch screen at these times (depending on the
value of ``disable_touch``).

There will be a script installed in ``/etc/pm/sleep.d`` that will automatically
run ``think-resume`` when the system resumes.

EXIT STATUS
===========

0
    Everything okay.
1
    Some error.

FILES
=====

You can create a config file in ``$HOME/.config/think-rotate/resume.sh``, which
is a simple Bash script that is going to be sourced from ``think-resume``.

A sample config would look like this::

    disable_touch=true

You can set the following options:

``disable_touch``
    Whether to enable/disable the touch screen. Set it to ``true`` or something
    else.

EXAMPLE
=======

You can just call ``think-resume`` and it will do the right thing. (There
shouldn't be a reason why you would need to do this manually, because after
installation, it should be called automatically on system resume.)
