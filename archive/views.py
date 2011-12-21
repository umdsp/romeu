from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator, InvalidPage, EmptyPage

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

from archive.models import Creator, Location, Production, WorkRecord, DigitalObject, DigitalFile, Festival, FestivalOccurrence, DirectingMember, CastMember, DesignMember, TechMember, ProductionMember, DocumentationMember, AdvisoryMember, TranslatingFlatPage, DigitalObjectType

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

from random import randrange

class CreatorsListView(ListView):
    queryset = Creator.objects.filter(published=True).select_related().order_by('creator_name')
    context_object_name = "creators_list"
    template_name = "archive/creators_list.html"
    paginate_by = 100
    
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
                item['image'] = obj.files.all()[0].filepath
                item['title'] = obj.title
                item['creator_name'] = obj.related_creator.all()[0].display_name
                item['creator_id'] = obj.related_creator.all()[0].pk
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
        if self.object.photo:
            context['creatorphoto'] = default.backend.get_thumbnail(self.object.photo.filepath, "100x100", crop="center")
        else:
            context['creatorphoto'] = '/static/images/nophoto.jpg'
        return context
        
        
class ProductionsListView(ListView):
    queryset = Production.objects.filter(published=True).select_related().order_by('title')
    context_object_name = "productions_list"
    template_name = "archive/productions_list.html"
    paginate_by = 100

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
            if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                dos.append(alldos[num])
                count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.files.all()[0].filepath
                item['title'] = obj.title
                item['production_title'] = obj.related_production.all()[0].title
                item['production_id'] = obj.related_production.all()[0].pk
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
        dos = DigitalObject.objects.select_related().filter(related_production__pk=self.object.pk).filter(files__isnull=False)
        if dos.exists():
            viewmore = False
            files = DigitalFile.objects.select_related().filter(digital_object__in=dos).order_by('?')
            if files.count() > 10:
                viewmore = True
            context['productionobjects'] = files[:10]
            context['viewmore'] = viewmore
        directing_team = []
        if DirectingMember.objects.filter(production__pk=self.object.pk).exists():
            for item in DirectingMember.objects.filter(production__pk=self.object.pk):
                directing_team.append(item)
        context['directing_team'] = directing_team
        cast = []
        if CastMember.objects.filter(production__pk=self.object.pk).exists():
            for item in CastMember.objects.filter(production__pk=self.object.pk):
                cast.append(item)
        context['cast'] = cast
        return context

class WorkRecordsListView(ListView):
    queryset = WorkRecord.objects.filter(published=True).select_related().order_by('title')
    context_object_name = "writtenworks_list"
    template_name = "archive/workrecords_list.html"
    paginate_by = 100
    
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
            if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                dos.append(alldos[num])
                count += 1
        if dos:
            for obj in dos:
                item = {}
                item['image'] = obj.files.all()[0].filepath
                item['title'] = obj.title
                item['work_title'] = obj.related_work.all()[0].title
                item['work_id'] = obj.related_work.all()[0].pk
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
        digiobj = DigitalObject.objects.filter(related_work__pk=self.object.pk).filter(files__isnull=False).order_by('?')
        if digiobj.exists():
            context['workrecordphoto'] = MEDIA_URL + default.backend.get_thumbnail(digiobj[0].files.order_by('?')[0].filepath, "100x100", crop='center').name
        else:
            context['workrecordphoto'] = STATIC_URL + 'images/nophoto.jpg'
        return context
        
class VenuesListView(ListView):
    queryset = Location.objects.filter(published=True).filter(productions__isnull=False).select_related().distinct().order_by('title')
    context_object_name = "venues_list"
    template_name = "archive/venues_list.html"
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        context = super(VenuesListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(locations__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        if length > 0:
            while count < 3:
                num = randrange(0, length)
                if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                    dos.append(alldos[num])
                    count += 1
        if dos:
            for obj in dos[:6]:
                item = {}
                item['image'] = obj.files.all()[0].filepath
                item['title'] = obj.title
                item['venue_title'] = obj.locations.all()[0].title
                item['loc_id'] = obj.locations.all()[0].pk
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
        if self.object.photo:
            context['venuephoto'] = default.backend.get_thumbnail(self.object.photo.filepath, "100x100", crop="center")
        else:
            context['venuephoto'] = '/static/images/nophoto.jpg'
        return context
        
class DigitalObjectsListView(ListView):
    imagetype = DigitalObjectType.objects.get(title="Image")
    queryset = DigitalObject.objects.filter(published=True, files__isnull=False, digi_object_format=imagetype).distinct().select_related().order_by('-digital_object__creation_date')
    context_object_name = 'digital_objects'
    dos = []
    for obj in queryset:
        item = {}
        item['image'] = obj.files.all()[0].filepath
        item['title'] = obj.title
        item['pk'] = obj.pk
        dos.append(item)
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 30
        
class DigitalObjectDetailView(DetailView):
    queryset = DigitalObject.objects.filter(published=True).select_related()
    context_object_name = "digital_object"
    template_name = "archive/digitalobject_detail.html"
    
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
    if f.template_name:
        t = loader.select_template(f.template_name, DEFAULT_TEMPLATE)
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, { 'flatpage': f })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, TranslatingFlatPage, f.id)
    return response

