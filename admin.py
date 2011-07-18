from django.contrib import admin

from datatrans.models import KeyValue


class KeyValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'language', 'edited', 'fuzzy')
    ordering = ('digest', 'language')
    search_fields = ('value',)
    list_filter = ('language', 'edited', 'fuzzy')

admin.site.register(KeyValue, KeyValueAdmin)
