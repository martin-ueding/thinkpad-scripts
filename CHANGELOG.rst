.. Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

#########
Changelog
#########

v3.3
    - Rename project to “thinkpad-scripts”
    - Add subpixel anti-alias order change on rotation for Gnome

v3.2
    - Update copyright years in the documentation.
    - Add a guard that prevents multiple execution of ``think-dock`` and
      ``think-rotate``. For some reason, the ``udev`` hooks call the script
      twice, resulting in race conditions.

v3.1.2
    - Fix finding of external display. I tried to improve the syntax, but let
      the script fail whenever the number needed to be incremented.

v3.1.1
    - Clean all ``*.pyc`` files in makefile. This was causing errors with
      prisine tars and Debian packaging before.
    - Add changelog to documentation

v3.1
    - Pass target orientation to postrotate hook
    - Pass version number to Sphinx automatically from the changelog

v3.0.2
    - Manual pages with Sphinx

v3.0.1
    - Allow more relative positions by putting the ``-of`` into the value of
      the ``relative_position`` variable

v3.0
    - Settings of the keycodes is now done via a ``.hwdb`` file for ``udev``.
      This requires ``udev`` to be of version 196 or greater. Therefore, it is
      marked as a major release, since it breaks Ubuntu 13.04 and earlier.

v2.11
    - Add some guides: “Additional Keys” and “KDE Script Drawer”
    - Fix recursive make, pass ``-j`` down to child processes

v2.10.2
    - Actually return from function.

v2.10.1
    - Do not fail if ``qdbus`` does not work (like on vanilla Kubuntu 13.10)

v2.10
    - Print missing programs
    - Do not fail if ``qdbus`` is missing

v2.9
    - **Added**: ACPI hook to call ``think-rotate`` (Jim Turner)
    - **Added**: Support for systemd network inferface names (Jim Turner)
    - **Removed**: ``think-resume`` (Jim Turner)
    - Use syslog in ``think-dock``
    - Update documentation
    - State all dependencies (Debian package names)
    - Change indentation to four spaces instead of a single tab

v2.8.1
    - More logging to syslog
    - Disable ``kdialog`` for ACPI hooks since that does now work well

v2.8
    - Translate to German

v2.7.1
    - Close KDialog progress bar when the script fails (via ``trap``)

v2.7
    - **Added**: Hooks
    - **Added**: ``on|off`` for the ``think-touchpad`` script

v2.6
    - Support for ``kdialog`` status.

v2.5.2
    - Update the ACPI hooks to find other docks as well

v2.5.1
    - Find other docks as well

v2.5
    - Get microphone mute button to work

v2.4.1
    - Actually install makefiles
    - Implement required actions in ``init.d`` script to that Debian lintian
      does not complain

v2.4
    - Fix bezel keyboard codes, so that they are usable. (Jim Turner)
    - Add script to toggle touch screen. (Jim Turner)
    - Organize code in subdirectories, using recursive make.

v2.3.1
    - Map Wacom devices to the output when rotating in any case. Thanks to Jim
      Turner!

v2.3
    - Add support for other virtual keyboards. Thanks to Jim Turner!
    - Use shorter redirection (``&>`` instead of ``2>&!``).

v2.2.1
    - Fix spelling typo in ``relative_position``. Thanks to Jim Turner!

v2.2
    - Background most tasks so that they run in parallel. This should speed up
      docking.

v2.1
    - Only set Wacom screen devices. That way, any attached Wacom graphics
      tablet is not affected by the docking.

v2.0
    - Use the kernel to determine what the docking status is.
    - Add ``udev`` rules to perform the docking action.

v1.5
    - Desktop files for think-dock.

v1.4.3
    - Disable the wireless connection on docking.

v1.4.2
    - Fix commands in ``.desktop`` files.

v1.4.1
    - Install ``.desktop`` files.

v1.4
    - Query the state of the whole system automatically and determine the right
      action. You can still specify ``on`` or ``off``, if you want to.

v1.3
    - Optional config file for ``think-dock``.

v1.2.2
    - Fix flip direction.

v1.2.1
    - Disable wireless only when eth0 connected.
    - Document options.

v1.2
    - Change display brightness on docking.

v1.1
    - Check whether programs are there before using them.
    - Create directories on ``make install``.
    - Disable wifi when going onto the docking station.
    - Enable sound on docking.
    - Lower the volume after docking.
    - Query Wacom devices automatically.

v1.0
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
