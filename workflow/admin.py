from archive.models import Creator, Location, Stage, RelatedCreator, WorkRecord, WorkRecordCreator, WorkRecordFunction, Production, Role, DirectingMember, CastMember, DesignMember, TechMember, ProductionMember, DocumentationMember, AdvisoryMember, Festival, FestivalOccurrence, FestivalParticipant, Repository, Collection, DigitalObject, DigitalFile, Award, AwardCandidate, RelatedWork, SubjectHeading, BibliographicRecord, Country, City, Language, DirectingTeamFunction, CastMemberFunction, DesignTeamFunction, TechTeamFunction, ProductionTeamFunction, DocumentationTeamFunction, AdvisoryTeamFunction, OrgFunction, FestivalFunction, PhysicalObjectType, WorkRecordType, VenueType
from workflow.models import Queue, QueueItem
from modeltranslation.admin import TranslationAdmin

from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField

from archive.autocomplete_admin import FkAutocompleteAdmin, InlineAutocompleteAdmin, InlineStackedAutocompleteAdmin
from ajax_select import make_ajax_form

class AutocompleteTranslationAdmin(FkAutocompleteAdmin, TranslationAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AutocompleteTranslationAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

def make_ctda_queue(modeladmin, request, queryset):
    queryset.update(queue=Queue.objects.get(title="CTDA"))
make_ctda_queue.short_description = "Move to CTDA queue"

def make_chc_queue(modeladmin, request, queryset):
    queryset.update(queue=Queue.objects.get(title="CHC"))
make_chc_queue.short_description = "Move to CHC queue"

        
class QueueAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']
    
    class Media:
        css = {
            'all': ('/css/tabbed_translation_fields.css',)
        }
        js = (
            '/js/tiny_mce/tiny_mce.js', '/js/textareas.js', '/js/scripts.js',
            '/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/js/tabbed_translation_fields.js',
        )

class QueueItemAdmin(admin.ModelAdmin):
    list_display = ('object', 'object_number', 'phys_assessed', 'captured', 'post_proc', 'supervisor_qc', 'edited', 'metadata', 'prepped', 'link_to')
    list_editable = ('phys_assessed', 'captured', 'post_proc', 'supervisor_qc', 'edited', 'metadata', 'prepped')
    list_filter = ('high_priority', 'queue')
    ordering = ['-high_priority']
    
    fieldsets = (
        (None, {
            'fields': ('object', 'queue', 'high_priority')
        }),
        ('Status', {
            'fields': ('phys_assessed', 'captured', 'post_proc', 'supervisor_qc', 'edited', 'metadata', 'prepped')
        }),
    )
    class Media:
        css = {
            'all': ('/css/tabbed_translation_fields.css',)
        }
        js = (
            '/js/tiny_mce/tiny_mce.js', '/js/textareas.js', '/js/scripts.js',
            '/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/js/tabbed_translation_fields.js',
        )
        
admin.site.register(Queue, QueueAdmin)
admin.site.register(QueueItem, QueueItemAdmin)

admin.site.add_action(make_ctda_queue)
admin.site.add_action(make_chc_queue)