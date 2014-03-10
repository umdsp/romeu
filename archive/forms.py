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
                             DesignTeamFunctionLookup)
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
    
    source_work = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=WorkRecordLookup,
        required=True,
        label=_(u"Source Work"))

    venue = selectable_forms.AutoCompleteSelectField(
        lookup_class=LocationLookup,
        allow_new=False,
        label=_(u"Venue"))

    primary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Primary Bibliography"))
    
    secondary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Secondary Bibliography"))

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


class DirectingMemberAdminForm(ModelForm):

    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(DirectingMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk  
    
    class Meta(object):
        model = DirectingMember


class CastMemberAdminForm(ModelForm):
    
    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))
    role = selectable_forms.AutoCompleteSelectField(
        lookup_class=RoleLookup,
        allow_new=False,
        required=False,
        label=_(u"Role"))
    
    def __init__(self, *args, **kwargs): 
        super(CastMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
            if self.instance.role:
                self.initial['role'] = self.instance.role.pk
    
    class Meta(object):
        model = DirectingMember


class DesignMemberAdminForm(ModelForm):

    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))
    
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
        

class TechMemberAdminForm(ModelForm):
    
    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(TechMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
    
    class Meta(object):
        model = TechMember


class ProductionMemberAdminForm(ModelForm):
    
    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(ProductionMemberAdminForm, self).__init__(*args, **kwargs) 
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk
    
    class Meta(object):
        model = ProductionMember
        

class AdvisoryMemberAdminForm(ModelForm):
    
    person = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Person"))

    def __init__(self, *args, **kwargs):
        super(AdvisoryMemberAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.person:
                self.initial['person'] = self.instance.person.pk


class RoleAdminForm(ModelForm):
    
    source_text = selectable_forms.AutoCompleteSelectField(
        lookup_class=WorkRecordLookup,
        allow_new=False,
        label=_(u"Source text"))
    

    def __init__(self, *args, **kwargs):

        super(RoleAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.source_text:
                self.initial['source_text'] = self.instance.source_text.pk
        

class CreatorAdminForm(ModelForm):
    
    birth_city = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        allow_new=True,
        label=_(u"City of Birth"),
        required=False)
    
    death_city = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        allow_new=False,
        label=_(u"City of Death"),
        required=False)
    
    nationality = selectable_forms.AutoCompleteSelectField(
        lookup_class=CountryLookup,
        allow_new=False,
        label=_(u"Nationality"),
        required=False)
    
    headquarter_city = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        allow_new=False,
        label=_(u"Office / headquarters"),
        required=False)
    
    photo = selectable_forms.AutoCompleteSelectField(
        lookup_class=DigitalObjectLookup,
        allow_new=False,
        label=_(u"Photo"),
        required=False)
    
    primary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Primary Bibliography"))
    
    secondary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Secondary Bibliography"))
    
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
        

class RelatedCreatorAdminForm(ModelForm):
    
    second_creator = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Related creator"))
    
    def __init__(self, *args, **kwargs):
        super(RelatedCreatorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
             if self.instance.second_creator:
                 self.initial['second_creator'] = self.instance.second_creator.pk
        
    class Meta(object):
        model = RelatedCreator
        

class DigitalObjectAdminForm(ModelForm):
    """
    related_creator = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=CreatorLookup,
        label=_(u"Related creator"),
        required=False)
    """
    related_production = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=ProductionLookup,
        label=_(u"Related production"),
        required=False)
    
    related_festival = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=FestivalOccurrenceLookup,
        label=_(u"Related festival"),
        required=False)
    
    related_venue = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=LocationLookup,
        label=_(u"Related venue"),
        required=False)
    
    related_work = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=WorkRecordLookup,
        label=_(u"Related work"),
        required=False)
    """    
    related_award = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=AwardLookup,
        label=_(u"Related award"),
        required=False)
    """
    collection = selectable_forms.AutoCompleteSelectField(
        lookup_class=CollectionLookup,
        allow_new=False,
        label=_(u"Collection"))

    object_creator = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        allow_new=False,
        label=_(u"Object creator"),
        required=False)

    phys_obj_city = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        allow_new=False,
        label=_(u"Physical object city"),
        required=False)

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

        
class LocationAdminForm(ModelForm):

    city = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        label=_(u"City"),
        required=False)
    
    country = selectable_forms.AutoCompleteSelectField(
        lookup_class=CountryLookup,
        label=_(u"Country"))
    
    photo = selectable_forms.AutoCompleteSelectField(
        lookup_class=DigitalObjectLookup,
        label=_(u"Photo"),
        required=False)
    
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


class WorkRecordAdminForm(ModelForm):

    digital_copy = selectable_forms.AutoCompleteSelectField(
        lookup_class=DigitalObjectLookup,
        label=_(u"Digital copy"),
        required=False)

    primary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Primary Bibliography"))
    
    secondary_publications = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=PublicationLookup,
        required=False,
        label=_(u"Secondary Bibliography"))
    
    def __init__(self, *args, **kwargs):
        super(WorkRecordAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.digital_copy:
                self.initial['digital_copy'] = self.instance.digital_copy.pk
       
    class Meta(object):
        model = WorkRecord


class RelatedWorkAdminForm(ModelForm):

    second_work = selectable_forms.AutoCompleteSelectField(
        lookup_class=WorkRecordLookup,
        label=_(u"Related work"))
    
    def __init__(self, *args, **kwargs):
        super(RelatedWorkAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.second_work:
                self.initial['second_work'] = self.instance.second_work.pk
                
    class Meta(object):
        model = RelatedWork
        

class WorkRecordCreatorAdminForm(ModelForm):

    creator = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        label=_(u"Creator"))
    
    def __init__(self, *args, **kwargs):
        super(WorkRecordCreatorAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.creator:
                self.initial['creator'] = self.instance.creator.pk

    class Meta(object):
        model = WorkRecordCreator


class DigitalObjectRelatedCreatorAdminForm(ModelForm):

    creator = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        label=_(u"Creator"))
    
    def __init__(self, *args, **kwargs):
        super(DigitalObjectRelatedCreatorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.creator:
                self.initial['creator'] = self.instance.creator.pk

    class Meta(object):
        model = DigitalObject_Related_Creator

    
class CityAdminForm(ModelForm):
    country = selectable_forms.AutoCompleteSelectField(
        lookup_class=CountryLookup,
        label=_(u"Country"))
    
    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.country:
                self.initial['country'] = self.instance.country.pk

    class Meta(object):
        model = City

        
class RepositoryAdminForm(ModelForm):
    location = selectable_forms.AutoCompleteSelectField(
        lookup_class=LocationLookup,
        label=_(u"Location"))
    
    def __init__(self, *args, **kwargs):
        super(RepositoryAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.location:
                self.initial['location'] = self.instance.location.pk
        
    class Meta(object):
        model = Repository

        
class FestivalOccurrenceAdminForm(ModelForm):
    
    festival_series = selectable_forms.AutoCompleteSelectField(
        lookup_class=FestivalLookup,
        label=_(u"Festival series"))

    venue = selectable_forms.AutoCompleteSelectMultipleField(
        lookup_class=LocationLookup,
        label=_(u"Venue"))

    productions = selectable_forms.AutoCompleteSelectMultipleField(
        required=False,
        lookup_class=ProductionLookup,
        label=_(u"Productions"))

    def __init__(self, *args, **kwargs):
        super(FestivalOccurrenceAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            if self.instance.festival_series:
                self.initial['festival_series'] = self.instance.festival_series.pk

    class Meta(object):
        model = FestivalOccurrence
        

class FestivalParticipantAdminForm(ModelForm):

    participant = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        label=_(u"Participant"))
    
    def __init__(self, *args, **kwargs):
        super(FestivalParticipantAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.participant:
                self.initial['participant'] = self.instance.participant.pk

    class Meta(object):
        model = FestivalParticipant


"""
class BibliographicRecordAdminForm(ModelForm):
    work_record = selectable_forms.AutoCompleteSelectField(lookup_class=WorkRecordLookup, label=_(u"Work record"))

    def __init__(self, *args, **kwargs):
        super(BibliographicRecordAdminForm, self).__init__(*args, **kwargs)
        wrel = ManyToOneRel(WorkRecord, 'id')
        self.fields['work_record'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['work_record'].widget, wrel, self.admin_site)
"""

class StageAdminForm(ModelForm):

    venue = selectable_forms.AutoCompleteSelectField(
        lookup_class=LocationLookup,
        label=_(u"Venue"))

    def __init__(self, *args, **kwargs):
        super(StageAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.venue:
                self.initial['venue'] = self.instance.venue.pk


class AwardCandidateAdminForm(ModelForm):

    award = selectable_forms.AutoCompleteSelectField(
        lookup_class=AwardLookup,
        label=_(u"Award"))

    recipient = selectable_forms.AutoCompleteSelectField(
        lookup_class=CreatorLookup,
        label=_(u"Recipient"))

    production = selectable_forms.AutoCompleteSelectField(
        lookup_class=ProductionLookup,
        required=False,
        label=_(u"Production"))

    place = selectable_forms.AutoCompleteSelectField(
        lookup_class=CityLookup,
        required=False,
        label=_(u"Place"))

    festival = selectable_forms.AutoCompleteSelectField(
        lookup_class=FestivalLookup,
        required=False,
        label=_(u"Festival"))

    work_record = selectable_forms.AutoCompleteSelectField(
        lookup_class=WorkRecordLookup,
        required=False,
        label=_(u"Work record"))

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
