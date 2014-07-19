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
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from archive.models import Creator, Production, WorkRecord
from archive.lookups import (CreatorLookup,
                             ProductionLookup,
                             WorkRecordLookup)
from publications.lookups import PublicationLookup
from publications.models import Publication

import selectable
from selectable import forms as selectable_forms


class PublicationAdminForm(ModelForm):
    
    primary_creators = forms.ModelMultipleChoiceField(
        queryset=Creator.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=CreatorLookup,
            attrs={'size':'100'}))

    secondary_creators = forms.ModelMultipleChoiceField(
        queryset=Creator.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=CreatorLookup,
            attrs={'size':'100'}))

    primary_productions = forms.ModelMultipleChoiceField(
        queryset=Production.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=ProductionLookup,
            attrs={'size':'100'}))

    secondary_productions = forms.ModelMultipleChoiceField(
        queryset=Production.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=ProductionLookup,
            attrs={'size':'100'}))
    
    primary_workrecords = forms.ModelMultipleChoiceField(
        queryset=WorkRecord.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=WorkRecordLookup,
            attrs={'size':'100'}))
    
    secondary_workrecords = forms.ModelMultipleChoiceField(
        queryset=WorkRecord.objects.all(), 
        required=False,
        widget=selectable_forms.AutoCompleteSelectMultipleWidget(
            lookup_class=WorkRecordLookup,
            attrs={'size':'100'}))
    
    def __init__(self, *args, **kwargs): 
        super(PublicationAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['primary_creators'] = self.instance.primary_bibliography_for.all()
            self.initial['secondary_creators'] = self.instance.secondary_bibliography_for.all()
            self.initial['primary_productions'] = self.instance.production_primary_bibliography_for.all()
            self.initial['secondary_productions'] = self.instance.production_secondary_bibliography_for.all()
            self.initial['primary_workrecords'] = self.instance.workedrecord_primary_bibliography_for.all()
            self.initial['secondary_workrecords'] = self.instance.workedrecord_secondary_bibliography_for.all()
        
    class Meta(object):
        model = Publication

