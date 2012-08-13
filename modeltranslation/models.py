# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# -*- coding: utf-8 -*-
import sys

from django.conf import settings
from django.db import models

from modeltranslation.settings import TRANSLATION_REGISTRY
from modeltranslation.translator import translator

# Every model registered with the modeltranslation.translator.translator is
# patched to contain additional localized versions for every field specified
# in the model's translation options.

# Import the project's global "translation.py" which registers model classes
# and their translation options with the translator object.
try:
    __import__(TRANSLATION_REGISTRY, {}, {}, [''])
except ImportError:
    sys.stderr.write("modeltranslation: Can't import module '%s'.\n"
                     "(If the module exists, it's causing an ImportError "
                     "somehow.)\n" % TRANSLATION_REGISTRY)
    # For some reason ImportErrors raised in translation.py or in modules that
    # are included from there become swallowed. Work around this problem by
    # printing the traceback explicitly.
    import traceback
    traceback.print_exc()

# After importing all translation modules, all translation classes are
# registered with the translator.
if settings.DEBUG:
    try:
        if sys.argv[1] in ('runserver', 'runserver_plus'):
            translated_model_names = ', '.join(
                t.__name__ for t in translator._registry.keys())
            print('modeltranslation: Registered %d models for '
                    'translation (%s).' % (len(translator._registry),
                                            translated_model_names))
    except IndexError:
        pass
