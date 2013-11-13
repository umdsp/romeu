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

#!/usr/bin/env python2.7
import sys
import os
import django.core.handlers.wsgi
sys.path.append('/ctda/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 
class ForcePostHandler(django.core.handlers.wsgi.WSGIHandler):
    """Workaround for: 
http://lists.unbit.it/pipermail/uwsgi/2011-February/001395.html
    """
    def get_response(self, request):
        request.POST # force reading of POST data
        return super(ForcePostHandler, self).get_response(request)

application = ForcePostHandler()
