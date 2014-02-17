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
                             CollectionLookup, CityLookup, AwardLookup)

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
    venue = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup,
                                                     allow_new=False, label=_(u"Venue"))
#    theater_companies = selectable_forms.AutoCompleteSelectMultipleField(
#                                            lookup_class=TheaterCompanyLookup,
#                                            required=False,
#                                            label=_(u"Theater companies"))

    def __init__(self, *args, **kwargs): 
        super(ProductionAdminForm, self).__init__(*args, **kwargs)
        vrel = ManyToOneRel(Location, 'id') 
        tcrel = ManyToManyRel(Creator, 'id')
        self.fields['venue'].widget = admin.widgets.RelatedFieldWidgetWrapper(
            self.fields['venue'].widget, vrel, self.admin_site)
#        self.fields['theater_companies'].widget = admin.widgets.RelatedFieldWidgetWrapper(
#            self.fields['theater_companies'].widget, tcrel, self.admin_site)
        
        corporate_creator = Creator.objects.filter(creator_type='corp',
                                                   org_name__isnull=False)
        self.fields['theater_companies'].queryset = corporate_creator

    class Meta(object):
        model = Production

class DirectingMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(DirectingMemberAdminForm, self).__init__(*args, **kwargs) 
        prel = ManyToOneRel(Creator, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)
    
    class Meta(object):
        model = DirectingMember

class CastMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))
    role = selectable_forms.AutoCompleteSelectField(lookup_class=RoleLookup, allow_new=False, required=False, label=_(u"Role"))
    
    def __init__(self, *args, **kwargs): 
        super(CastMemberAdminForm, self).__init__(*args, **kwargs) 
        prel = ManyToOneRel(Creator, 'id')
        rrel = ManyToOneRel(Role, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)
        self.fields['role'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['role'].widget, rrel, self.admin_site)
    
    class Meta(object):
        model = DirectingMember

class DesignMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(DesignMemberAdminForm, self).__init__(*args, **kwargs) 
        prel = ManyToOneRel(Creator, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)
    
    class Meta(object):
        model = DesignMember
        
class TechMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(TechMemberAdminForm, self).__init__(*args, **kwargs) 
        prel = ManyToOneRel(Creator, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)
    
    class Meta(object):
        model = TechMember

class ProductionMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))
    
    def __init__(self, *args, **kwargs): 
        super(ProductionMemberAdminForm, self).__init__(*args, **kwargs) 
        prel = ManyToOneRel(Creator, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)
    
    class Meta(object):
        model = ProductionMember
        
class AdvisoryMemberAdminForm(ModelForm):
    person = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Person"))

    def __init__(self, *args, **kwargs):
        super(AdvisoryMemberAdminForm, self).__init__(*args, **kwargs)
        prel = ManyToOneRel(Creator, 'id')
        self.fields['person'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['person'].widget, prel, self.admin_site)

class RoleAdminForm(ModelForm):
    source_text = selectable_forms.AutoCompleteSelectField(lookup_class=WorkRecordLookup, allow_new=False, label=_(u"Source text"))
    
    def __init__(self, *args, **kwargs):
        super(RoleAdminForm, self).__init__(*args, **kwargs)
        wrel = ManyToOneRel(WorkRecord, 'id')
        self.fields['source_text'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['source_text'].widget, wrel, self.admin_site)
        
class CreatorAdminForm(ModelForm):
    birth_location = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, allow_new=False, label=_(u"Birth location"), required=False)
    death_location = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, allow_new=False, label=_(u"Death location"), required=False)
    nationality = selectable_forms.AutoCompleteSelectField(lookup_class=CountryLookup, allow_new=False, label=_(u"Nationality"), required=False)
    location = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, allow_new=False, label=_(u"Office / headquarters"), required=False)
    photo = selectable_forms.AutoCompleteSelectField(lookup_class=DigitalObjectLookup, allow_new=False, label=_(u"Photo"), required=False)
    
    def __init__(self, *args, **kwargs): 
        super(CreatorAdminForm, self).__init__(*args, **kwargs) 
        lrel = ManyToOneRel(Location, 'id')
        crel = ManyToOneRel(Country, 'id')
        dorel = ManyToOneRel(DigitalObject, 'id')
        self.fields['birth_location'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['birth_location'].widget, lrel, self.admin_site)
        self.fields['death_location'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['death_location'].widget, lrel, self.admin_site)
        self.fields['nationality'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['nationality'].widget, crel, self.admin_site)
        self.fields['location'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['location'].widget, lrel, self.admin_site)
        self.fields['photo'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['photo'].widget, dorel, self.admin_site)

    class Meta(object):
        model = Creator
        
class RelatedCreatorAdminForm(ModelForm):
    second_creator = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Related creator"))
    
    def __init__(self, *args, **kwargs):
        super(RelatedCreatorAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Creator, 'id')
        self.fields['second_creator'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['second_creator'].widget, crel, self.admin_site)
        
    class Meta(object):
        model = RelatedCreator
        
class DigitalObjectAdminForm(ModelForm):

    related_creator = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=CreatorLookup, label=_(u"Related creator"), required=False)
    related_production = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=ProductionLookup, label=_(u"Related production"), required=False)
    related_festival = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=FestivalOccurrenceLookup, label=_(u"Related festival"), required=False)
    related_venue = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=LocationLookup, label=_(u"Related venue"), required=False)
    related_work = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=WorkRecordLookup, label=_(u"Related work"), required=False)
    related_award = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=AwardLookup, label=_(u"Related award"), required=False)

    collection = selectable_forms.AutoCompleteSelectField(lookup_class=CollectionLookup, allow_new=False, label=_(u"Collection"))
    object_creator = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, allow_new=False, label=_(u"Object creator"), required=False)
    phys_obj_location = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, allow_new=False, label=_(u"Physical object location"), required=False)
    replicate_tags = forms.BooleanField(required=False, label=_('Associate Tags with Production and Work record'))
    
    def __init__(self, *args, **kwargs):
        super(DigitalObjectAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Creator, 'id')
        prel = ManyToOneRel(Production, 'id')
        frel = ManyToOneRel(FestivalOccurrence, 'id')
        lrel = ManyToOneRel(Location, 'id')
        wrel = ManyToOneRel(WorkRecord, 'id')
        awrel = ManyToOneRel(Award, 'id')
        colrel = ManyToOneRel(Collection, 'id')
        self.fields['related_creator'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_creator'].widget, crel, self.admin_site)
        self.fields['related_production'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_production'].widget, prel, self.admin_site)
        self.fields['related_festival'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_festival'].widget, frel, self.admin_site)
        self.fields['related_venue'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_venue'].widget, lrel, self.admin_site)
        self.fields['related_work'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_work'].widget, wrel, self.admin_site)
        self.fields['related_award'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['related_award'].widget, awrel, self.admin_site)
        self.fields['collection'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['collection'].widget, colrel, self.admin_site)
        self.fields['object_creator'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['object_creator'].widget, crel, self.admin_site)
        self.fields['phys_obj_location'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['phys_obj_location'].widget, lrel, self.admin_site)
        
    class Meta(object):
        model = DigitalObject
        
class LocationAdminForm(ModelForm):
    city = selectable_forms.AutoCompleteSelectField(lookup_class=CityLookup, label=_(u"City"), required=False)
    country = selectable_forms.AutoCompleteSelectField(lookup_class=CountryLookup, label=_(u"Country"))
    photo = selectable_forms.AutoCompleteSelectField(lookup_class=DigitalObjectLookup, label=_(u"Photo"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)
        cityrel = ManyToOneRel(City, 'id')
        countryrel = ManyToOneRel(Country, 'id')
        dorel = ManyToOneRel(DigitalObject, 'id')
        self.fields['city'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['city'].widget, cityrel, self.admin_site)
        self.fields['country'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['country'].widget, countryrel, self.admin_site)
        self.fields['photo'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['photo'].widget, dorel, self.admin_site)
        
    class Meta(object):
        model = Location

class WorkRecordAdminForm(ModelForm):
    digital_copy = selectable_forms.AutoCompleteSelectField(lookup_class=DigitalObjectLookup, label=_(u"Digital copy"), required=False)
    
    def __init__(self, *args, **kwargs):
        super(WorkRecordAdminForm, self).__init__(*args, **kwargs)
        dorel = ManyToOneRel(DigitalObject, 'id')
        self.fields['digital_copy'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['digital_copy'].widget, dorel, self.admin_site)
        
    class Meta(object):
        model = WorkRecord
        
class RelatedWorkAdminForm(ModelForm):
    second_work = selectable_forms.AutoCompleteSelectField(lookup_class=WorkRecordLookup, label=_(u"Related work"))
    
    def __init__(self, *args, **kwargs):
        super(RelatedWorkAdminForm, self).__init__(*args, **kwargs)
        wrel = ManyToOneRel(WorkRecord, 'id')
        self.fields['second_work'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['second_work'].widget, wrel, self.admin_site)
        
    class Meta(object):
        model = RelatedWork
        
class WorkRecordCreatorAdminForm(ModelForm):
    creator = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, label=_(u"Creator"))
    
    def __init__(self, *args, **kwargs):
        super(WorkRecordCreatorAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Creator, 'id')
        self.fields['creator'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['creator'].widget, crel, self.admin_site)
        
    class Meta(object):
        model = WorkRecordCreator


class DigitalObjectRelatedCreatorAdminForm(ModelForm):
    creator = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, label=_(u"Creator"))
    
    def __init__(self, *args, **kwargs):
        super(DigitalObjectRelatedCreatorAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Creator, 'id')
        self.fields['creator'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['creator'].widget, crel, self.admin_site)
        
    class Meta(object):
        model = DigitalObject_Related_Creator

    
class CityAdminForm(ModelForm):
    country = selectable_forms.AutoCompleteSelectField(lookup_class=CountryLookup, label=_(u"Country"))
    
    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Country, 'id')
        self.fields['country'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['country'].widget, crel, self.admin_site)
        
    class Meta(object):
        model = City
        
class RepositoryAdminForm(ModelForm):
    location = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, label=_(u"Location"))
    
    def __init__(self, *args, **kwargs):
        super(RepositoryAdminForm, self).__init__(*args, **kwargs)
        lrel = ManyToOneRel(Location, 'id')
        self.fields['location'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['location'].widget, lrel, self.admin_site)
        
    class Meta(object):
        model = Repository
        
class FestivalOccurrenceAdminForm(ModelForm):
    festival_series = selectable_forms.AutoCompleteSelectField(lookup_class=FestivalLookup, label=_(u"Festival series"))
 #   venue = selectable_forms.AutoCompleteSelectMultipleField(lookup_class=LocationLookup, label=_(u"Venue"))
#    productions = selectable_forms.AutoCompleteSelectMultipleField(required=False, lookup_class=ProductionLookup, label=_(u"Productions"))

    def __init__(self, *args, **kwargs):
        super(FestivalOccurrenceAdminForm, self).__init__(*args, **kwargs)
        frel = ManyToOneRel(Festival, 'id')
        lrel = ManyToOneRel(Location, 'id')
        prel = ManyToManyRel(Production, 'id')
        self.fields['festival_series'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['festival_series'].widget, frel, self.admin_site)
#        self.fields['venue'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['venue'].widget, lrel, self.admin_site)
#        self.fields['productions'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['productions'].widget, prel, self.admin_site)
        
    class Meta(object):
        model = FestivalOccurrence
        
class FestivalParticipantAdminForm(ModelForm):
    participant = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, label=_(u"Participant"))
    
    def __init__(self, *args, **kwargs):
        super(FestivalParticipantAdminForm, self).__init__(*args, **kwargs)
        crel = ManyToOneRel(Creator, 'id')
        self.fields['participant'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['participant'].widget, crel, self.admin_site)
        
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
    venue = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, label=_(u"Venue"))

    def __init__(self, *args, **kwargs):
        super(StageAdminForm, self).__init__(*args, **kwargs)
        lrel = ManyToOneRel(Location, 'id')
        self.fields['venue'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['venue'].widget, lrel, self.admin_site)

class AwardCandidateAdminForm(ModelForm):
    award = selectable_forms.AutoCompleteSelectField(lookup_class=AwardLookup, label=_(u"Award"))
    recipient = selectable_forms.AutoCompleteSelectField(lookup_class=CreatorLookup, label=_(u"Recipient"))
    production = selectable_forms.AutoCompleteSelectField(lookup_class=ProductionLookup, required=False, label=_(u"Production"))
    place = selectable_forms.AutoCompleteSelectField(lookup_class=LocationLookup, required=False, label=_(u"Place"))
    festival = selectable_forms.AutoCompleteSelectField(lookup_class=FestivalLookup, required=False, label=_(u"Festival"))
    work_record = selectable_forms.AutoCompleteSelectField(lookup_class=WorkRecordLookup, required=False, label=_(u"Work record"))

    def __init__(self, *args, **kwargs):
        super(AwardCandidateAdminForm, self).__init__(*args, **kwargs)
        arel = ManyToOneRel(Award, 'id')
        crel = ManyToOneRel(Creator, 'id')
        prel = ManyToOneRel(Production, 'id')
        lrel = ManyToOneRel(Location, 'id')
        frel = ManyToOneRel(Festival, 'id')
        wrel = ManyToOneRel(WorkRecord, 'id')
        self.fields['award'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['award'].widget, arel, self.admin_site)
        self.fields['recipient'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['recipient'].widget, crel, self.admin_site)
        self.fields['production'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['production'].widget, prel, self.admin_site)
        self.fields['place'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['place'].widget, lrel, self.admin_site)
        self.fields['festival'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['festival'].widget, frel, self.admin_site)
        self.fields['work_record'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['work_record'].widget, wrel, self.admin_site)
