##############
Unity Launcher
##############

The Unity Launcher on the left side is only shown if you excert pressure with the mouse. That means that you do not only have to put the mouse to the left edge of the screen, but push it beyond that edge. This is not possible to do with touchscreen or the pen, so you need to show the launcher by default.

cpbl_ contributed this ``postrotate`` hook:

.. code-block:: bash

    #!/bin/bash
    if [[ "$1" = "normal" ]]
    then
        echo "Found normal"
        dconf write /org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode 1
    else
        echo "Found tablet mode"
        dconf write /org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode 0
    fi

This hook will work with version 3.1 or newer. In `Issue #35
<https://github.com/martin-ueding/thinkpad-scripts/issues/35>`_, cpbl_ pointed
out the the rotation hooks are not passed an argument with the target rotation.

.. _cpbl: https://github.com/cpbl
