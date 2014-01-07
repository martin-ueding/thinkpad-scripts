.. Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

############
Environments
############

The environment differs between the normal user and root. This might be the
cause for some bugs.

Difference user and root
========================

See the following diff between the user and root environment, made with ``$
env`` and ``# env``:

.. literalinclude:: diff-user-root.diff
    :language: diff

Difference user and ``su``
==========================

If you look the differences to an environment made with ``su``, there is less
changed, but still a lot missing. I made the following with (where ``mu`` is my
user account):

.. code-block:: console

    # su -c env mu

This is the output:

.. literalinclude:: diff-user-su.diff
    :language: diff

Shared properties
=================

In both cases, the variable ``DBUS_SESSION_BUS_ADDRESS`` is missing. This might
be cause for bugs like `#36
<https://github.com/martin-ueding/think-rotate/issues/36>`_.

Difference user and ``su -c env``
=================================

Even if you use ``env`` to recreate the user's environment, it does not change
anything, apparently:

.. code-block:: console

    su -c 'env env' mu

.. literalinclude:: diff-user-su_env.diff
    :language: diff

.. vim: spell tw=79
