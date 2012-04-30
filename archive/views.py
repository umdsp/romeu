from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.xheaders import populate_xheaders
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

from settings import MEDIA_URL, STATIC_URL

from sorl.thumbnail import default

from archive.models import Creator, Location, Production, WorkRecord, DigitalObject, DigitalFile, \
                           Festival, FestivalOccurrence, DirectingMember, CastMember, DesignMember, \
                           TechMember, ProductionMember, DocumentationMember, AdvisoryMember, \
                           TranslatingFlatPage, DigitalObjectType, HomePageInfo, \
                           PhysicalObjectType, Collection, Repository

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

from random import randrange

# For flatpages
DEFAULT_TEMPLATE = 'flatpages/default.html'

class CreatorsListView(ListView):
    queryset = Creator.objects.filter(published=True).select_related().order_by('creator_name')
    context_object_name = "creators_list"
    template_name = "archive/creators_list.html"
    paginate_by = 120
    
    def get_context_data(self, **kwargs):
        context = super(CreatorsListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_creator__isnull=False, files__isnull=False, digi_object_format=imagetype)
        length = len(alldos) - 1
        count = 0
        dos = []
        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                dos.append(alldos[num])
                count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.first_file().filepath
                item['title'] = obj.title
                item['creator_name'] = obj.related_creator.all()[0].display_name
                item['creator_id'] = obj.related_creator.all()[0].pk
                item['pk'] = obj.pk
                objects_list.append(item)
                
        context['digital_objects'] = objects_list
        return context
         
         
class CreatorsAlphaListView(CreatorsListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = Creator.objects.filter(published=True).filter(creator_name__iregex=r'^[0-9!@#$%^&*\(\)]').select_related().order_by('creator_name')
        else:
            qset = Creator.objects.filter(published=True).filter(creator_name__istartswith=self.kwargs['alpha']).select_related().order_by('creator_name')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(CreatorsAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context
         
                
class CreatorDetailView(DetailView):
    queryset = Creator.objects.filter(published=True).select_related()
    context_object_name = "creator"
    template_name = "archive/creator_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(CreatorDetailView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        alldos = DigitalObject.objects.filter(related_creator=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        if alldos:
            for obj in alldos:
                for file in obj.files.order_by('seq_id'):
                    item = {}
                    item['image'] = file.filepath
                    item['title'] = obj.title
                    item['pk'] = obj.pk
                    objects_list.append(item)
            context['digital_objects'] = objects_list
        videos = DigitalObject.objects.filter(related_creator=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
        if videos:
            video_list = []
            for vid in videos:
                item = {}
                if vid.poster_image:
                    item['poster'] = vid.poster_image
                item['hidef'] = vid.hi_def_video
                item['object_id'] = vid.object_number()
                item['title'] = vid.title
                item['pk'] = vid.pk
                video_list.append(item)
            context['videos'] = video_list
        if self.object.photo:
            photofile = self.object.photo.first_file()
            context['creatorphoto'] = photofile.filepath
        else:
            context['creatorphoto'] = False
        return context
        
        
class ProductionsListView(ListView):
    queryset = Production.objects.filter(published=True).select_related().order_by('title')
    context_object_name = "productions_list"
    template_name = "archive/productions_list.html"
    paginate_by = 120

    def get_context_data(self, **kwargs):
        context = super(ProductionsListView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_production__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].first_file():
                dos.append(alldos[num])
                count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.first_file().filepath
                item['title'] = obj.title
                item['production_title'] = obj.related_production.all()[0].title
                item['production_id'] = obj.related_production.all()[0].pk
                item['pk'] = obj.pk
                objects_list.append(item)
                
            context['digital_objects'] = objects_list
            return context
            
class ProductionsAlphaListView(ProductionsListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = Production.objects.filter(published=True).filter(title__iregex=r'^[0-9!@#$%^&*\(\)]').select_related().order_by('title')
        else:
            qset = Production.objects.filter(published=True).filter(title__istartswith=self.kwargs['alpha']).select_related().order_by('title')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(ProductionsAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context

class ProductionDetailView(DetailView):
    queryset = Production.objects.filter(published=True).select_related()
    context_object_name = "production"
    template_name = "archive/production_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionDetailView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        alldos = DigitalObject.objects.filter(related_production=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        if alldos:
            for obj in alldos:
                for file in obj.files.order_by('seq_id'):
                    item = {}
                    item['image'] = file.filepath
                    item['title'] = obj.title
                    item['pk'] = obj.pk
                    objects_list.append(item)
            context['digital_objects'] = objects_list
        videos = DigitalObject.objects.filter(related_production=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
        if videos:
            video_list = []
            for vid in videos:
                item = {}
                if vid.poster_image:
                    item['poster'] = vid.poster_image
                item['hidef'] = vid.hi_def_video
                item['object_id'] = vid.object_number()
                item['title'] = vid.title
                item['pk'] = vid.pk
                video_list.append(item)
            context['videos'] = video_list
        return context

class WorkRecordsListView(ListView):
    queryset = WorkRecord.objects.filter(published=True).select_related().order_by('title')
    context_object_name = "writtenworks_list"
    template_name = "archive/workrecords_list.html"
    paginate_by = 120
    
    def get_context_data(self, **kwargs):
        context = super(WorkRecordsListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_work__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].first_file():
                dos.append(alldos[num])
                count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.first_file().filepath
                item['title'] = obj.title
                item['work_title'] = obj.related_work.all()[0].title
                item['work_id'] = obj.related_work.all()[0].pk
                item['pk'] = obj.pk
                objects_list.append(item)
                
        context['digital_objects'] = objects_list
        return context

class WorkRecordsAlphaListView(WorkRecordsListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = WorkRecord.objects.filter(published=True).filter(title__iregex=r'^[0-9!@#$%^&*\(\)]').select_related().order_by('title')
        else:
            qset = WorkRecord.objects.filter(published=True).filter(title__istartswith=self.kwargs['alpha']).select_related().order_by('title')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(WorkRecordsAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context
        
class WorkRecordDetailView(DetailView):
    queryset = WorkRecord.objects.filter(published=True).select_related()
    context_object_name = "workrecord"
    template_name = "archive/workrecord_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkRecordDetailView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_work=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        if alldos:
            for obj in alldos:
                for file in obj.files.order_by('seq_id'):
                    item = {}
                    item['image'] = file.filepath
                    item['title'] = obj.title
                    item['pk'] = obj.pk
                    objects_list.append(item)
            context['digital_objects'] = objects_list
        return context
        
class VenuesListView(ListView):
    queryset = Location.objects.filter(published=True).filter(productions__isnull=False).select_related().distinct().order_by('title')
    context_object_name = "venues_list"
    template_name = "archive/venues_list.html"
    paginate_by = 120
    
    def get_context_data(self, **kwargs):
        context = super(VenuesListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_venue__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        if length > 0:
            while count < 3:
                num = randrange(0, length)
                if alldos[num].files.count() > 0 and alldos[num].first_file():
                    dos.append(alldos[num])
                    count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.first_file().filepath
                item['title'] = obj.title
                item['venue_title'] = obj.related_venue.all()[0].title
                item['loc_id'] = obj.related_venue.all()[0].pk
                item['pk'] = obj.pk
                objects_list.append(item)
                
        context['digital_objects'] = objects_list
        return context
        
class VenuesAlphaListView(VenuesListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = Location.objects.filter(published=True).filter(productions__isnull=False).filter(title__iregex=r'^[0-9!@#$%^&*\(\)]').distinct().select_related().order_by('title')
        else:
            qset = Location.objects.filter(published=True).filter(productions__isnull=False).filter(title__istartswith=self.kwargs['alpha']).distinct().select_related().order_by('title')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(VenuesAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context
        
class VenueDetailView(DetailView):
    queryset = Location.objects.filter(published=True).select_related()
    context_object_name = "venue"
    template_name = "archive/venue_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(related_venue=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        if alldos:
            for obj in alldos:
                for file in obj.files.order_by('seq_id'):
                    item = {}
                    item['image'] = file.filepath
                    item['title'] = obj.title
                    item['pk'] = obj.pk
                    objects_list.append(item)
            context['digital_objects'] = objects_list
        if self.object.photo:
            context['venuephoto'] = default.backend.get_thumbnail(self.object.photo.files.all()[0].filepath, "100x100", crop="center")
        return context

class DigitalObjectsListView(ListView):
    queryset = DigitalObject.objects.filter(Q(published=True), Q(digi_object_format__title="Image", files__isnull=False) | Q(digi_object_format__title="Video recording", ready_to_stream=True)).distinct().select_related().order_by('title')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 36

class DigitalObjectsVideosListView(ListView):
    vidtype = DigitalObjectType.objects.get(title="Video recording")
    queryset = DigitalObject.objects.filter(published=True, ready_to_stream=True, poster_image__isnull=False, digi_object_format=vidtype).distinct().select_related().order_by('-creation_date')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 36

class DigitalObjectsImagesListView(ListView):
    imagetype = DigitalObjectType.objects.get(title="Image")
    queryset = DigitalObject.objects.filter(published=True, files__isnull=False, digi_object_format=imagetype).distinct().select_related().order_by('-creation_date')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 36

# Function to generate the page with a list of PhysicalObjectTypes, for use with the TypeListView below.
def phys_types_list(request):
    pots = []
    for p in PhysicalObjectType.objects.order_by('title'):
        if p.has_viewable_objects():
            pots.append(p)
    context_dict = {'types': pots}
    return render_to_response('archive/digitalobjecttypes_list.html', context_dict, context_instance=RequestContext(request))

class DigitalObjectsTypeListView(ListView):
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 36

    def get_context_data(self, **kwargs):
        context = super(DigitalObjectsTypeListView, self).get_context_data(**kwargs)
        try:
            context['physobjtype'] = PhysicalObjectType.objects.get(slug__iexact=self.args[0]).title
        except:
            context['physobjtype'] = self.args[0]
        return context

    def get_queryset(self):
        type_name = get_object_or_404(PhysicalObjectType, slug__iexact=self.args[0])
        return DigitalObject.objects.filter(Q(published=True), Q(digi_object_format__title="Image", files__isnull=False) | Q(digi_object_format__title="Video recording", ready_to_stream=True)).filter(phys_object_type=type_name).distinct().select_related().order_by('title')

# Function to generate the page with a list of Collections, for use with the CollectionListView below.
def collections_list(request):
    collections = []
    for c in Collection.objects.order_by('repository__repository_id', 'collection_id'):
        if c.has_viewable_objects():
            collections.append(c)
    context_dict = {'collections': collections}
    return render_to_response('archive/digitalobjecttypes_list.html', context_dict, context_instance=RequestContext(request))

class DigitalObjectsCollectionListView(ListView):
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 36

    def get_context_data(self, **kwargs):
        context = super(DigitalObjectsCollectionListView, self).get_context_data(**kwargs)
        temp = self.args[0]
        temp_repo = Repository.objects.get(repository_id=temp[0:3])
        temp_coll_id = temp[3:]
        try:
            context['current_collection'] = Collection.objects.get(collection_id=temp_coll_id, repository=temp_repo)
        except:
            context['current_collection'] = self.args[0]
        return context

    def get_queryset(self):
        temp = self.args[0]
        temp_repo = Repository.objects.get(repository_id=temp[0:3])
        temp_coll_id = temp[3:]
        current_collection = get_object_or_404(Collection, collection_id=temp_coll_id, repository=temp_repo)
        return DigitalObject.objects.filter(Q(published=True), Q(digi_object_format__title="Image", files__isnull=False) | Q(digi_object_format__title="Video recording", ready_to_stream=True)).filter(collection=current_collection).distinct().select_related().order_by('title')

class DigitalObjectDetailView(DetailView):
    queryset = DigitalObject.objects.filter(published=True).select_related()
    context_object_name = "digital_object"
    template_name = "archive/digitalobject_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(DigitalObjectDetailView, self).get_context_data(**kwargs)
        digifiles = self.object.files.order_by('seq_id')
        context['digifiles'] = digifiles
        return context

# Utility function for search view
def get_search_results(modeltype, query):
    return SearchQuerySet().models(modeltype).auto_query(query)
    
def search_view(request):
    query = creator_matches = location_matches = production_matches = workrecord_matches = False

    if request.GET.has_key('q'):
        # User submitted a search term.
        query = request.GET['q']
        creator_matches = get_search_results(Creator, query)
        location_matches = get_search_results(Location, query)
        production_matches = get_search_results(Production, query)
        workrecord_matches = get_search_results(WorkRecord, query)
        
    context = {}
    if query:
        context['q'] = query
    if creator_matches:
        context['creator_matches'] = creator_matches
    if location_matches:
        context['location_matches'] = location_matches
    if production_matches:
        context['production_matches'] = production_matches
    if workrecord_matches:
        context['workrecord_matches'] = workrecord_matches
        
    return render_to_response('search/search.html', context, RequestContext(request))

def flatpage(request, url, **kwargs):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(TranslatingFlatPage, url__exact=url, sites__id__exact=settings.SITE_ID)
    return render_flatpage(request, f)

@csrf_protect
def render_flatpage(request, f):
    if f.url == '/':
        info = HomePageInfo.objects.get(pk=1)
        if info.box_1_id:
            box_1 = {}
            box_1['obj'] = DigitalObject.objects.get(pk=info.box_1_id)
            box_1['image'] = box_1['obj'].files.all()[0].filepath
        else:
            box_1 = False
        if info.box_2_id:
            box_2 = {}
            box_2['obj'] = DigitalObject.objects.get(pk=info.box_2_id)
            box_2['image'] = box_2['obj'].files.all()[0].filepath
        else:
            box_2 = False
        if info.box_3_id:
            box_3 = {}
            box_3['obj'] = DigitalObject.objects.get(pk=info.box_3_id)
            box_3['image'] = box_3['obj'].files.all()[0].filepath
        else:
            box_3 = False
    else:
        info = False
        box_1 = False
        box_2 = False
        box_3 = False
    if f.template_name:
        t = loader.select_template([f.template_name, DEFAULT_TEMPLATE])
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, { 'flatpage': f, 'info': info, 'box_1': box_1, 'box_2': box_2, 'box_3': box_3 })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, TranslatingFlatPage, f.id)
    return response

