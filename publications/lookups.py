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

from publications.models.publication import Publication
from django.db.models import Q

from selectable.base import LookupBase
from selectable.registry import registry

class ArchiveLookup(LookupBase):
    filters = {}
    
    def get_queryset(self):
        qs = self.model._default_manager.get_query_set()
        if self.filters:
            qs = qs.filter(**self.filters)
        return qs
        
    def get_item_id(self, item):
        return item.pk
    
    def get_item(self, value):
        item = None
        if value:
            try:
                item = self.get_queryset().filter(pk=value)[0]
            except IndexError:
                pass
        return item
        
    def get_item_value(self, item):
        return item.__unicode__()

class PublicationLookup(ArchiveLookup):
    model = Publication
    def get_query(self,request,term):
        return Publication.objects.filter(title__icontains=term)

registry.register(PublicationLookup)