.. Copyright © 2013-2014 Martin Ueding <martin-ueding.de>

Script Drawer For KDE Plasma Panel
==================================

Since there are more scripts than buttons, I added a drawer with all the
programs to my KDE Panel. It looks like this:

.. figure:: kicker.png

    The script collection in a folder right next to the system clock.

.. figure:: drawer.png

    KDE Plasma Panel drawer with all ``thinkpad-`` scripts.

Add a new “folder view” to your panel and set the following options:

(1) Go into the first tab and (2) set the folder to
``/usr/share/applications``.

.. figure:: settings1.png

(3) Then go to the “Filter” tab and (4) set
``thinkpad-*.desktop`` as the filter. That will only list scripts from this
collection.

.. figure:: settings2.png
