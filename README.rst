.. Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

###############
ThinkPad Rotate
###############

This script is intended for the Lenovo ThinkPad X220 Tablet which features a
Wacom pen and touch screen. With this script, you can rotate the screen in any
direction you like and it will also rotate the pen and touch input.

It will also disable the trackpoint (the xinput id is automatically queried) so
that the back of the screen does not move your mouse if there is any force on
the side of the screen.

Installation
============

Type::

    # make install

If you want to have the manual page installed, type ``make`` before you run
``make install``. This needs to have ``rst2man`` from ``python-docutils``
installed.

Usage
=====

By default, it will rotate to the left, since you can use the battery as a
nice handle then. If you invoke it without any arguments, it will rotate the
screen to the left or back to normal::

    rotate

And then later on::

    rotate

If you want to rotate it to other directions, you can specify the direction,
like so::

    rotate left
    rotate right
    rotate flip
    rotate normal

License
=======

I took this script from a `forums entry
<http://forum.thinkpads.com/viewtopic.php?p=676101#p676101>`_ where the
original author said:

    “Put this in a file blah.sh anywhere, and do whatever you want with it!”

The changes that I made to that script are licensed unter the `Expat License
<http://www.jclark.com/xml/copying.txt>`_, so you are welcome do use it as
you like.
