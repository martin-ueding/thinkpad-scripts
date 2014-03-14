.. Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

###########
Why Python?
###########

:Author: Martin Ueding <dev@martin-ueding.de>

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

.. vim: spell tw=79
