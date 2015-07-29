.. Copyright © 2012-2015 Martin Ueding <dev@martin-ueding.de>

#########
Changelog
#########

v4.4.1
    Released: 2015-07-29 08:23:28 +0200

    - Check list of PulseAudio devices to get sound settings right.
      (Contributed by Jannis Stoppe, thank you!)
    - Update regular expressions for ``xinput``. We have been using the ones
      for ``xsetwacom`` until now. Since we have switched to ``xinput`` in
      version 4.2.3, this should fix bugs since then.

v4.4.0
    Released: 2015-05-09 10:51:34 +0200

    - Add a workaround for an XRandr bug that I have on my machine.

v4.3.0
    Released: 2015-03-25 14:53:31 +0100

    - Fix a bug that was introduced in 69ef6ea. This leads to premature exit
      and dump of a stacktrace. The screens got rotated, but the TrackPoint
      would not be disabled.

    - Add an option to disable the internal screen on docking (GH-103).

v4.2.6
    Released: 2015-03-15 22:53:34 +0100

    - Update documentation for openSUSE package

v4.2.5
    Released: 2015-03-15 19:28:52 +0100

    - Remove icons from docking desktop files to get it to build on openSUSE
      Build Service

v4.2.4
    Released: 2015-02-19 18:49:21 +0100

    - Write transformation matrices to debug output.
    - Small fixes in documentation: Remove dead navigation entry and use
      correct syntax highlighting for config snippet.

v4.2.3
    Released: 2015-02-08

    - Add documentation about Fedora package
    - Add hardware specific documentation
    - Replace ``xsetwacom`` with ``xinput`` in all cases and use transformation
      matrix (GH-91)
    - Add a nice error message when a screen could not be found
    - Remove ``termcolor`` as a dependency
    - Always have at least one screen enabled
    - Be more careful with ``gsettings``, check whether the schema exists
      before writing to it

v4.2.2
    Released: 2015-01-24

    - Remove dependency on ``termcolor`` since that is not packaged for Python
      3 in Ubuntu or Fedora. It was not needed heavily anyway, so I just got
      rid of it.

    - Add manual page for ``thinkpad-config``
    - Add manual page for ``thinkpad-trackpoint``
    - Add manual page for ``thinkpad-scripts-config-migration``
    - Add a common epilogue for all manual pages

    - Remove mailing list from README
    - Replace hard coded strings with configuration options (GH-91)
    - Toggle touch screen with ``xinput`` only (GH-91)
    - Give a real error when rotation cannot be determined (GH-92)

v4.2.1
    Released: 2015-01-20

    - Fix errors in ``.desktop`` files
    - Use built-in mocking for unit tests

v4.2.0
    Released: 2015-01-15

    - Log error when unsupported key is given to rotate hook.
    - Fix ``full-install`` target in makefile.
    - Add ``test`` target to makefile.
    - Add support for multiple external monitors. See the manual page of
      ``thinkpad-dock`` for the details of the configuration options.

v4.1.5
    Released: 2014-10-26

    - Make selection of ethernet connection which is restarted predictable.
    - Remove call to ``nmcli con down`` in the restarting of the network
      connection. This makes it compatible with nmcli 0.9.10. That closes
      `GH-81 <https://github.com/martin-ueding/thinkpad-scripts/issues/81>`_,
      fixes `GH-74
      <https://github.com/martin-ueding/thinkpad-scripts/issues/74>`_ and closes
      `GH-75 <https://github.com/martin-ueding/thinkpad-scripts/issues/75>`_,

v4.1.4
    Released: 2014-10-25

    - Fix `GH-79
      <https://github.com/martin-ueding/thinkpad-scripts/issues/79>`_ by
      catching the exceptions and logging warnings. Missing TrackPoint and
      TouchPad do not cause the program to abort now.

v4.1.3
    Released: 2014-10-15

    - Fix breakage of the rotation script when the subpixel order cannot be
      changed for some reason. An error is logged then.

v4.1.2
    Released: 2014-10-05

    - Fix hiding of Unity launcher (GitHub #72)
    - Warn about ``make install`` (GitHub #76)

v4.1.1
    Released: 2014-09-07

    - Add ``network.connection_name`` configuration option.
    - Add support for ``nmcli`` v0.9.10 command line interface.

v4.1
    Released: 2014-07-12

    - Add ``tablet-normal`` rotation. That will not rotate the screen but
      deactivate the trackpoint.
    - Accept all rotation names again.

v4.0.8:
    Released: 2014-06-14

    - Fix some errors in the manual pages

v4.0.7
    Released: 2014-06-14

    - Make triggering on hardware rotation slightly more robust against changes
      in the event that ``acpid`` gives.

v4.0.6
    Released: 2014-06-02

    - Toggle Wacom Touch property with ``xsetwacom`` as well as using
      ``xinput``.

v4.0.5
    Released: 2014-05-29

    - Automatic determination of ethernet network connection
    - ``make install`` does not restart any services. ``make full-install``
      does that now.

v4.0.4
    Released: 2014-05-29

    - State Python termcolor dependency in the documentation
    - Stop failing if ``gsettings`` is not installed
    - Add subpixel rotation in Xfce
    - Warn about missing screen when docking

v4.0.3
    Released: 2014-05-28

    - Replace unicode arrow because of Launchpad errors.

v4.0.2
    Released: 2014-05-28

    - Assert Python 3 everywhere. I suspect that the Launchpad Build System
      uses Python 2 for some reason. That causes some unicode errors.

v4.0.1
    Released: 2014-05-28

    - Fill in dependencies in the “Getting Started“ guide.
    - Explicitly state the encoding in ``getversion.py``.

v4.0
    Released: 2014-05-27

    - Complete rewrite in Python 3.
    - INI style config. Run ``thinkpad-scripts-config-migrate`` to help you
      migrate your config.
    - Remove the transitional scripts. If you have anything that still depends
      on having scripts starting with ``think-``, **this will break!**
    - v3.0.1 introduced more relative positions by putting the ``-of`` into
      your configuration variable. Old configurations that still had ``left``
      or ``right`` still worked, since the script appended the ``-of`` for you.
      Those couple lines were removed, so **add a ``-of`` to your config, if
      you do not have already!**

    - You can change the regular expression that matches the Wacom devices now
      in the config. That is ``touch.regex`` in the config.

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

.. vim: spell tw=79
