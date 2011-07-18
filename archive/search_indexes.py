from haystack.indexes import *
from haystack import site
from archive.models import Creator, Production, Location, WorkRecord

class CreatorIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='creator_ascii_name')
    born = DateField(model_attr='birth_date', null=True)
    died = DateField(model_attr='death_date', null=True)
    gender = CharField(model_attr='gender', null=True)
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Creator.objects.filter(published=True)
        
class ProductionIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='ascii_title')
    
    def index_queryset(self):
        return Production.objects.filter(published=True)
        
class LocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='title_ascii')
    
    def index_queryset(self):
        return Location.objects.filter(published=True)
        
class WorkRecordIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='ascii_title')
    
    def index_request(self):
        return WorkRecord.objects.filter(published=True)
        
site.register(Creator, CreatorIndex)
site.register(Production, ProductionIndex)
site.register(Location, LocationIndex)
site.register(WorkRecord, WorkRecordIndex)