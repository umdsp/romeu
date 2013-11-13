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
from warnings import warn

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


if hasattr(settings, 'MODELTRANSLATION_TRANSLATION_REGISTRY'):
    TRANSLATION_REGISTRY =\
    getattr(settings, 'MODELTRANSLATION_TRANSLATION_REGISTRY', None)
elif hasattr(settings, 'TRANSLATION_REGISTRY'):
    warn('The setting TRANSLATION_REGISTRY is deprecated, use '
         'MODELTRANSLATION_TRANSLATION_REGISTRY instead.', DeprecationWarning)
    TRANSLATION_REGISTRY = getattr(settings, 'TRANSLATION_REGISTRY', None)
else:
    raise ImproperlyConfigured("You haven't set the "
                               "MODELTRANSLATION_TRANSLATION_REGISTRY "
                               "setting yet.")

AVAILABLE_LANGUAGES = [l[0] for l in settings.LANGUAGES]
DEFAULT_LANGUAGE = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', None)
if DEFAULT_LANGUAGE and DEFAULT_LANGUAGE not in AVAILABLE_LANGUAGES:
    raise ImproperlyConfigured('MODELTRANSLATION_DEFAULT_LANGUAGE not '
                               'in LANGUAGES setting.')
elif not DEFAULT_LANGUAGE:
    DEFAULT_LANGUAGE = AVAILABLE_LANGUAGES[0]

# FIXME: We can't seem to override this particular setting in tests.py
CUSTOM_FIELDS =\
getattr(settings, 'MODELTRANSLATION_CUSTOM_FIELDS', ())
try:
    if sys.argv[1] == 'test':
        CUSTOM_FIELDS =\
        getattr(settings, 'MODELTRANSLATION_CUSTOM_FIELDS',
                ('BooleanField',))
except IndexError:
    pass
