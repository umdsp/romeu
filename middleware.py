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

"this is a minimal locale selecting middleware that will look at the current session"

from django.utils.cache import patch_vary_headers
from django.utils import translation

class MinimalLocaleMiddleware(object):
    """
    This is a minimal version of the LocaleMiddleware from Django.
    It only supports setting the current language from sessions.
    This allows the main site to be in one language while the site
    administrators can switch the language, so they don't experience
    problems while editing original database content when this is not
    in the main site's language.
    """

    def process_request(self, request):
        language = get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response


def get_language_from_request(request):
    from django.conf import settings
    supported = dict(settings.LANGUAGES)

    if hasattr(request, 'session'):
        lang_code = request.session.get('django_language', None)
        if lang_code in supported and lang_code is not None:
            return lang_code
    return settings.LANGUAGE_CODE

