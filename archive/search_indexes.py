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

from haystack.indexes import *
from haystack import site
from archive.models import Creator, Production, Location, WorkRecord, DigitalObject
from taggit.models import Tag, TaggedItem

class CreatorIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='creator_ascii_name')
    born = DateField(model_attr='birth_date', null=True)
    died = DateField(model_attr='death_date', null=True)
    gender = CharField(model_attr='gender', null=True)
    tag_name = MultiValueField()
        
    def prepare_creator_tag(self, obj):
        return [tag for tag in obj.tags.names()]
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Creator.objects.filter(published=True)
        
class ProductionIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='ascii_title')
    tag_name = MultiValueField()

    def prepare_production_tag(self, obj):
        return [tag for tag in obj.tags.names()]
    
    def index_queryset(self):
        return Production.objects.filter(published=True)
        
class LocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='title_ascii')
    tag_name = MultiValueField()

    def prepare_location_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_queryset(self):
        return Location.objects.filter(published=True)
        
class WorkRecordIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='ascii_title')
    tag_name = MultiValueField()

    def prepare_workrecord_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_request(self):
        return WorkRecord.objects.filter(published=True)

class DigitalObjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='ascii_title')
    tag_name = MultiValueField()

    def prepare_digitalobject_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_request(self):
        return DigitalObject.objects.filter(published=True)
        
class TagIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    tag_name = CharField(model_attr='tag__name', faceted=True)
#    digital_object_title = CharField(model_attr='digitalobject__ascii_title')
#    workrecord_object_title = CharField(model_attr='workrecord__ascii_title')
#    location_object_title = CharField(model_attr='location__title_ascii')
#    creator_object_title = CharField(model_attr='creator__creator_ascii_name')
#    production_object_title = CharField(model_attr='production__ascii_title')
#    def get_model(self):
#        return Tag

    def index_request(self):
        return TaggedItem.objects.all()


site.register(Creator, CreatorIndex)
site.register(Production, ProductionIndex)
site.register(Location, LocationIndex)
site.register(WorkRecord, WorkRecordIndex)
site.register(DigitalObject, DigitalObjectIndex)
site.register(TaggedItem, TagIndex)