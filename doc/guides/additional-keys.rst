.. Copyright © 2013 Jim Turner <jturner314@gmail.com>

####################################
Configuring Additional Hardware Keys
####################################

Introduction
============

Keys are identified on multiple levels in Linux: *scancode*, *keycode*, and
*keysym*. A *scancode* is the sequence of bytes that a keyboard sends to a
computer when a key is pressed. A *keycode* corresponds to a specific
function. A *keysym* corresponds to a symbol typed by the keyboard and mappings
of *scancodes* to *keysyms* depend on the keyboard layout. The progression of
mapping goes *scancode* → *keycode* → *keysym.* [#f1]_ By default, some unusual
hardware keys, such as those on the bezels of some tablets, are not mapped. This
guide explains how to map *scancodes* to *keycodes* using the udev hwdb, which
is part of udev versions 196 and later.

Directions
==========

Determine the scancodes of the keys
-----------------------------------

#. Determine your Linux kernel version with::

    $ uname -r

#. For kernels v2.6 and later, you need reboot with the kernel parameter
   ``atkbd.softraw=0`` in order for the following step to work [#f1]_. Detailed
   instructions on how to add kernel parameters are provided in [#f2]_.

#. Switch to a virtual console with a text terminal with ``Ctrl-Alt-F2``, login,
   then run as root [#f1]_::

    # showkey --scancodes

   When you press a key, it should send the scancode to stdout. Sometimes,
   pressing and releasing a key have two different scancodes, and both scancodes
   will show up in the output of ``showkey --scancodes``. For example, pressing
   and releasing the screen rotation bezel key on the X220 tablet gives the
   keycodes ``0x67`` and ``0xe7``. Just choose the one that occurs when you
   initially press the key. For the keys that you want to map, write down which
   key corresponds to which scancode. Mappings for older ThinkPad tablets are
   available at [#f6]_.

#. You can switch back to your graphical environment with a key combination
   somewhere between ``Ctrl-Alt-F1`` and ``Ctrl-Alt-F7`` and then reboot to
   restore your default kernel parameters.

Determine which keycodes you want to map them to
------------------------------------------------

#. Look in ``/lib/udev/hwdb.d/60-keyboard.hwdb`` for mappings of some other
   ThinkPad models [#f3]_; these provide a guide for which key should correspond
   to which keycode. (The mappings are up to you, but it's a good idea to pick
   mappings similar to already established ones.)

#. A complete list of possible keycodes is in ``/usr/include/linux/input.h``
   [#f3]_. Look for the definitions with the names ``KEY_<KEYCODE>``.

Determine the modalias string of your keyboard
----------------------------------------------

#. Use this command to list all of the modalias entries on your system [#f4]_::

    $ find /sys -name modalias -print0 | xargs -0 cat | sort -u

#. Determine the modalias string that corresponds to your keyboard. The relevant
   one will probably start with ``dmi``. One example from an X220 tablet is::

    dmi:bvnLENOVO:bvr8DET46WW(1.16):bd05/18/2011:svnLENOVO:pn42962WU:pvrThinkPadX220Tablet:rvnLENOVO:rn42962WU:rvrNotAvailable:cvnLENOVO:ct10:cvrNotAvailable:

Write and install a udev hwdb configuration file
------------------------------------------------

#. Create a hwdb file with the mappings that you want. Here is the file from
   ``think-rotate``, named ``90-X220T-keyboard.hwdb``::

    # Thinkpad X220_Tablet
    keyboard:dmi:bvn*:bvr*:bd*:svnLENOVO*:pn*:pvrThinkPadX220Tablet*
    KEYBOARD_KEY_67=cyclewindows                           # bezel circular arrow
    KEYBOARD_KEY_6c=scale                                  # rotate screen

   * Anything after a ``#`` is a comment and is ignored.

   * The second line is a pattern that should match the modalias string of your
     keyboard. This example matches the modalias string in the previous
     section.

   * The following lines are the mappings. Each line is in the form
     ``KEYBOARD_KEY_<scancode>=<keycode>``. The ``<scancode>`` should be the
     value you obtained earlier without the ``0x`` at the front, and the
     ``<keycode>`` should be the keycode you selected earlier but in all
     lowercase.

#. Give the file an appropriate name, such as ``90-X220T-keyboard.hwdb``, and
   place it in ``/lib/udev/hwdb.d/``.

See [#f3]_ for more details.

Update the udev hwdb
--------------------

#. Run the following to update the udev hwdb::

     # udevadm hwdb --update

#. You may need to reboot for the changes to take effect.

Where to go from here
---------------------

* Now that you have properly mapped keycodes, you need to bind functionality to
  them. You can do this with your desktop environment's settings manager.

* Note that some keycodes may not be mapped to keysyms, so your desktop
  environment may not recognize them. In this case, the easiest thing to do is
  to choose a different keycode for that key. (This is what I did for the X220
  screen rotation button in ``think-rotate``: based on other ThinkPad models in
  ``/lib/udev/hwdb.d/60-keyboard.hwdb``, the ``direction`` keycode would be the
  better choice than ``scale``. However, ``direction`` was not mapped in my
  desktop environment, so it was easier just to choose a different keycode that
  wasn't mapped to anything.) The alternative is to use a utility like xmodmap
  to perform the mapping of keycode to keysym [#f5]_.

* You can find some interesting tricks at this (somewhat out-of-date) page:
  [#f7]_.

References
==========

.. [#f1] https://wiki.archlinux.org/index.php/Extra_Keyboard_Keys
.. [#f2] https://wiki.archlinux.org/index.php/Kernel_parameters
.. [#f6] http://www.thinkwiki.org/wiki/Tablet_Hardware_Buttons
.. [#f3] https://wiki.archlinux.org/index.php/Map_scancodes_to_keycodes
.. [#f4] http://people.skolelinux.org/pere/blog/Modalias_strings___a_practical_way_to_map__stuff__to_hardware.html
.. [#f5] https://wiki.archlinux.org/index.php/Xmodmap
.. [#f7] http://www.thinkwiki.org/wiki/How_to_get_special_keys_to_work
