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

from archive.models import (Creator, Location, Stage, RelatedCreator, WorkRecord,
                            WorkRecordCreator, WorkRecordFunction, Production,
                            Role, DirectingMember, CastMember, DesignMember,
                            TechMember, ProductionMember, DocumentationMember,
                            AdvisoryMember, Festival, FestivalOccurrence,
                            FestivalParticipant, Repository, Collection,
                            DigitalObject, DigitalFile, DigitalObject_Related_Creator,
                            Award, AwardCandidate,
                            RelatedWork, SubjectHeading, 
                            Country, City, Language, DirectingTeamFunction,
                            CastMemberFunction, DesignTeamFunction,
                            TechTeamFunction, ProductionTeamFunction,
                            DocumentationTeamFunction, AdvisoryTeamFunction,
                            OrgFunction, FestivalFunction, PhysicalObjectType,
                            WorkRecordType, VenueType, DigitalObjectType,
                            License, HomePageInfo, SpecialPerformanceType)

from unaccent.unaccent import monkey_patch_where_node
monkey_patch_where_node()

from modeltranslation.admin import TranslationAdmin

from django.utils.translation import ugettext_lazy as _

from archive.lookups import (CreatorLookup, ProductionLookup, LocationLookup,
                             RoleLookup, WorkRecordLookup, CountryLookup,
                             DigitalObjectLookup, CityLookup)
from archive import forms as arcforms

from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
# from django.db.models.query import CollectedObjects
from django.db.models.fields.related import ForeignKey, ManyToOneRel
from django.forms.models import model_to_dict
from django.db.models.fields import CharField

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from reversion.admin import VersionAdmin

#import selectable
#from selectable import forms as selectable_forms

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.sites.models import Site
from archive.models import TranslatingFlatPage

from settings import MEDIA_URL, STATIC_URL

class AjaxTranslationAdmin(AjaxSelectAdmin, TranslationAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AjaxTranslationAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

class AjaxUltraAdmin(AjaxTranslationAdmin, VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AjaxUltraAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

class TranslatingVersioningAdmin(TranslationAdmin, VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslatingVersioningAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

class AjaxInlineAdmin(admin.TabularInline):
    def get_form(self, request, obj=None, **kwargs):
        form = super(AjaxInlineAdmin,self).get_form(request,obj,**kwargs)
        autoselect_fields_check_can_add(form,self.model,request.user)
        return form


# Actions for all model types
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected items as published"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = "Mark selected items as unpublished"

# def clone_objects(objects, title_fieldnames):
#     def clone(from_object, title_fieldnames):
#         args = dict([(fld.name, getattr(from_object, fld.name)) for fld in from_object._meta.fields if fld is not from_object._meta.pk])
# 
#         for field in from_object._meta.fields:
#             if field.name in title_fieldnames:
#                 if isinstance(field, CharField):
#                     args[field.name] = getattr(from_object, field.name) + " (copy)"
# 
#         return from_object.__class__.objects.create(**args)
# 
#     if not hasattr(objects,'__iter__'):
#        objects = [ objects ]
# 
#     # We always have the objects in a list now
#     objs = []
#     for object in objects:
#         obj = clone(object, title_fieldnames)
#         obj.save()
#         objs.append(obj)
# 
# def action_clone(modeladmin, request, queryset):
#     objs = clone_objects(queryset, ("name", "title"))
# action_clone.short_description = "Duplicate the selected objects"


# INLINE MODELS
class RelatedWorkInline(admin.TabularInline):
    form = arcforms.RelatedWorkAdminForm
    model = RelatedWork
    extra = 0
    fk_name = 'first_work'
    
    def __init__(self, model, admin_site):
        super(RelatedWorkInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class RelatedCreatorInline(admin.TabularInline):
    form = arcforms.RelatedCreatorAdminForm
    model = RelatedCreator
    extra = 0
    fk_name = 'first_creator'
    
    def __init__(self, model, admin_site):
        super(RelatedCreatorInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
        

class DigitalObjectRelatedCreatorInline(admin.TabularInline):
    form = arcforms.DigitalObjectRelatedCreatorAdminForm
    model = DigitalObject_Related_Creator
    extra = 0
    
    def __init__(self, model, admin_site):
        super(DigitalObjectRelatedCreatorInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site


class WorkRecordCreatorInline(admin.TabularInline):
    form = arcforms.WorkRecordCreatorAdminForm
    model = WorkRecordCreator
    extra = 0
    
    def __init__(self, model, admin_site):
        super(WorkRecordCreatorInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class DirectingMemberInline(admin.TabularInline):
    form = arcforms.DirectingMemberAdminForm
    model = DirectingMember
    extra = 0

    def __init__(self, model, admin_site):
        super(DirectingMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class CastMemberInline(admin.TabularInline):
    form = arcforms.CastMemberAdminForm
    model = CastMember
    extra = 0

    def __init__(self, model, admin_site):
        super(CastMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class DesignMemberInline(admin.TabularInline):
    form = arcforms.DesignMemberAdminForm
    model = DesignMember
    extra = 0

    def __init__(self, model, admin_site):
        super(DesignMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class TechMemberInline(admin.TabularInline):
    form = arcforms.TechMemberAdminForm
    model = TechMember
    extra = 0

    def __init__(self, model, admin_site):
        super(TechMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class ProductionMemberInline(admin.TabularInline):
    form = arcforms.ProductionMemberAdminForm
    model = ProductionMember
    extra = 0

    def __init__(self, model, admin_site):
        super(ProductionMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class AdvisoryMemberInline(admin.TabularInline):
    form = arcforms.AdvisoryMemberAdminForm
    model = AdvisoryMember
    extra = 0

    def __init__(self, model, admin_site):
        super(AdvisoryMemberInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class FestivalParticipantInline(admin.TabularInline):
    form = arcforms.FestivalParticipantAdminForm
    model = FestivalParticipant
    extra = 0

    def __init__(self, model, admin_site):
        super(FestivalParticipantInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class RoleInline(admin.TabularInline):
    model = Role
    extra = 1

class StageInline(admin.StackedInline):
    model = Stage
    extra = 0

class DigitalFileInline(admin.TabularInline):
    model = DigitalFile
    extra = 1
    verbose_name = "digital file"
    verbose_name_plural = "digital files"

# ADMIN MODELS
class CreatorAdmin(TranslationAdmin):
    form = arcforms.CreatorAdminForm
    list_display = ('creator_name', 'nationality', 'birth_date_display', 'death_date_display', 'has_system_links',)
    list_filter = ('published','has_attention','creator_type',)
    exclude = ('creator_name',)
    date_hierarchy = 'birth_date'
    search_fields = ['creator_name', 'creator_ascii_name', 'name_variants']
    inlines = (RelatedCreatorInline,)
#    filter_horizontal = ['primary_publications', 'secondary_publications']     
    fieldsets = (
        (None, {
            'fields': ('prefix', 'given_name', 'middle_name', 'family_name', 'suffix', 'org_name', 'creator_type', 'name_variants')
        }),
        ('Birth / Death / Activity', {
            'fields': ('birth_city', ('birth_date', 'birth_date_precision', 'birth_date_BC'), 'death_city',
                       ('death_date', 'death_date_precision', 'death_date_BC'), ('earliest_active', 'earliest_active_precision', 'earliest_active_BC'),
                       ('latest_active', 'latest_active_precision', 'latest_active_BC'))
        }),
        ('Details', {
            'fields': ('gender', 'nationality', 'headquarter_city', 'biography', 'website', 'photo',
                       'primary_publications', 'secondary_publications',
                       #'primary_bibliography', 'secondary_bibliography',
                       'awards_text', 'biblio_text', 'biblio_text_es', 'secondary_biblio_text', 'secondary_biblio_text_es')
        }),
        ('Standard fields', {
            'fields': ('notes', 'attention', 'needs_editing', 'published', 'profiler_name', 'profiler_entry_date', 'tags')
        })
    )
    
    def __init__(self, model, admin_site):
        super(CreatorAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': (("%s%s" % (STATIC_URL, 'css/tabbed_translation_fields.css')),
                    ("%s%s" % (STATIC_URL, 'css/iconic.css')),
                    ("%s%s" % (STATIC_URL, 'css/admin_form.css'))
                   )
        }
        js = (
            ("%s%s" % (STATIC_URL, 'js/tiny_mce/tiny_mce.js')),
            ("%s%s" % (STATIC_URL, 'js/textareas.js')),
            ("%s%s" % (STATIC_URL, 'js/scripts.js')),
            ("%s%s" % (STATIC_URL, 'js/tabbed_translation_fields.js')),
            ("%s%s" % (STATIC_URL, 'js/admin_form.js'))
        )

"""
class BibliographicRecordAdmin(admin.ModelAdmin):
    form = arcforms.BibliographicRecordAdminForm
    
    def __init__(self, model, admin_site):
        super(BibliographicRecordAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )
"""

class LocationAdmin(TranslationAdmin):
    form = arcforms.LocationAdminForm
    list_display = ('title', 'begin_date_display', 'end_date_display', 'city', 'state', 'country', 'has_system_links',)
    search_fields = ['title_ascii', 'title', 'title_variants', 'city__name', 'state', 'summary', 'notes']
    inlines = (StageInline,)
    list_filter = ('has_attention',)
    fieldsets = (
        (None, {
            'fields': ('title', 'title_variants', 'country', 'venue_type')
        }),
        ('Begin/end dates', {
            'fields': (('begin_date', 'begin_date_precision', 'begin_date_BC'), ('end_date', 'end_date_precision', 'end_date_BC'))
        }),
        ('Address', {
            'fields': ('address', 'address2', 'city', 'state', 'postal_code')
        }),
        ('Geolocation', {
            'fields': ('lat', 'lon', 'altitude')    
        }),
        ('Further details', {
            'fields': ('summary', 'website', 'photo')
        }),
        ('Standard fields', {
            'fields': ('notes', 'attention', 'needs_editing', 'published', 'profiler_name', 'profiler_entry_date', 'tags')
        })
    )
    
    def __init__(self, model, admin_site):
        super(LocationAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class StageAdmin(TranslationAdmin):
    form = arcforms.StageAdminForm

    def __init__(self, model, admin_site):
        super(StageAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class WorkRecordAdmin(TranslationAdmin):
    form = arcforms.WorkRecordAdminForm
    inlines = (WorkRecordCreatorInline, RoleInline, RelatedWorkInline,)
    list_display = ('title', 'creators_display', 'work_type', 'has_system_links')
    list_filter = ('work_type', 'lang', 'has_attention',)
    search_fields = ['title', 'subtitle', 'ascii_title', 'title_variants']
    filter_horizontal = ['subject', 'lang']
    fieldsets = (
        ('Titles', {
            'fields': ('title', 'subtitle', 'title_variants')
        }),
        ('Description', {
            'fields': ('work_type', 'lang')
        }),
        ('Creation / Publication', {
            'fields': (('creation_date', 'creation_date_precision', 'creation_date_BC'),
                'primary_publications', 'secondary_publications',
                'performance_rights', )
        }),
        ('Standard fields', {
            'fields': ('summary', 'notes', 'attention', 'needs_editing', 'published', 'profiler_name', 'profiler_entry_date', 'tags')
        })
    )
    
    def __init__(self, model, admin_site):
        super(WorkRecordAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class RoleAdmin(admin.ModelAdmin):
    form = arcforms.RoleAdminForm
    ordering = ('title',)
    
    def __init__(self, model, admin_site):
        super(RoleAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class ProductionAdmin(TranslationAdmin):
    form = arcforms.ProductionAdminForm
    save_as = True
    save_on_top = True
    inlines = (DirectingMemberInline, CastMemberInline, DesignMemberInline, TechMemberInline, ProductionMemberInline, AdvisoryMemberInline,)
    list_display = ('title', 'venue', 'stage', 'display_directors', 'begin_date_display', 'end_date_display', 'has_system_links')
    date_hierarchy = 'begin_date'
    search_fields = ['title', 'ascii_title', 'title_variants', 'notes']
    list_filter = ('has_attention',)
    filter_horizontal = ['source_work', 'theater_companies'] 
    fieldsets = (
        (None, {
            'fields': ('source_work', 'title', 'subtitle', 'title_variants')
        }),
        ('Place and dates', {
            'fields': ('theater_companies', 'venue', 'stage', ('begin_date', 'begin_date_precision', 'begin_date_BC'), ('end_date', 'end_date_precision', 'end_date_BC'),)
        }),
        ('Additional details', {
            'fields': (('is_special_performance', 'special_performance_type'), 'premier', 'website',
                'primary_publications', 'secondary_publications')}),
        ('Plain text information', {
            'fields': (
                'awards_text', 'biblio_text', 'biblio_text_es')
        }),
        ('Standard fields', {
            'fields': ('notes', 'attention', 'needs_editing', 'published', 'profiler_name', 'profiler_entry_date', 'tags')
        })
    )
    
    def __init__(self, model, admin_site):
        super(ProductionAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
     
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
            '/static/js/admin_form.js'
        )

class FestivalAdmin(TranslationAdmin):
    ordering = ['title',]
    search_fields = ['title']

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class FestivalOccurrenceAdmin(TranslationAdmin):
    form = arcforms.FestivalOccurrenceAdminForm
    inlines = (FestivalParticipantInline, )
    date_hierarchy = 'begin_date'
    list_filter = ('has_attention',)
    filter_horizontal = ['primary_publications', 'productions', 'venue']
    search_fields = ['ascii_title', 'title']
    exclude = ('ascii_title',)
    
    fieldsets = (
        (None, {
            'fields': ('festival_series', 'title', 'title_variants', 'productions', 'primary_publications')
        }),
        ('Place and dates', {
            'fields': ('venue', ('begin_date', 'begin_date_precision', 'begin_date_BC'), ('end_date', 'end_date_precision', 'end_date_BC'))
        }),
        ('Standard fields', {
            'fields': (('notes', 'attention', 'needs_editing', 'published', 'profiler_name', 'profiler_entry_date', 'tags'))
        })
    )
    
    def __init__(self, model, admin_site):
        super(FestivalOccurrenceAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css')
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class RepositoryAdmin(TranslationAdmin):
    list_filter = ('has_attention',)
    form = arcforms.RepositoryAdminForm
    search_fields = ['title', 'ascii_title']
    exclude = ('ascii_title',)

    def __init__(self, model, admin_site):
        super(RepositoryAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class CollectionAdmin(TranslationAdmin):
    list_display = ('title', 'repository', 'collection_id')
    list_filter = ('repository', 'has_attention',)
    search_fields = ['title', 'ascii_title']
    exclude = ('ascii_title',)
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class DigitalObjectAdmin(TranslationAdmin):
    form = arcforms.DigitalObjectAdminForm
    inlines = (DigitalObjectRelatedCreatorInline, DigitalFileInline, )
    save_as = True
    save_on_top = True
    search_fields = ['ascii_title', 'title', 'title_variants']
    list_filter = ('has_attention', 'collection', 'digi_object_format', 'restricted', 'ready_to_stream')
    filter_horizontal = ['subject','related_production', 'related_festival', 'related_venue', 'related_work'] #, 'related_award']
    exclude = ('ascii_title',)
    list_display = ('object_number_display', 'title')
    
    fieldsets = (
        ('Basic info', {
            'fields': ('title', 'title_variants', 'collection', 'object_creator', 'language', 'subject', 'rights_holders', 'license_type', 'permission_form')
        },),
        ('Identification', {
            'fields': ('object_id', 'digital_id', 'identifier',)
        },),
        ('Container information', {
            'fields': (('series_num', 'series_name',), ('subseries_num', 'subseries_name',), ('box_num',), ('folder_num', 'folder_name', 'folder_date',),)
        },),
        ('Physical object information', {
            'fields': ('phys_object_type', 'marks', 'measurements', 'donor', 'sponsor_note', ('phys_obj_date', 'phys_obj_precision', 'phys_obj_BC'), 'phys_obj_location')
        },),
        ('Digital object information', {
            'fields': ('digi_object_format', ('creation_date', 'creation_date_precision', 'creation_date_BC'))
        },),
        ('Relationships', {
            'fields': ('related_production', 'related_festival', 'related_venue', 'related_work') #, 'related_award')
        },),
        ('Video settings', {
            'fields': (('restricted', 'restricted_description'), 'ready_to_stream', 'hi_def_video', 'poster_image')
        },),
        ('Standard fields', {
            'fields': ('summary', 'notes', 'attention', 'needs_editing', 'published', ('tags', 'replicate_tags') )
        },),
    )

    def __init__(self, model, admin_site):
        super(DigitalObjectAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    def save_model(self, request, new_object, form, change=False):
        # hook into save_model to work around the m2m widget save issue
        form_col =  form.cleaned_data['collection']
        for field in ['related_production', 'related_festival', 'related_venue', 'related_work']: #, 'related_award']:
            form.cleaned_data[field] = form.cleaned_data[field] or []

        return super(DigitalObjectAdmin, self).save_model(request, new_object, form, change=False)
    
    def save_related(self, request, form, formsets, change):
        
        associate_tags = form.cleaned_data['replicate_tags']
        if associate_tags:
            form_tags =  form.cleaned_data['tags']
            digitalobject_related_production = form.cleaned_data['related_production']
            digitalobject_related_work = form.cleaned_data['related_work']
            for production in  digitalobject_related_production:
                for tag in form_tags:
                    production.tags.add(tag)
            for work_record in  digitalobject_related_work:
                for tag in form_tags:
                    work_record.tags.add(tag)  
        
        return super(DigitalObjectAdmin, self).save_related(request, form, formsets, change)
 
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',
                    '/static/css/admin_form.css'),
            'print': ('/static/css/digitalobject.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class SubjectHeadingAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )



# Enumeration admins
class CountryAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class CityAdmin(TranslationAdmin):
    form = arcforms.CityAdminForm
    
    def __init__(self, model, admin_site):
        super(CityAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class LanguageAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class LicenseAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class AwardAdmin(TranslationAdmin):
    list_display = ('title', 'award_org')
    ordering = ['title']
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class AwardCandidateAdmin(TranslationAdmin):
    form = arcforms.AwardCandidateAdminForm
    search_fields = ['award__title', 'category', 'recipient__creator_name']
    verbose_name = "award nomination / win"
    verbose_name_plural = "award nominations / wins"
    list_filter = ('has_attention', 'year')
    list_display = ('award', 'year', 'category', 'recipient')
    ordering = ['award', '-year']

    def __init__(self, model, admin_site):
        super(AwardCandidateAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/tabbed_translation_fields.js',
        )

class DirectingTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class CastMemberFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class DesignTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class TechTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class ProductionTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class AdvisoryTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )


class OrgFunctionAdmin(TranslationAdmin):
    
    list_filter = ('func_type',)
    list_display = ('title', 'ordinal')
    ordering = ['ordinal']
    
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css', 'static/css/admin_form.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class FestivalFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class WorkRecordFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class PhysicalObjectTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class SpecialPerformanceTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )


class WorkRecordTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class DigitalObjectTypeAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class VenueTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )


class TranslatingFlatPageForm(FlatpageForm):
    class Meta:
        model = TranslatingFlatPage

class TranslatingFlatPageAdmin(FlatPageAdmin, TranslationAdmin):
    form = TranslatingFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'order', 'child_of', 'template_name')}),
    )
    list_display = ('url', 'title', 'child_of')

    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )

class HomePageInfoAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/static/css/tabbed_translation_fields.css',)
        }
        js = (
            '/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js', '/static/js/scripts.js',
            '/static/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/js/tabbed_translation_fields.js',
        )


admin.site.register(Creator, CreatorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(WorkRecord, WorkRecordAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(FestivalOccurrence, FestivalOccurrenceAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(DigitalObject, DigitalObjectAdmin)
admin.site.register(SubjectHeading, SubjectHeadingAdmin)
#admin.site.register(BibliographicRecord, BibliographicRecordAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(AwardCandidate, AwardCandidateAdmin)

admin.site.register(License, LicenseAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(DirectingTeamFunction, DirectingTeamFunctionAdmin)
admin.site.register(CastMemberFunction, CastMemberFunctionAdmin)
admin.site.register(DesignTeamFunction, DesignTeamFunctionAdmin)
admin.site.register(TechTeamFunction, TechTeamFunctionAdmin)
admin.site.register(ProductionTeamFunction, ProductionTeamFunctionAdmin)
admin.site.register(AdvisoryTeamFunction, AdvisoryTeamFunctionAdmin)
admin.site.register(OrgFunction, OrgFunctionAdmin)
admin.site.register(FestivalFunction, FestivalFunctionAdmin)
admin.site.register(WorkRecordFunction, WorkRecordFunctionAdmin)
admin.site.register(PhysicalObjectType, PhysicalObjectTypeAdmin)
admin.site.register(DigitalObjectType, DigitalObjectTypeAdmin)
admin.site.register(WorkRecordType, WorkRecordTypeAdmin)
admin.site.register(VenueType, VenueTypeAdmin)
admin.site.register(SpecialPerformanceType, SpecialPerformanceTypeAdmin)

admin.site.add_action(make_published)
admin.site.add_action(make_unpublished)
# admin.site.add_action(action_clone)

admin.site.unregister(FlatPage)
admin.site.register(TranslatingFlatPage, TranslatingFlatPageAdmin)

admin.site.register(HomePageInfo, HomePageInfoAdmin)
