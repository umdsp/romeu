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


from ajax_select.fields import autoselect_fields_check_can_add
from django.contrib import admin

class AjaxSelectAdmin(admin.ModelAdmin):
    
    """ in order to get + popup functions subclass this or do the same hook inside of your get_form """
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(AjaxSelectAdmin,self).get_form(request,obj,**kwargs)
        
        autoselect_fields_check_can_add(form,self.model,request.user)
        return form

