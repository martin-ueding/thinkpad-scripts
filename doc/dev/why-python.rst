.. Copyright © 2014 Martin Ueding <mu@martin-ueding.de>

###########
Why Python?
###########

:Author: Martin Ueding <mu@martin-ueding.de>

Advantages
==========

Why do I want to switch to Python 3 over Bash?

INI config format
    The Bash implementation just sourced its config file. So you could write a
    little shell script that assigned a couple variables and you were done with
    it.

    Python has the ``configparser`` module which enables using INI style config
    files. There is a default configuration which can be overwritten. This
    offers sectioning in the config, which makes sense with the current amount
    of options.

Language offers module
    Bash has no notion of modules. It just has scripts that could be sourced.
    This was done with the ``lib`` folder, but it has felt like a hack from the
    very beginning. When I documented those functions, I realized that it was
    hard to do that since Bash functions do not have named parameter like real
    programming languages. The biggest issue are the missing return values.

    Since modules are easy with Python, I can split the long scripts into
    multiple modules.

Scoping
    The Bash implementation used a lot of global variables. Like the
    ``$external`` that appeared magically when you would call the
    ``find-external`` function. I believe in the “explicit is better than
    implicit” statement of the Python Zen, so this bugged me.

    With the scopes in the functions, I can create lot of simple, small
    functions that can be tested and reused better.

XML support
    With the XML config file for fontconfig coming up, I wanted to have a
    language that can work with XML files natively. Using ``sed`` on a XML file
    just seems wrong. Well, XML as configuration seems wrong as well.

Direct GUI
    So far, the GUI has been made with ``kdialog`` which received messages via
    ``qdbus``. This works. But with Python, a binding like PyQt can be used to
    create a real GUI.

Better string processing
    There are lines like the following in the 3.x codebase:

    .. code-block:: bash

        external=$(xrandr | grep -Eo '(\S+) connected' | grep -Eo '^(\S+)' | grep -v "$internal") 

    I think this can be done much nicer in Python.

    .. code-block:: python

        def get_external(internal):
            lines = tps.check_output(['xrandr'], logger).decode().split('\n')
            for line in lines:
                if not line.startswith(internal):
                    matcher = re.search(r'^(\S+) connected', line)
                    if matcher:
                        return matcher.group(1)

    Yes, it is way more code. But I find it easier to read and more self
    explanatory.

Possibility of a daemon
    It would be possible to have this running as a daemon which gets messages
    via D-Bus. The hooks that get called with hardware events are run as root
    and without the ``DISPLAY`` variable set. The 3.x code uses ``su`` to run
    the code in the context of the user. With such a daemon, it would be
    possible to avoid that and invoke the action.

    This has the disadvantage of an always running daemon, which is not really
    needed.

Better documentation
    Docstrings and Sphinx allows one to document the hell out of code. And it
    is quite fun. With that, it is really easy to document the various parts of
    the codebase in a standard way.

Disadvantages
=============

I do see some disadvantages. They are not big issues, I think.

Requires Python knowledge
    It will require the developers to know Python. Or they will have to be
    willing to learn it for this project. I do not consider Python an uncommon
    language, not more uncommon than Bash, on Linux. Look at various Ubuntu
    scripts, they are written in Python.

    Bash is pretty hard to get right with all its pitfalls. So Python might be
    an easier choice to get people to contribute.

Adds more dependencies
    Bash is included in virtually every distribution. Python should be as well,
    but there might be somebody without Python on his system.

.. vim: spell tw=79
