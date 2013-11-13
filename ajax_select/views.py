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

from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse


def ajax_lookup(request,channel):
    """ this view supplies results for both foreign keys and many to many fields """

    # it should come in as GET unless global $.ajaxSetup({type:"POST"}) has been set
    # in which case we'll support POST
    if request.method == "GET":
        # we could also insist on an ajax request
        if 'q' not in request.GET:
            return HttpResponse('')
        query = request.GET['q']
    else:
        if 'q' not in request.POST:
            return HttpResponse('') # suspicious
        query = request.POST['q']
    
    lookup_channel = get_lookup(channel)
    
    if query:
        instances = lookup_channel.get_query(query,request)
    else:
        instances = []

    results = []
    for item in instances:
        itemf = lookup_channel.format_item(item)
        itemf = itemf.replace("\n","").replace("|","&brvbar;")
        resultf = lookup_channel.format_result(item)
        resultf = resultf.replace("\n","").replace("|","&brvbar;")
        results.append( "|".join((unicode(item.pk),itemf,resultf)) )
    return HttpResponse("\n".join(results))


def add_popup(request,app_label,model):
    """ present an admin site add view, hijacking the result if its the dismissAddAnotherPopup js and returning didAddPopup """ 
    themodel = models.get_model(app_label, model) 
    admin = site._registry[themodel]

    admin.admin_site.root_path = "/ajax_select/" # warning: your URL should be configured here. 
    # as in your root urls.py includes :
    #    (r'^ajax_select/', include('ajax_select.urls')),
    # I should be able to auto-figure this out but ...

    response = admin.add_view(request,request.path)
    if request.method == 'POST':
        if response.content.startswith('<script type="text/javascript">opener.dismissAddAnotherPopup'):
            return HttpResponse( response.content.replace('dismissAddAnotherPopup','didAddPopup' ) )
    return response

