.. Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

#########
Changelog
#########

v3.5.1
    Released: 2014-02-22

    - Small fixes in the manual pages

v3.5
    Released: 2014-02-22

    - **Added**: Set the option ``toggle_unity_launcher`` for
      :doc:`/man/thinkpad-rotate.1` to un-hide the Unity launcher whenever the
      screen is rotated. This was previously an example hook in the guides, now
      it is part of the main suite of scripts.

v3.4
    Released: 2014-02-21

    - Rename all the scripts from ``think-`` to ``thinkpad-`` to match the new
      project name. To ease transition, there are transition scripts with the
      old names. **Be sure to adjust all your scripts and hooks accordingly!**
      The transition scripts will be dropped with version 4.0.
    - Rename the configuration directory from ``~/.config/think-rotate`` to
      ``~/.config/thinkpad-scripts``. There is an automatic upgrade script in
      place, so calling either ``thinkpad-rotate`` or ``thinkpad-dock`` will
      rename your configuration folder if it exists and there is no new one
      already existing.
    - Put dates into the changelog, for all releases so far.

v3.3
    Released: 2014-02-21

    - Rename project to “thinkpad-scripts”
    - Add subpixel anti-alias order change on rotation for Gnome

v3.2
    Released: 2014-01-07

    - Update copyright years in the documentation.
    - Add a guard that prevents multiple execution of ``think-dock`` and
      ``think-rotate``. For some reason, the ``udev`` hooks call the script
      twice, resulting in race conditions.

v3.1.2
    Released: 2014-01-07

    - Fix finding of external display. I tried to improve the syntax, but let
      the script fail whenever the number needed to be incremented.

v3.1.1
    Released: 2014-01-05

    - Clean all ``*.pyc`` files in makefile. This was causing errors with
      prisine tars and Debian packaging before.
    - Add changelog to documentation

v3.1
    Released: 2014-01-03

    - Pass target orientation to postrotate hook
    - Pass version number to Sphinx automatically from the changelog

v3.0.2
    Released: 2013-12-19

    - Manual pages with Sphinx

v3.0.1
    Released: 2013-12-10

    - Allow more relative positions by putting the ``-of`` into the value of
      the ``relative_position`` variable

v3.0
    Released: 2013-12-01

    - Settings of the keycodes is now done via a ``.hwdb`` file for ``udev``.
      This requires ``udev`` to be of version 196 or greater. Therefore, it is
      marked as a major release, since it breaks Ubuntu 13.04 and earlier.

v2.11
    Released: 2013-12-01

    - Add some guides: “Additional Keys” and “KDE Script Drawer”
    - Fix recursive make, pass ``-j`` down to child processes

v2.10.2
    Released: 2013-10-30

    - Actually return from function.

v2.10.1
    Released: 2013-10-28

    - Do not fail if ``qdbus`` does not work (like on vanilla Kubuntu 13.10)

v2.10
    Released: 2013-10-28

    - Print missing programs
    - Do not fail if ``qdbus`` is missing

v2.9
    Released: 2013-10-07

    - **Added**: ACPI hook to call ``think-rotate`` (Jim Turner)
    - **Added**: Support for systemd network inferface names (Jim Turner)
    - **Removed**: ``think-resume`` (Jim Turner)
    - Use syslog in ``think-dock``
    - Update documentation
    - State all dependencies (Debian package names)
    - Change indentation to four spaces instead of a single tab

v2.8.1
    Released: 2013-09-30

    - More logging to syslog
    - Disable ``kdialog`` for ACPI hooks since that does now work well

v2.8
    Released: 2013-09-24

    - Translate to German

v2.7.1
    Released: 2013-08-08

    - Close KDialog progress bar when the script fails (via ``trap``)

v2.7
    Released: 2013-07-31

    - **Added**: Hooks
    - **Added**: ``on|off`` for the ``think-touchpad`` script

v2.6
    Released: 2013-06-26

    - Support for ``kdialog`` status.

v2.5.2
    Released: 2013-05-10

    - Update the ACPI hooks to find other docks as well

v2.5.1
    Released: 2013-05-06

    - Find other docks as well

v2.5
    Released: 2013-02-03

    - Get microphone mute button to work

v2.4.1
    Released: 2012-12-29

    - Actually install makefiles
    - Implement required actions in ``init.d`` script to that Debian lintian
      does not complain

v2.4
    Released: 2012-12-29

    - Fix bezel keyboard codes, so that they are usable. (Jim Turner)
    - Add script to toggle touch screen. (Jim Turner)
    - Organize code in subdirectories, using recursive make.

v2.3.1
    Released: 2012-11-02

    - Map Wacom devices to the output when rotating in any case. Thanks to Jim
      Turner!

v2.3
    Released: 2012-10-25

    - Add support for other virtual keyboards. Thanks to Jim Turner!
    - Use shorter redirection (``&>`` instead of ``2>&!``).

v2.2.1
    Released: 2012-10-22

    - Fix spelling typo in ``relative_position``. Thanks to Jim Turner!

v2.2
    Released: 2012-10-15

    - Background most tasks so that they run in parallel. This should speed up
      docking.

v2.1
    Released: 2012-10-06

    - Only set Wacom screen devices. That way, any attached Wacom graphics
      tablet is not affected by the docking.

v2.0
    Released: 2012-08-31

    - Use the kernel to determine what the docking status is.
    - Add ``udev`` rules to perform the docking action.

v1.5
    Released: 2012-08-31

    - Desktop files for think-dock.

v1.4.5
    Released: 2012-07-21

    - Revert too intelligent behavior.

v1.4.4
    Released: 2012-07-21

    - Even if the user calls ``think-dock on``, do not dock if there is no
      external monitor attached. This might be the case when the ``think-dock
      on`` is called automatically without any prior checks. If the script
      would dock either way, it might disable wireless (although that is only
      done when ``eth0`` is connected) and set the volume to a wrong setting.

v1.4.3
    Released: 2012-07-20

    - Disable the wireless connection on docking.

v1.4.2
    Released: 2012-07-20

    - Fix commands in ``.desktop`` files.

v1.4.1
    Released: 2012-07-20

    - Install ``.desktop`` files.

v1.4
    Released: 2012-07-20

    - Query the state of the whole system automatically and determine the right
      action. You can still specify ``on`` or ``off``, if you want to.

v1.3
    Released: 2012-07-16

    - Optional config file for ``think-dock``.

v1.2.2
    Released: 2012-07-16

    - Fix flip direction.

v1.2.1
    Released: 2012-07-16

    - Disable wireless only when eth0 connected.
    - Document options.

v1.2
    Released: 2012-07-15

    - Change display brightness on docking.

v1.1
    Released: 2012-07-15

    - Check whether programs are there before using them.
    - Create directories on ``make install``.
    - Disable wifi when going onto the docking station.
    - Enable sound on docking.
    - Lower the volume after docking.
    - Query Wacom devices automatically.

v1.0
    Released: 2012-07-13

    This is the first release with a version number. It contains a couple fixes
    and improvements compared to previous (before 2012-07-13) versions of these
    scripts.

    - Accept other names for the rotation.
    - Disable the trackpad as well.
    - Start and stop the virtual keyboard.
    - Try to go back automatically, if a rotation is already set.
    - Use ``--rotation`` instead of ``-o``. This will only rotate the internal
      screen and not any attached screens as well.

Way before 2012-07-13, those are significant changes in the history:

- Add desktop files.
- Also set Wacom hardware correctly.
- Determine resolution automatically.
- Disable trackpoint when switching.
- Dynamically find external display.
- Limit Wacom devices to internal screen.
- Set external monitor as primary.

.. vim: spell
