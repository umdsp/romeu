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

from haystack import indexes
#from haystack import site
from archive.models import Creator, Production, Location, WorkRecord, DigitalObject, Festival
from taggit.models import Tag, TaggedItem

class CreatorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='creator_ascii_name')
    born = indexes.DateField(model_attr='birth_date', null=True)
    died = indexes.DateField(model_attr='death_date', null=True)
    gender = indexes.CharField(model_attr='gender', null=True)
    tag_name = indexes.MultiValueField()
    
    def get_model(self):
        return Creator    
    
    def prepare_creator_tag(self, obj):
        return [tag for tag in obj.tags.names()]
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Creator.objects.filter(published=True)
        
class ProductionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='ascii_title')
    tag_name = indexes.MultiValueField()
    
    def get_model(self):
        return Production 

    def prepare_production_tag(self, obj):
        return [tag for tag in obj.tags.names()]
    
    def index_queryset(self):
        return Production.objects.filter(published=True)
        
class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='title_ascii')
    tag_name = indexes.MultiValueField()

    def get_model(self):
        return Location 

    def prepare_location_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_queryset(self):
        return Location.objects.filter(published=True)
        
class WorkRecordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='ascii_title')
    tag_name = indexes.MultiValueField()


    def get_model(self):
        return WorkRecord

    def prepare_workrecord_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_request(self):
        return WorkRecord.objects.filter(published=True)

class DigitalObjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='ascii_title')
    tag_name = indexes.MultiValueField()

    def get_model(self):
        return DigitalObject

    def prepare_digitalobject_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_request(self):
        return DigitalObject.objects.filter(published=True)

class FestivalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='title')
    tag_name = indexes.MultiValueField()

    def get_model(self):
        return Festival
    
    def prepare_festival_tag(self, obj):
        return [tag for tag in obj.tags.names()]

    def index_request(self):
        return Festival.objects.filter()

    
class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    tag_name = indexes.CharField(model_attr='tag__name', faceted=True)

    def get_model(self):
        return TaggedItem 

    def index_request(self):
        return TaggedItem.objects.all()

"""
site.register(Creator, CreatorIndex)
site.register(Production, ProductionIndex)
site.register(Location, LocationIndex)
site.register(WorkRecord, WorkRecordIndex)
site.register(DigitalObject, DigitalObjectIndex)
site.register(Festival, FestivalIndex)
site.register(TaggedItem, TagIndex)
"""
