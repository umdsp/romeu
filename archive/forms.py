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

from django.contrib import admin
from django.db.models.fields.related import (ForeignKey, ManyToOneRel,
                                            ManyToManyRel)
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from archive.lookups import (CreatorLookup, ProductionLookup, LocationLookup,
                             RoleLookup, WorkRecordLookup, CountryLookup,
                             DigitalObjectLookup, FestivalLookup,
                             FestivalOccurrenceLookup, TheaterCompanyLookup,
                             CollectionLookup, CityLookup, AwardLookup,
                             DesignTeamFunctionLookup,
                             AwardCandidateLookup)
from publications.lookups import PublicationLookup

import selectable
from selectable import forms as selectable_forms

from archive.models import (Creator, Location, Stage, RelatedCreator, WorkRecord,
                            WorkRecordCreator, WorkRecordFunction, Production,
                            Role, DirectingMember, CastMember, DesignMember,
                            TechMember, ProductionMember, DocumentationMember,
                            AdvisoryMember, Festival, FestivalOccurrence,
                            FestivalParticipant, Repository, Collection,
                            DigitalObject, DigitalFile, DigitalObject_Related_Creator,
                            Award, AwardCandidate,
                            RelatedWork, SubjectHeading, Country, City,
                            Language, DirectingTeamFunction, CastMemberFunction,
                            DesignTeamFunction, TechTeamFunction,
                            ProductionTeamFunction, DocumentationTeamFunction,
                            AdvisoryTeamFunction, OrgFunction,
                            FestivalFunction, PhysicalObjectType,
                            WorkRecordType, VenueType, DigitalObjectType)


class ProductionAdminForm(ModelForm):

    theater_companies = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=TheaterCompanyLookup,
        required=False,
        label=_(u"Theater companies"))
    
    def __init__(self, *args, **kwargs): 
        super(ProductionAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.venue:
                self.initial['venue'] = self.instance.venue.pk        

        corporate_creator = Creator.objects.filter(creator_type='corp',
                                                   org_name__isnull=False)

        self.fields['theater_companies'].widget.update_query_parameters({'theater_companies': corporate_creator })

    class Meta(object):
        model = Production
        widgets = {
            'source_work': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=WorkRecordLookup,
                attrs={'size':'100'}),
            'venue': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=LocationLookup,
                attrs={'size':'100'}),
            'primary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
            'secondary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
        }


class DirectingMemberAdminForm(ModelForm):

    def __init__(self, *args, **kwargs): 
        super(DirectingMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk  
    
    class Meta(object):
        model = DirectingMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'})
        }


class CastMemberAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs): 
        super(CastMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
            if self.instance.role:
                self.initial['role'] = self.instance.role.pk
    
    class Meta(object):
        model = DirectingMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
            'role': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=RoleLookup,
                attrs={'size':'60'}),
        }

class DesignMemberAdminForm(ModelForm):

    """
    functions = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=DesignTeamFunctionLookup,
        required=False,
        label=_(u"Function"))
    """
    
    def __init__(self, *args, **kwargs): 
        super(DesignMemberAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
    
    class Meta(object):
        model = DesignMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'})
        }
        

class TechMemberAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs): 
        super(TechMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
    
    class Meta(object):
        model = TechMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'})
        }


class ProductionMemberAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs): 
        super(ProductionMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
    
    class Meta(object):
        model = ProductionMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'})
        }
        

class AdvisoryMemberAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(AdvisoryMemberAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk

    class Meta(object):
        model = AdvisoryMember
        widgets = {
            'person': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'})
        }

class RoleAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):

        super(RoleAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.source_text:
                self.initial['source_text'] = self.instance.source_text.pk

    class Meta(object):
        model = Role
        widgets = {
            'source_text': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=WorkRecordLookup,
                attrs={'size':'100'}),
        }


class CreatorAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs): 
         super(CreatorAdminForm, self).__init__(*args, **kwargs) 
         
         if self.instance and self.instance.pk:
             if self.instance.birth_city:
                 self.initial['birth_city'] = self.instance.birth_city.pk
             if self.instance.death_city:
                 self.initial['death_city'] = self.instance.death_city.pk
             if self.instance.nationality:
                 self.initial['nationality'] = self.instance.nationality.pk
             if self.instance.headquarter_city:
                 self.initial['headquarter_city'] = self.instance.headquarter_city.pk
             if self.instance.photo:
                 self.initial['photo'] = self.instance.photo.pk

    class Meta(object):
        model = Creator
        widgets = {
            'birth_city': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'60'}),
            'death_city': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'60'}),
            'nationality': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CountryLookup,
                attrs={'size':'60'}),
            'headquarter_city': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'60'}),
            'photo': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=DigitalObjectLookup,
                attrs={'size':'60'}),
            'primary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
            'secondary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
        }
        

class RelatedCreatorAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RelatedCreatorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
             if self.instance.second_creator:
                 self.initial['second_creator'] = self.instance.second_creator.pk
        
    class Meta(object):
        model = RelatedCreator
        widgets = {
            'second_creator': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'60'}),
        }
        

class DigitalObjectAdminForm(ModelForm):

    replicate_tags = forms.BooleanField(
        required=False,
        label=_('Associate Tags with Production and Work record'))
    
    def __init__(self, *args, **kwargs):
        super(DigitalObjectAdminForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            if self.instance.collection:
                self.initial['collection'] = self.instance.collection.pk
            if self.instance.object_creator:
                self.initial['object_creator'] = self.instance.object_creator.pk
            if self.instance.phys_obj_city:
                self.initial['phys_obj_city'] = self.instance.phys_obj_city.pk

        
    class Meta(object):
        model = DigitalObject
        widgets = {
            'related_production': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=ProductionLookup,
                attrs={'size':'100'}),
            'related_festival': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=FestivalOccurrenceLookup,
                attrs={'size':'100'}),
            'related_venue': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=LocationLookup,
                attrs={'size':'100'}),
            'related_work': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=WorkRecordLookup,
                attrs={'size':'100'}),
            'related_award': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=AwardCandidateLookup,
                attrs={'size':'100'}),
            'collection': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CollectionLookup,
                attrs={'size':'100'}),
            'object_creator': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
            'phys_obj_city': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'100'}),
        }

        
class LocationAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.city:
                self.initial['city'] = self.instance.city.pk
            if self.instance.country:
                self.initial['country'] = self.instance.country.pk
            if self.instance.photo:
                self.initial['photo'] = self.instance.photo.pk
        
    class Meta(object):
        model = Location
        widgets = {
            'city': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'100'}),
            'country': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CountryLookup,
                attrs={'size':'100'}),
            'photo': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=DigitalObjectLookup,
                attrs={'size':'100'}),
        }


class WorkRecordAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkRecordAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.digital_copy:
                self.initial['digital_copy'] = self.instance.digital_copy.pk
       
    class Meta(object):
        model = WorkRecord
        widgets = {
            'digital_copy': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=DigitalObjectLookup,
                attrs={'size':'60'}),
            'primary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
            'secondary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}),
        }


class RelatedWorkAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RelatedWorkAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.second_work:
                self.initial['second_work'] = self.instance.second_work.pk

    class Meta(object):
        model = RelatedWork
        widgets = {
            'second_work': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=WorkRecordLookup,
                attrs={'size':'100'}),
        }
        

class WorkRecordCreatorAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkRecordCreatorAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.creator:
                self.initial['creator'] = self.instance.creator.pk

    class Meta(object):
        model = WorkRecordCreator
        widgets = {
            'creator': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
        }


class DigitalObjectRelatedCreatorAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DigitalObjectRelatedCreatorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.creator:
                self.initial['creator'] = self.instance.creator.pk

    class Meta(object):
        model = DigitalObject_Related_Creator
        widgets = {
            'creator': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
        }

    
class CityAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.country:
                self.initial['country'] = self.instance.country.pk


    class Meta(object):
        model = City
        widgets={
            'country': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CountryLookup,
                attrs={'size':'100'}),
        }

        
class RepositoryAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RepositoryAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.location:
                self.initial['location'] = self.instance.location.pk
        
    class Meta(object):
        model = Repository
        widgets = {
            'location': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=LocationLookup,
                attrs={'size':'100'})
        }
        
class FestivalOccurrenceAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FestivalOccurrenceAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.festival_series:
                self.initial['festival_series'] = self.instance.festival_series.pk

    class Meta(object):
        model = FestivalOccurrence
        widgets = {
            'festival_series': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=FestivalLookup,
                attrs={'size':'100'}),
            'venue': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=LocationLookup,
                attrs={'size':'100'}),
            'productions': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=ProductionLookup,
                attrs={'size':'100'}),
            'primary_publications': selectable_forms.AutoCompleteSelectMultipleWidget(
                lookup_class=PublicationLookup,
                attrs={'size':'100'}), 
        }
        

class FestivalParticipantAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FestivalParticipantAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.participant:
                self.initial['participant'] = self.instance.participant.pk

    class Meta(object):
        model = FestivalParticipant
        widgets = {
            'participant': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
        }


class StageAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StageAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.venue:
                self.initial['venue'] = self.instance.venue.pk

    class Meta(object):
        model = Stage
        widgets = {
            'venue': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=LocationLookup,
                attrs={'size':'100'}),
        }

class AwardCandidateAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AwardCandidateAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.award:
                self.initial['award'] = self.instance.award.pk
            if self.instance.recipient:
                self.initial['recipient'] = self.instance.recipient.pk
            if self.instance.production:
                self.initial['production'] = self.instance.production.pk
            if self.instance.place:
                self.initial['place'] = self.instance.place.pk
            if self.instance.festival:
                self.initial['festival'] = self.instance.festival.pk
            if self.instance.work_record:
                self.initial['work_record'] = self.instance.work_record.pk
                
    class Meta(object):
        model = AwardCandidate
        widgets = {
            'award': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=AwardLookup,
                attrs={'size':'100'}),
            'recipient': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CreatorLookup,
                attrs={'size':'100'}),
            'production': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=ProductionLookup,
                attrs={'size':'100'}),
            'place': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=CityLookup,
                attrs={'size':'100'}),
            'festival': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=FestivalLookup,
                attrs={'size':'100'}),
            'work_record': selectable_forms.AutoCompleteSelectWidget(
                lookup_class=WorkRecordLookup,
                attrs={'size':'100'}),
        }

