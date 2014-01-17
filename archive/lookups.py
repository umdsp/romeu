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

from archive.models import (Creator, Location, Production, WorkRecord, Role,
                            Country, DigitalObject, Festival,
                            FestivalOccurrence, Collection, City, Award)
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

class CreatorLookup(ArchiveLookup):
    model = Creator
    def get_query(self,request,term):
        return Creator.objects.filter(Q(creator_ascii_name__icontains=term) |
                                      Q(creator_name__icontains=term) |
                                      Q(name_variants__icontains=term) |
                                      Q(creator_display_name__icontains=term) |
                                      Q(creator_display_ascii_name__icontains=term))
    
class TheaterCompanyLookup(ArchiveLookup):
    model = Creator
    def get_query(self,request,term):
        return Creator.objects.filter(org_name__icontains=term)

    
class LocationLookup(ArchiveLookup):
    model = Location
    def get_query(self,request,term):
        return Location.objects.filter(Q(title_ascii__icontains=term) |
                                       Q(title__icontains=term) |
                                       Q(title_variants__icontains=term))
        
        
class ProductionLookup(ArchiveLookup):
    model = Production
    def get_query(self,request,term):
        return Production.objects.filter(Q(ascii_title__icontains=term) |
                                         Q(title__icontains=term) |
                                         Q(title_variants__icontains=term))
        
class WorkRecordLookup(ArchiveLookup):
    model = WorkRecord
    def get_query(self,request,term):
        
        return WorkRecord.objects.filter(Q(ascii_title__icontains=term) |
                                         Q(title__icontains=term) |
                                         Q(title_variants__icontains=term))
        
class RoleLookup(ArchiveLookup):
    model = Role
    def get_query(self,request,term):
        work_record_list = request.GET.get('source_text', None)
        if work_record_list:
            return Role.objects.filter(source_text__id__in=work_record_list.split(","))
        else:
            return Role.objects.filter(Q(source_text__title__icontains=term) |
                                       Q(source_text__ascii_title__icontains=term) |
                                       Q(source_text__title_variants__icontains=term) |
                                       Q(title__icontains=term))
        
class CountryLookup(ArchiveLookup):
    model = Country
    def get_query(self,request,term):
        return Country.objects.filter(Q(name__icontains=term) |
                                      Q(demonym__icontains=term))
        
class DigitalObjectLookup(ArchiveLookup):
    model = DigitalObject
    def get_query(self,request,term):
        return DigitalObject.objects.filter(Q(object_id__icontains=term) |
                                            Q(digital_id__icontains=term) |
                                            Q(identifier__icontains=term) |
                                            Q(title__icontains=term) |
                                            Q(title_variants__icontains=term) |
                                            Q(summary__icontains=term))

class FestivalLookup(ArchiveLookup):
    model = Festival
    def get_query(self,request,term):
        return Festival.objects.filter(title__icontains=term)

class FestivalOccurrenceLookup(ArchiveLookup):
    model = FestivalOccurrence
    def get_query(self,request,term):
        return FestivalOccurrence.objects.filter(Q(title__icontains=term) |
                                                 Q(title_variants__icontains=term) |
                                                 Q(festival_series__title__icontains=term))

class CollectionLookup(ArchiveLookup):
    model = Collection
    def get_query(self,request,term):
        return Collection.objects.filter(Q(collection_id__icontains=term) |
                                         Q(title__icontains=term)).order_by('title')

class CityLookup(ArchiveLookup):
    model = City
    def get_query(self,request,term):
        return City.objects.filter(name__icontains=term)

class AwardLookup(ArchiveLookup):
    model = Award
    def get_query(self,request,term):
        return Award.objects.filter(title__icontains=term)

registry.register(CreatorLookup)
registry.register(TheaterCompanyLookup)
registry.register(LocationLookup)
registry.register(ProductionLookup)
registry.register(WorkRecordLookup)
registry.register(RoleLookup)
registry.register(CountryLookup)
registry.register(DigitalObjectLookup)
registry.register(FestivalLookup)
registry.register(FestivalOccurrenceLookup)
registry.register(CollectionLookup)
registry.register(CityLookup)
registry.register(AwardLookup)
