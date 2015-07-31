.. Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>

Find hardware events
====================

The ThinkPad X220 Tablet has a hardware sensor that registers when the screen
is turned around. To find the code of the event, use ``acpi_listen``:

.. code-block:: console

    $ acpi_listen
    video/tabletmode TBLT 0000008A 00000001
    video/tabletmode TBLT 0000008A 00000000

I started the command, turned the screen around, flipped it onto the keyboard
and back again.

This then goes into an ACPI hook file like so:

.. code-block:: ini

    event=video/tabletmode TBLT 0000008A 0000000[01]
    action=/usr/bin/thinkpad-rotate-hook %e

If you give us the output of ``acpi_listen``, we can try to get the hardware
event working for you. The hook in ``tps/hooks.py`` needs to be made aware of
the hardware keys as well in order to decide which action to take.
