# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import locale
import os
import sys

from babel import Locale
from babel import dates, numbers, support, Locale
from babel.support import Translations
from flufl.i18n import registry
from flufl.i18n import PackageStrategy

try:
    from pytz.gae import pytz
except ImportError:
    from pytz import timezone, UTC
else:
    timezone = pytz.timezone
    UTC = pytz.UTC
    
from tps.__meta__ import name as domain_name

class BabelPackageStrategy(PackageStrategy):
    '''Babel backend for flufl.i18n with all additions that it offers'''
    
    DEFAULT_LOCALE = 'en_US'
    
    def __call__(self, language_code=None):
        languages = (None if language_code is None else [language_code])
        return Translations.load(self._messages_dir, languages, self.name)
    
    def get_default_locale(self):
        defloc = Locale.default('LC_MESSAGES')
        if not defloc:
            # probably duplicates the above method
            loc, encoding = locale.getdefaultlocale()
            if loc:
                defloc = Locale.parse(loc)
                if not defloc:
                    defloc = Locale.parse(BabelPackageStrategy.DEFAULT_LOCALE)
        return defloc
        
    def list_locales(self):
        if not os.path.isdir(self._messages_dir):
            return []
        result = []
        for folder in os.listdir(self._messages_dir):
            locale_dir = os.path.join(self._messages_dir, folder, 'LC_MESSAGES')
            if not os.path.isdir(locale_dir):
                continue
            if filter(lambda x: x.endswith('.mo'), os.listdir(locale_dir)):
                result.append(Locale.parse(folder))
        if not result:
            result.append(self.get_default_locale())
        return result

def install(application, names=None):
    '''Install Application._() system wide  in python builtins 
    namespace for default locale
    '''
    import builtins
    builtins.__dict__['_'] = application._
    if hasattr(names, "__contains__"):
        catalog = application.get(application.default)
        if "gettext" in names:
            builtins.__dict__['gettext'] = builtins.__dict__['_']
        if "ngettext" in names:
            builtins.__dict__['ngettext'] = catalog.ngettext
        if "lgettext" in names:
            builtins.__dict__['lgettext'] = catalog.lgettext
        if "lngettext" in names:
            builtins.__dict__['lngettext'] = catalog.lngettext

strategy = BabelPackageStrategy(domain_name, sys.modules[__name__])
application = registry.register(strategy)
application.default = str(strategy.get_default_locale())
