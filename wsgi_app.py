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
