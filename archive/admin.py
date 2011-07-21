from archive.models import Creator, Location, Stage, RelatedCreator, WorkRecord, WorkRecordCreator, WorkRecordFunction, Production, Role, DirectingMember, CastMember, DesignMember, TechMember, ProductionMember, DocumentationMember, AdvisoryMember, Festival, FestivalOccurrence, FestivalParticipant, Repository, Collection, DigitalObject, DigitalFile, Award, AwardCandidate, RelatedWork, SubjectHeading, BibliographicRecord, Country, City, Language, DirectingTeamFunction, CastMemberFunction, DesignTeamFunction, TechTeamFunction, ProductionTeamFunction, DocumentationTeamFunction, AdvisoryTeamFunction, OrgFunction, FestivalFunction, PhysicalObjectType, WorkRecordType, VenueType, DigitalObjectType
from modeltranslation.admin import TranslationAdmin

from django.utils.translation import ugettext_lazy as _

from archive.lookups import CreatorLookup, ProductionLookup, LocationLookup, RoleLookup, WorkRecordLookup, CountryLookup, DigitalObjectLookup, CityLookup
from archive import forms as arcforms

from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
# from django.db.models.query import CollectedObjects
from django.db.models.fields.related import ForeignKey, ManyToOneRel
from django.forms.models import model_to_dict
from django.db.models.fields import CharField

from archive.autocomplete_admin import FkAutocompleteAdmin, InlineAutocompleteAdmin, InlineStackedAutocompleteAdmin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add
from reversion.admin import VersionAdmin

import selectable
from selectable import forms as selectable_forms

class AutocompleteTranslationAdmin(FkAutocompleteAdmin, TranslationAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AutocompleteTranslationAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

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

class SuperUltraAdmin(AutocompleteTranslationAdmin, VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(SuperUltraAdmin, self).formfield_for_dbfield(db_field, **kwargs)
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
    extra = 1
    fk_name = 'work_1'
    
    def __init__(self, model, admin_site):
        super(RelatedWorkInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class RelatedCreatorInline(admin.TabularInline):
    form = arcforms.RelatedCreatorAdminForm
    model = RelatedCreator
    extra = 1
    fk_name = 'creator_1'
    
    def __init__(self, model, admin_site):
        super(RelatedCreatorInline, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class WorkRecordCreatorInline(admin.TabularInline):
    form = arcforms.WorkRecordCreatorAdminForm
    model = WorkRecordCreator
    extra = 1
    
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
    extra = 1

class DigitalFileInline(admin.TabularInline):
    model = DigitalFile
    extra = 1
    verbose_name = "digital file"
    verbose_name_plural = "digital files"

# ADMIN MODELS
class CreatorAdmin(TranslatingVersioningAdmin):
    form = arcforms.CreatorAdminForm
    list_display = ('creator_name', 'nationality', 'birth_date_display', 'death_date_display', 'has_system_links',)
    list_filter = ('published','has_attention',)
    exclude = ('creator_name',)
    date_hierarchy = 'birth_date'
    search_fields = ['creator_name', 'creator_ascii_name', 'name_variants']
    inlines = (RelatedCreatorInline,)
    filter_horizontal = ['primary_bibliography', 'secondary_bibliography']
    fieldsets = (
        (None, {
            'fields': ('prefix', 'given_name', 'middle_name', 'family_name', 'suffix', 'org_name', 'creator_type', 'name_variants')
        }),
        ('Birth / Death / Activity', {
            'fields': ('birth_location', ('birth_date', 'birth_date_precision', 'birth_date_BC'), 'death_location', ('death_date', 'death_date_precision', 'death_date_BC'), ('earliest_active', 'earliest_active_precision', 'earliest_active_BC'), ('latest_active', 'latest_active_precision', 'latest_active_BC'))
        }),
        ('Details', {
            'fields': ('gender', 'nationality', 'location', 'biography', 'website', 'photo', 'primary_bibliography', 'secondary_bibliography')
        }),
        ('Standard fields', {
            'fields': ('notes', 'attention', 'needs_editing', 'published')
        })
    )
    
    def __init__(self, model, admin_site):
        super(CreatorAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class BibliographicRecordAdmin(FkAutocompleteAdmin):
    related_search_fields = {'work_record': ('ascii_title', 'title', 'title_variants', 'summary')}

    class Media:
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
        )

class LocationAdmin(TranslatingVersioningAdmin):
    form = arcforms.LocationAdminForm
    list_display = ('title', 'address', 'city', 'state', 'country',)
    search_fields = ['title_ascii', 'title', 'title_variants', 'city__name', 'state', 'summary', 'notes']
    inlines = (StageInline,)
    list_filter = ('has_attention',)
    fieldsets = (
        (None, {
            'fields': ('title', 'title_variants', 'country', 'venue_type')
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
            'fields': ('notes', 'attention', 'needs_editing', 'published')
        })
    )
    
    def __init__(self, model, admin_site):
        super(LocationAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class StageAdmin(AutocompleteTranslationAdmin):
    related_search_fields = {'venue': ('title_ascii', 'title', 'title_variants',)}
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class WorkRecordAdmin(TranslatingVersioningAdmin):
    form = arcforms.WorkRecordAdminForm
    inlines = (WorkRecordCreatorInline, RoleInline, RelatedWorkInline,)
    list_display = ('title', 'creators_display', 'work_type', 'genre', 'culture', 'style')
    list_filter = ('work_type', 'lang', 'genre', 'culture', 'style', 'has_attention',)
    search_fields = ['title', 'ascii_title', 'title_variants']
    filter_horizontal = ['subject', 'lang']
    fieldsets = (
        ('Titles', {
            'fields': ('title', 'title_variants')
        }),
        ('Description', {
            'fields': ('work_type', 'subject', 'genre', 'culture', 'style', 'lang')
        }),
        ('Creation / Publication', {
            'fields': (('creation_date', 'creation_date_precision', 'creation_date_BC'), ('publication_date', 'publication_date_precision', 'publication_date_BC'), 'publication_rights', 'performance_rights')
        }),
        ('Access', {
            'fields': ('website', 'digital_copy')
        }),
        ('Standard fields', {
            'fields': ('summary', 'notes', 'attention', 'needs_editing', 'published')
        })
    )
    
    def __init__(self, model, admin_site):
        super(WorkRecordAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class RoleAdmin(admin.ModelAdmin):
    form = arcforms.RoleAdminForm
    ordering = ('title',)
    
    def __init__(self, model, admin_site):
        super(RoleAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

class ProductionAdmin(TranslatingVersioningAdmin):
    form = arcforms.ProductionAdminForm
    inlines = (DirectingMemberInline, CastMemberInline, DesignMemberInline, TechMemberInline, ProductionMemberInline,)
    list_display = ('title', 'venue', 'begin_date_display', 'end_date_display',)
    date_hierarchy = 'begin_date'
    search_fields = ['title', 'ascii_title', 'title_variants', 'notes']
    list_filter = ('has_attention',)
    filter_horizontal = ['source_work', 'secondary_bibliography',]
    fieldsets = (
        (None, {
            'fields': ('source_work', 'title', 'subtitle', 'title_variants')
        }),
        ('Place and dates', {
            'fields': ('theater_company', 'venue', 'stage', ('begin_date', 'begin_date_precision', 'begin_date_BC'), ('end_date', 'end_date_precision', 'end_date_BC'),)
        }),
        ('Additional details', {
            'fields': (('is_special_performance', 'special_performance_type'), 'premier', 'website', 'secondary_bibliography')
        }),
        ('Standard fields', {
            'fields': ('notes', 'attention', 'needs_editing', 'published')
        })
    )
    
    def __init__(self, model, admin_site):
        super(ProductionAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
     
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class FestivalAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class FestivalOccurrenceAdmin(TranslatingVersioningAdmin):
    form = arcforms.FestivalOccurrenceAdminForm
    inlines = (FestivalParticipantInline,)
    date_hierarchy = 'begin_date'
    list_filter = ('has_attention',)
    filter_horizontal = ['productions', 'secondary_bibliography']
    
    fieldsets = (
        (None, {
            'fields': ('festival_series', 'title', 'title_variants', 'productions', 'secondary_bibliography')
        }),
        ('Place and dates', {
            'fields': ('venue', ('begin_date', 'begin_date_precision', 'begin_date_BC'), ('end_date', 'end_date_precision', 'end_date_BC'))
        }),
        ('Standard fields', {
            'fields': (('notes', 'attention', 'needs_editing', 'published'))
        })
    )
    
    def __init__(self, model, admin_site):
        super(FestivalOccurrenceAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class RepositoryAdmin(TranslationAdmin):
    list_filter = ('has_attention',)
    form = arcforms.RepositoryAdminForm
    
    def __init__(self, model, admin_site):
        super(RepositoryAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class CollectionAdmin(TranslationAdmin):
    list_display = ('title', 'repository', 'collection_id')
    list_filter = ('repository', 'has_attention',)
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class DigitalObjectAdmin(TranslatingVersioningAdmin):
    form = arcforms.DigitalObjectAdminForm
    inlines = (DigitalFileInline,)
    search_fields = ['title', 'title_variants']
    list_filter = ('has_attention', 'collection',)
    filter_horizontal = ['subject', 'related_production', 'related_festival', 'related_creator', 'related_venue', 'related_work']
    fieldsets = (
        ('Basic info', {
            'fields': ('title', 'title_variants', 'collection', 'object_creator', 'language', 'subject', 'rights', 'copyright')
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
            'fields': ('related_production', 'related_festival', 'related_venue', 'related_creator', 'related_work',)
        },),
        ('Standard fields', {
            'fields': ('summary', 'notes', 'attention', 'needs_editing', 'published',)
        },),
    )

    def __init__(self, model, admin_site):
        super(DigitalObjectAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site

    def save_model(self, request, new_object, form, change=False):
        # hook into save_model to work around the m2m widget save issue
        for field in ['related_creator', 'related_production', 'related_festival', 'related_venue', 'related_work']:
            form.cleaned_data[field] = form.cleaned_data[field] or []
        return super(DigitalObjectAdmin, self).save_model(request, new_object, form, change=False)

    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',),
            'print': ('/media/css/digitalobject.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class SubjectHeadingAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )



# Enumeration admins
class CountryAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class CityAdmin(TranslationAdmin):
    form = arcforms.CityAdminForm
    
    def __init__(self, model, admin_site):
        super(CityAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site
    
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css', '/static/css/iconic.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/tabbed_translation_fields.js',
        )

class LanguageAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class AwardAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class AwardCandidateAdmin(AutocompleteTranslationAdmin):
    related_search_fields = {'award': ('title',), 'recipient': ('creator_name', 'name_variants'), 'production': ('ascii_title', 'title', 'title_variants'), 'place': ('title_ascii', 'title', 'title_variants'), 'festival': ('title', 'title_variants'), 'work_record': ('ascii_title', 'title', 'title_variants')}
    verbose_name = "award nomination / win"
    verbose_name_plural = "award nominations / wins"
    list_filter = ('has_attention',)
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class DirectingTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class CastMemberFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class DesignTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class TechTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class ProductionTeamFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class OrgFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class FestivalFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class WorkRecordFunctionAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class PhysicalObjectTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class WorkRecordTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class DigitalObjectTypeAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
        )

class VenueTypeAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('/media/css/tabbed_translation_fields.css',)
        }
        js = (
            '/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js', '/media/js/scripts.js',
            '/media/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/media/js/tabbed_translation_fields.js',
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
admin.site.register(BibliographicRecord, BibliographicRecordAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(AwardCandidate, AwardCandidateAdmin)

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(DirectingTeamFunction, DirectingTeamFunctionAdmin)
admin.site.register(CastMemberFunction, CastMemberFunctionAdmin)
admin.site.register(DesignTeamFunction, DesignTeamFunctionAdmin)
admin.site.register(TechTeamFunction, TechTeamFunctionAdmin)
admin.site.register(ProductionTeamFunction, ProductionTeamFunctionAdmin)
admin.site.register(OrgFunction, OrgFunctionAdmin)
admin.site.register(FestivalFunction, FestivalFunctionAdmin)
admin.site.register(WorkRecordFunction, WorkRecordFunctionAdmin)
admin.site.register(PhysicalObjectType, PhysicalObjectTypeAdmin)
admin.site.register(DigitalObjectType, DigitalObjectTypeAdmin)
admin.site.register(WorkRecordType, WorkRecordTypeAdmin)
admin.site.register(VenueType, VenueTypeAdmin)

admin.site.add_action(make_published)
admin.site.add_action(make_unpublished)
# admin.site.add_action(action_clone)