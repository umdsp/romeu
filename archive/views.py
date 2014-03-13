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

import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_protect

from django.db.models import Q, Count


import django.utils.simplejson as json
from django.utils.safestring import mark_safe
from django.utils import timezone

from django.shortcuts import get_object_or_404

from settings import MEDIA_URL, STATIC_URL

from sorl.thumbnail import default

from archive.models import (Creator, Location, Production, WorkRecord,
                            DigitalObject, DigitalFile, Festival,
                            FestivalOccurrence, DirectingMember, CastMember,
                            DesignMember, TechMember, ProductionMember,
                            DocumentationMember, AdvisoryMember, HomePageInfo,
                            TranslatingFlatPage, DigitalObjectType,
                            PhysicalObjectType, Collection, Repository,
                            Award, AwardCandidate, City)
                           
from taggit.models import Tag, TaggedItem
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

from random import randrange
from unaccent.unaccent import monkey_patch_where_node
monkey_patch_where_node()

import urllib2

# For flatpages
DEFAULT_TEMPLATE = 'flatpages/default.html'

class CreatorsListView(ListView):
#    queryset = Creator.objects.filter(published=True).select_related().order_by('creator_name')  - TODO: only use select_related if need to display information related to foreging key field
    queryset = Creator.objects.filter(published=True).order_by('creator_name')
    context_object_name = "creators_list"
    template_name = "archive/creators_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):

        context = super(CreatorsListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_creator__isnull=False, files__isnull=False, digi_object_format=imagetype)
        length = len(alldos) - 1
        count = 0
        dos = []

        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                dos.append(alldos[num])
                count += 1
                
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
        audiotype = DigitalObjectType.objects.get(title='Audio recording')
        
        alldos = DigitalObject.objects.filter(published=True, related_creator=self.object, files__isnull=False, digi_object_format=imagetype).distinct()

        for obj in alldos:
            for file in obj.files.order_by('seq_id'):
                item = {}
                item['image'] = file.filepath
                item['title'] = obj.title
                item['pk'] = obj.pk
                objects_list.append(item)
        context['digital_objects'] = objects_list

        videos = DigitalObject.objects.filter(published=True, related_creator=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
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

        audios = DigitalObject.objects.filter(published=True, related_creator=self.object, digi_object_format=audiotype).distinct()
        audio_list = []
        for audio in audios:
            item = {}
            if audio.poster_image:
                item['poster'] = audio.poster_image
            item['object_id'] = audio.object_number()
            item['title'] = audio.title
            item['pk'] = audio.pk
            audio_list.append(item)
        context['audios'] = audio_list
        
        
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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductionsListView, self).get_context_data(**kwargs)
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_production__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []

        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].first_file():
                dos.append(alldos[num])
                count += 1
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
        audiotype = DigitalObjectType.objects.get(title='Audio recording')
        
        alldos = DigitalObject.objects.filter(published=True, related_production=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        
        for obj in alldos:
            for file in obj.files.order_by('seq_id'):
                item = {}
                item['image'] = file.filepath
                item['title'] = obj.title
                item['pk'] = obj.pk
                objects_list.append(item)
        context['digital_objects'] = objects_list

        videos = DigitalObject.objects.filter(published=True, related_production=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
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


        audios = DigitalObject.objects.filter(published=True, related_production=self.object, digi_object_format=audiotype).distinct()
        audio_list = []
        for audio in audios:
            item = {}
            if audio.poster_image:
                item['poster'] = audio.poster_image
            item['object_id'] = audio.object_number()
            item['title'] = audio.title
            item['pk'] = audio.pk
            audio_list.append(item)
        context['audios'] = audio_list

        return context

class WorkRecordsListView(ListView):

    queryset = WorkRecord.objects.filter(published=True).select_related().order_by('title')
    context_object_name = "writtenworks_list"
    template_name = "archive/workrecords_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):

        context = super(WorkRecordsListView, self).get_context_data(**kwargs)

        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_work__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        while count < 3:
            num = randrange(0, length)
            if alldos[num].files.count() > 0 and alldos[num].first_file():
                dos.append(alldos[num])
                count += 1
#        if dos:
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


        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        audiotype = DigitalObjectType.objects.get(title='Audio recording')

        alldos = DigitalObject.objects.filter(published=True, related_work=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        
        objects_list = []
        for obj in alldos:
            for file in obj.files.order_by('seq_id'):
                item = {}
                item['image'] = file.filepath
                item['title'] = obj.title
                item['pk'] = obj.pk
                objects_list.append(item)
        context['digital_objects'] = objects_list
        
        videos = DigitalObject.objects.filter(published=True, related_work=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
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


        audios = DigitalObject.objects.filter(published=True, related_work=self.object, digi_object_format=audiotype).distinct()
        audio_list = []
        for audio in audios:
            item = {}
            if audio.poster_image:
                item['poster'] = audio.poster_image
            item['object_id'] = audio.object_number()
            item['title'] = audio.title
            item['pk'] = audio.pk
            audio_list.append(item)
        context['audios'] = audio_list        
        
        return context
        
class VenuesListView(ListView):
    
    queryset = Location.objects.filter(published=True).filter(productions__isnull=False).select_related().distinct().order_by('title')
    context_object_name = "venues_list"
    template_name = "archive/venues_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        
        context = super(VenuesListView, self).get_context_data(**kwargs)

        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_venue__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        dos = []
        if length > 0:
            while count < 3:
                num = randrange(0, length)
                if alldos[num].files.count() > 0 and alldos[num].first_file():
                    dos.append(alldos[num])
                    count += 1
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
        videotype = DigitalObjectType.objects.get(title='Video recording')
        audiotype = DigitalObjectType.objects.get(title='Audio recording')

        alldos = DigitalObject.objects.filter(published=True, related_venue=self.object, files__isnull=False, digi_object_format=imagetype).distinct()

        for obj in alldos:
            for file in obj.files.order_by('seq_id'):
                item = {}
                item['image'] = file.filepath
                item['title'] = obj.title
                item['pk'] = obj.pk
                objects_list.append(item)
        context['digital_objects'] = objects_list
            
        videos = DigitalObject.objects.filter(published=True, related_venue=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
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


        audios = DigitalObject.objects.filter(published=True, related_venue=self.object, digi_object_format=audiotype).distinct()
        audio_list = []
        for audio in audios:
            item = {}
            if audio.poster_image:
                item['poster'] = audio.poster_image
            item['object_id'] = audio.object_number()
            item['title'] = audio.title
            item['pk'] = audio.pk
            audio_list.append(item)
        context['audios'] = audio_list             

        if self.object.photo:
            context['venuephoto'] = default.backend.get_thumbnail(self.object.photo.files.all()[0].filepath, "100x100", crop="center")
        return context

class DigitalObjectsListView(ListView):
    queryset = DigitalObject.objects.filter(Q(published=True),
                                            Q(digi_object_format__title="Image",
                                              files__isnull=False) |
                                            Q(digi_object_format__title="Video recording",
                                              ready_to_stream=True)
                                            ).distinct().select_related().order_by('title')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 12

class DigitalObjectsVideosListView(ListView):
    vidtype = DigitalObjectType.objects.get(title="Video recording")
    queryset = DigitalObject.objects.filter(published=True, ready_to_stream=True,
                                            poster_image__isnull=False,
                                            digi_object_format=vidtype
                                            ).distinct().select_related().order_by('-creation_date')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 12

class DigitalObjectsImagesListView(ListView):
    imagetype = DigitalObjectType.objects.get(title="Image")
    queryset = DigitalObject.objects.filter(published=True, files__isnull=False, digi_object_format=imagetype).distinct().select_related().order_by('-creation_date')
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 12

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
    paginate_by = 12

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
    collections_qs = Collection.objects.order_by('repository__repository_id', 'collection_id')
    for c in collections_qs:
        if c.has_viewable_objects():
            collections.append(c)
    context_dict = {'collections': collections}
    return render_to_response('archive/digitalobjecttypes_list.html', context_dict, context_instance=RequestContext(request))

class DigitalObjectsCollectionListView(ListView):
    context_object_name = 'digital_objects'
    template_name = "archive/digitalobjects_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(DigitalObjectsCollectionListView, self).get_context_data(**kwargs)
        temp = self.args[0]
        try:
            temp_repo = Repository.objects.get(repository_id=temp[0:3])
        except Repository.DoesNotExist:
            temp_repo = None
        temp_coll_id = temp[3:]
        try:
            context['current_collection'] = Collection.objects.get(collection_id=temp_coll_id, repository=temp_repo)
        except Collection.DoesNotExist:
            context['current_collection'] = self.args[0]
        return context

    def get_queryset(self):
        temp = self.args[0]
        try:
            temp_repo = Repository.objects.get(repository_id=temp[0:3])
        except Repository.DoesNotExist:
            temp_repo = None
        temp_coll_id = temp[3:]
        current_collection = get_object_or_404(Collection,
                                               collection_id=temp_coll_id,
                                               repository=temp_repo)
        return DigitalObject.objects.filter(
            Q(published=True),
            Q(digi_object_format__title="Image",
              files__isnull=False) |
            Q(digi_object_format__title="Video recording",
              ready_to_stream=True)
            ).filter(collection=current_collection
                     ).distinct().select_related().order_by('title')

class DigitalObjectDetailView(DetailView):
    queryset = DigitalObject.objects.filter(published=True).select_related()
    context_object_name = "digital_object"
    template_name = "archive/digitalobject_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(DigitalObjectDetailView, self).get_context_data(**kwargs)
        digifiles = self.object.files.order_by('seq_id')
        context['digifiles'] = digifiles
        return context

class FestivalsListView(ListView):
    
    queryset = Festival.objects.filter().order_by('title')
    context_object_name = "festivals_list"
    template_name = "archive/festivals_list.html"
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        
        context = super(FestivalsListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id

        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_festival__isnull=False, files__isnull=False, digi_object_format=imagetype)
        length = len(alldos) - 1
        count = 0
        dos = []
        if length > 0:
            while count < 3:
                num = randrange(0, length)
                if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                    dos.append(alldos[num])
                    count += 1

        for obj in dos:
            item = {}
            item['image'] = obj.first_file().filepath
            item['title'] = obj.title
            item['festival_title'] = obj.related_festival.all()[0].title
            item['festival_id'] = obj.related_festival.all()[0].pk
            item['pk'] = obj.pk
            objects_list.append(item)
                
        context['digital_objects'] = objects_list
        return context
         
         
class FestivalsAlphaListView(FestivalsListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = Festival.objects.filter(title__iregex=r'^[0-9!@#$%^&*\(\)]').select_related().order_by('title')
        else:
            qset = Festival.objects.filter(title__istartswith=self.kwargs['alpha']).select_related().order_by('title')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(FestivalsAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context
         
                
class FestivalDetailView(DetailView):
    queryset = Festival.objects.filter().select_related()
    context_object_name = "festival"
    template_name = "archive/festival_detail.html"
    
    def get_context_data(self, **kwargs):

        context = super(FestivalDetailView, self).get_context_data(**kwargs)
        context['festival_occurrences'] = FestivalOccurrence.objects.filter(
            festival_series__id=context['festival'].id,
            published=True).order_by('-begin_date')
        
        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        audiotype = DigitalObjectType.objects.get(title='Audio recording')

        objects_list = []      
        video_list = []
        audio_list = []
        
        for festival_Occurrence_obj in context['festival_occurrences']:
            if festival_Occurrence_obj.has_images():
                fo_images = DigitalObject.objects.filter(published=True, related_festival=festival_Occurrence_obj, files__isnull=False, digi_object_format=imagetype).distinct()
                for obj in fo_images:
                    for file in obj.files.order_by('seq_id'):
                        item = {}
                        item['image'] = file.filepath
                        item['title'] = obj.title
                        item['pk'] = obj.pk
                        objects_list.append(item)

            if festival_Occurrence_obj.has_videos():
                videos = DigitalObject.objects.filter(published=True, related_festival=festival_Occurrence_obj, digi_object_format=videotype, ready_to_stream=True).distinct()
                for vid in videos:
                    item = {}
                    if vid.poster_image:
                        item['poster'] = vid.poster_image
                    item['hidef'] = vid.hi_def_video
                    item['object_id'] = vid.object_number()
                    item['title'] = vid.title
                    item['pk'] = vid.pk
                    video_list.append(item)

            if festival_Occurrence_obj.has_audio():
                audios = DigitalObject.objects.filter(published=True, related_festival=festival_Occurrence_obj, digi_object_format=videotype, ready_to_stream=True).distinct()
                for audio in audios:
                    item = {}
                    if audio.poster_image:
                        item['poster'] = audio.poster_image
                    item['object_id'] = audio.object_number()
                    item['title'] = audio.title
                    item['pk'] = audio.pk
                    audio_list.append(item)

        context['digital_objects'] = objects_list
        context['videos'] = video_list
        context['audios'] = audio_list

#        if self.object.photo:
#            photofile = self.object.photo.first_file()
#            context['festivalphoto'] = photofile.filepath
#        else:
#            context['festivalphoto'] = False

        return context


class FestivalOccurrenceDetailView(DetailView):
    
    queryset = FestivalOccurrence.objects.filter(published=True).select_related()
    context_object_name = "festival_occurrence"
    template_name = "archive/festival_occurrence_detail.html"
    
    def get_context_data(self, **kwargs):

        context = super(FestivalOccurrenceDetailView, self).get_context_data(**kwargs)
        
        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        audiotype = DigitalObjectType.objects.get(title='Audio recording')

        objects_list = []      
        video_list = []
        audio_list = []
        
        fo_images = DigitalObject.objects.filter(published=True, related_festival=self.object, files__isnull=False, digi_object_format=imagetype).distinct()
        for obj in fo_images:
            for file in obj.files.order_by('seq_id'):
                item = {}
                item['image'] = file.filepath
                item['title'] = obj.title
                item['pk'] = obj.pk
                objects_list.append(item)

        videos = DigitalObject.objects.filter(published=True, related_festival=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
        for vid in videos:
            item = {}
            if vid.poster_image:
                item['poster'] = vid.poster_image
            item['hidef'] = vid.hi_def_video
            item['object_id'] = vid.object_number()
            item['title'] = vid.title
            item['pk'] = vid.pk
            video_list.append(item)

        audios = DigitalObject.objects.filter(published=True, related_festival=self.object, digi_object_format=videotype, ready_to_stream=True).distinct()
        for audio in audios:
            item = {}
            if audio.poster_image:
                item['poster'] = audio.poster_image
            item['object_id'] = audio.object_number()
            item['title'] = audio.title
            item['pk'] = audio.pk
            audio_list.append(item)

        context['digital_objects'] = objects_list
        context['videos'] = video_list
        context['audios'] = audio_list

        return context


class AwardsListView(ListView):
    
    queryset = Award.objects.all().order_by('title')
    context_object_name = "awards_list"
    template_name = "archive/awards_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):

        context = super(AwardsListView, self).get_context_data(**kwargs)
        # Make a container for all the object info - link to file + file info + creator id
        objects_list = []
        imagetype = DigitalObjectType.objects.get(title='Image')
        alldos = DigitalObject.objects.filter(published=True, related_award__isnull=False, files__isnull=False, digi_object_format=imagetype)
        count = 0
        length = len(alldos) - 1
        count = 0
        dos = set()

        if length > 0:
            while count < 3:
                num = randrange(0, length)
                if alldos[num].files.count() > 0 and alldos[num].files.all()[0]:
                    dos.add(alldos[num])
                    count += 1

        for obj in dos:
            item = {}
            item['image'] = obj.first_file().filepath
            item['title'] = obj.title
            item['award_title'] = obj.related_award.all()[0].award.title
            item['award_id'] = obj.related_award.all()[0].award.pk
            item['pk'] = obj.pk
            objects_list.append(item)
                
        context['digital_objects'] = objects_list

        return context

class AwardsAlphaListView(AwardsListView):
    def get_queryset(self):
        if self.kwargs['alpha'] == '0':
            qset = Award.objects.filter(title__iregex=r'^[0-9!@#$%^&*\(\)]').select_related().order_by('title')
        else:
            qset = Award.objects.filter(title__istartswith=self.kwargs['alpha']).select_related().order_by('title')
        return qset
    
    def get_context_data(self, **kwargs):
        context = super(AwardsAlphaListView, self).get_context_data(**kwargs)
        if self.kwargs['alpha'] == '0':
            alpha = '#'
        else:
            alpha = self.kwargs['alpha']
        context['alpha'] = alpha
        return context

class AwardDetailView(DetailView):

    queryset = Award.objects.all().select_related(depth=1)
    context_object_name = "award"
    template_name = "archive/award_detail.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(AwardDetailView, self).get_context_data(**kwargs)
        context['award_candidates'] = AwardCandidate.objects.filter(award__id=context['award'].id).order_by('-year')
        
        imagetype = DigitalObjectType.objects.get(title='Image')
        videotype = DigitalObjectType.objects.get(title='Video recording')
        audiotype = DigitalObjectType.objects.get(title='Audio recording')

        objects_list = []      
        video_list = []
        audio_list = []
        
        for award_candidates_obj in context['award_candidates']:
            if award_candidates_obj.has_images():
                ac_images = DigitalObject.objects.filter(published=True, related_award=award_candidates_obj, files__isnull=False, digi_object_format=imagetype).distinct()
                for obj in ac_images:
                    for file in obj.files.order_by('seq_id'):
                        item = {}
                        item['image'] = file.filepath
                        item['title'] = obj.title
                        item['pk'] = obj.pk
                        objects_list.append(item)

            if award_candidates_obj.has_videos():
                videos = DigitalObject.objects.filter(published=True, related_award=award_candidates_obj, digi_object_format=videotype, ready_to_stream=True).distinct()
                for vid in videos:
                    item = {}
                    if vid.poster_image:
                        item['poster'] = vid.poster_image
                    item['hidef'] = vid.hi_def_video
                    item['object_id'] = vid.object_number()
                    item['title'] = vid.title
                    item['pk'] = vid.pk
                    video_list.append(item)

            if award_candidates_obj.has_audio():
                audios = DigitalObject.objects.filter(published=True, related_award=award_candidates_obj, digi_object_format=videotype, ready_to_stream=True).distinct()
                for audio in audios:
                    item = {}
                    if audio.poster_image:
                        item['poster'] = audio.poster_image
                    item['object_id'] = audio.object_number()
                    item['title'] = audio.title
                    item['pk'] = audio.pk
                    audio_list.append(item)

        context['digital_objects'] = objects_list
        context['videos'] = video_list
        context['audios'] = audio_list    
        
        return context


# Utility function for search view
def get_search_results(modeltype, query):
    return SearchQuerySet().models(modeltype).auto_query(query)
    
def search_view(request):
    query = creator_matches = location_matches = production_matches = workrecord_matches = festival_matches = taggeditem_matches = digitalobject_matches = False

    if request.GET.has_key('q'):
        # User submitted a search term.
        query = request.GET['q']
        creator_matches = get_search_results(Creator, query)
        location_matches = get_search_results(Location, query)
        production_matches = get_search_results(Production, query)
        workrecord_matches = get_search_results(WorkRecord, query)
        festival_matches = get_search_results(Festival, query)
        digitalobject_matches = get_search_results(DigitalObject, query)
        taggeditem_matches = get_search_results(TaggedItem, query)
        tag_dict = {}
        for result in taggeditem_matches:
            if result.object is not None:
                if result.object.tag.name in tag_dict:
                    tag_dict[result.object.tag.name] += 1
                else:
                    tag_dict[result.object.tag.name] = 1

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
    if festival_matches:
        context['festival_matches'] = festival_matches
    if digitalobject_matches:
        context['digitalobject_matches'] = digitalobject_matches
    if taggeditem_matches:
        context['taggeditem_matches'] = taggeditem_matches
        context['tag_dict'] = tag_dict
        
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
            box_1['obj'] = DigitalObject.objects.get(pk=info.box_1_id, published=True)
            box_1['image'] = box_1['obj'].files.all()[0].filepath
        else:
            box_1 = False
        if info.box_2_id:
            box_2 = {}
            box_2['obj'] = DigitalObject.objects.get(pk=info.box_2_id, published=True)
            box_2['image'] = box_2['obj'].files.all()[0].filepath
        else:
            box_2 = False
        if info.box_3_id:
            box_3 = {}
            box_3['obj'] = DigitalObject.objects.get(pk=info.box_3_id, published=True)
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

def scalar_search_view(request):
    query = ""

    if request.GET.has_key('q'):
        # User submitted a search term.
        query = request.GET.get('q')

    istream = urllib2.urlopen(urllib2.Request(url="http://localhost:8983/scalar/servlet?q="+query))
    respstr = istream.read()
    return HttpResponse(respstr)

def search_do_view(request):
    query = digitalobject_matches = False

    if request.GET.has_key('q'):
        # User submitted a search term.
        query = request.GET['q']
        digitalobject_matches = get_search_results(DigitalObject, query)

    context = {}
    if query:
        context['q'] = query
    if digitalobject_matches:
        context['digitalobject_matches'] = digitalobject_matches

    return render_to_response('search/search_do.html', context, RequestContext(request))

def show_object(request):
    """ View all objects """
    return simple.direct_to_template(
        request,
        template="taggit/taggit.html",
        extra_context={
            'workrecords':WorkRecord.objects.filter(published=True),
            'productions':Production.objects.filter(published=True),
            'locations':Location.objects.filter(published=True),
            'creators':Creator.objects.filter(published=True),
            'digitalobjects':DigitalObject.objects.filter(published=True),
        })

class TaggedItemsListView(ListView):
    context_object_name = "taggeditems_list"
    template_name = "archive/taggeditems_list.html"
    paginate_by = 120
    model = TaggedItem

    def get_context_data(self, **kwargs):
        context = super(TaggedItemsListView, self).get_context_data(**kwargs)
        if self.request.GET.has_key('tag'):
                query = self.request.GET['tag']
        queryset = TaggedItem.objects.filter(tag__name=query)
        result_list = []
        result_dict = {}
        queryset = Creator.objects.filter(tags__name=query, published=True)
        for x in queryset:
                result_list.append(x)
        if result_list:
                result_dict["creator"] = result_list
        result_list = []
        queryset = Production.objects.filter(tags__name=query, published=True)
        for x in queryset:
                result_list.append(x)
        if result_list:
                result_dict["production"] = result_list
        result_list = []
        queryset = WorkRecord.objects.filter(tags__name=query, published=True)
        for x in queryset:
                result_list.append(x)
        if result_list:
                result_dict["writtenwork"] = result_list
        result_list = []
        queryset = DigitalObject.objects.filter(tags__name=query, published=True)
        for x in queryset:
                result_list.append(x)
        if result_list:
                result_dict["digitalobject"] = result_list
        result_list = []
        context['now'] = timezone.now()
        context['tag_result'] = result_dict
        return context

class TaggedItemDetailView(DetailView):
    queryset = TaggedItem.objects.select_related()
    context_object_name = "taggeditem_detail"
    template_name = "archive/taggeditem_detail.html"
    paginate_by = 10
    model = TaggedItem

    def get_context_data(self, **kwargs):
        context = super(TaggedItemDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def get_creators_json_response(request, g_name="", m_name="", f_name=""):
    
    """
        Returns json response of creators with same names
        according to the names passed in
    """
    
    names = json.loads(request.GET.get('jobj'))
    g_name=names['g_name']
    m_name=names['m_name']
    f_name=names['f_name']

    if ((g_name == "" or g_name is None) and
      (m_name == "" or m_name is None) and
      (f_name == "" or f_name is None)):
  
      json_response = json.dumps([])
      return HttpResponse(json_response, mimetype='application/json')
    
    creator_qs = []
    if g_name:
        creator_qs = Creator.objects.filter(given_name=g_name)

    if m_name:
        if creator_qs:
            creator_qs = creator_qs.filter(middle_name=m_name)
        else:
            creator_qs = Creator.objects.filter(middle_name=m_name)
            
    if f_name:
        if creator_qs:
            creator_qs = creator_qs.filter(family_name=f_name)
        else:
            creator_qs = Creator.objects.filter(family_name=f_name)
    
    creator_list = []
    for creator in creator_qs:
        creator_dict={}
        creator_dict['id']=creator.id
        if creator.given_name:
            creator_dict['g_name']=creator.given_name
        else:
            creator_dict['g_name']=''
        if creator.middle_name:
            creator_dict['m_name']=creator.middle_name
        else:
            creator_dict['m_name']=''
        if creator.family_name:
            creator_dict['f_name']=creator.family_name
        else:
            creator_dict['f_name']=''
        if creator.birth_city:
            creator_dict['b_loc']=creator.birth_city.name
        else:
            creator_dict['b_loc']=''
        creator_dict['b_date']=creator.birth_date_display()
        creator_list.append(creator_dict)

    json_response = json.dumps(creator_list)
  
    return HttpResponse(json_response, mimetype='application/json')

def get_creators_org_name_json_response(request):
    
    """
        Returns json response of creators with same org_names
        according to the org_names passed in
    """
    
    names = json.loads(request.GET.get('jobj'))
    org_name=names['org_name']

    if ((org_name == "" or org_name is None)):
  
      json_response = json.dumps([])
      return HttpResponse(json_response, mimetype='application/json')
  
    creator_qs = Creator.objects.filter(org_name=org_name)
    
    creator_list = []
    for creator in creator_qs:
        creator_dict={}
        creator_dict['id']=creator.id
        creator_dict['org_name']=creator.org_name
        creator_list.append(creator_dict)

    json_response = json.dumps(creator_list)
  
    return HttpResponse(json_response, mimetype='application/json')

def get_cities_json_response(request):
    
    """
        Returns json response of cities with same names
        according to the city and country passed in
    """
    json_object = json.loads(request.GET.get('jobj'))
    city=json_object['city']
    country=json_object['country']

    city_qs = City.objects.filter(name=city,
                                  country__id=country)
    city_list = []
    for city in city_qs:
        city_dict={}
        city_dict['id']=city.id
        city_dict['country']=city.country.name
        city_dict['state']=city.state
        city_dict['city']=city.name
        
        city_list.append(city_dict)
    
    json_response = json.dumps(city_list)
    
    return HttpResponse(json_response, mimetype='application/json')

def get_locations_json_response(request):
    
    """
        Returns json response of Location with same title
        country and city passed in
    """
    json_object = json.loads(request.GET.get('jobj'))
    title_en=json_object['title_en']
    title_es=json_object['title_es']
    title=title_en if title_en else title_es
    city=json_object['city']
    country=json_object['country']

    location_qs = Location.objects.filter(title__icontains=title,
                                          city__id=city,
                                          country__id=country)
    location_list = []
    for location in location_qs:
        location_dict={}
        location_dict['id']=location.id
        location_dict['country']=location.country.name
        location_dict['city']=location.city.name
        location_dict['location']=location.title
        
        location_list.append(location_dict)
    
    json_response = json.dumps(location_list)
    
    return HttpResponse(json_response, mimetype='application/json')

def get_festival_json_response(request):
    
    """
        Returns json response of festival with same title
        passed in
    """
    json_object = json.loads(request.GET.get('jobj'))
    title_en=json_object['title_en']
    title_es=json_object['title_es']
    title=title_en if title_en else title_es

    festival_qs = Festival.objects.filter(title__icontains=title)
    festival_list = []
    for festival in festival_qs:
        festival_dict={}
        festival_dict['id']=festival.id
        festival_dict['festival']=festival.title
        
        festival_list.append(festival_dict)
    
    json_response = json.dumps(festival_list)
    
    return HttpResponse(json_response, mimetype='application/json')