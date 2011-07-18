from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db import models
from django.utils import translation
from django.utils.datastructures import SortedDict

from datatrans.models import KeyValue, make_digest

'''
REGISTRY is a dict containing the registered models and their translation fields as a dict.
Example:

>>> from blog.models import Entry
>>> from datatrans.utils import *
>>> class EntryTranslation(object):
...     fields = ('title', 'body',)
...
>>> register(Entry, EntryTranslation)
>>> REGISTRY
{<class 'blog.models.Entry'>: {'body': <django.db.models.fields.TextField object at 0x911368c>,
                               'title': <django.db.models.fields.CharField object at 0x911346c>}}
'''
REGISTRY = SortedDict()

def get_registry():
    return REGISTRY

def get_default_language():
    # Get the source language code if specified, or else just the default language code.
    lang = getattr(settings, 'SOURCE_LANGUAGE_CODE', settings.LANGUAGE_CODE)
    default = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(default) == 0:
        # when not found, take first part ('en' instead of 'en-us')
        lang = lang.split('-')[0]
        default = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(default) == 0:
        raise ImproperlyConfigured("The [SOURCE_]LANGUAGE_CODE '%s' is not found in your LANGUAGES setting." % lang)
    return default[0]

def get_current_language():
    lang = translation.get_language()
    current = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(current) == 0:
        lang = lang.split('-')[0]
        current = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(current) == 0:
        raise ImproperlyConfigured("The current language '%s' is not found in your LANGUAGES setting." % lang)
    return current[0]

class FieldDescriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        lang_code = get_current_language()
        key = instance.__dict__[self.name]
        if len(key) == 0:
            return u''
        return KeyValue.objects.lookup(key, lang_code)

    def __set__(self, instance, value):
        lang_code = get_current_language()
        default_lang = get_default_language()

        if lang_code == default_lang or not self.name in instance.__dict__:
            instance.__dict__[self.name] = value
        else:
            original = instance.__dict__[self.name]
            if original == u'':
                instance.__dict__[self.name] = value
                original = value

            kv = KeyValue.objects.get_keyvalue(original, lang_code)
            kv.value = value
            kv.edited = True
            kv.save()

        return None


def _pre_save(sender, instance, **kwargs):
    setattr(instance, 'datatrans_old_language', get_current_language())
    default_lang = get_default_language()
    translation.activate(default_lang)

    # When we edit a registered model, update the original translations and mark them as unedited (to do)
    if instance.pk is not None:
        try:
            # Just because instance.pk is set, it does not mean that the instance
            # is saved. Most typical/important ex: loading fixtures
            original = sender.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            return None

        register = get_registry()
        fields = register[sender].values()
        for field in fields:
            old_digest = make_digest(original.__dict__[field.name])
            new_digest = make_digest(instance.__dict__[field.name])
            # If changed, update keyvalues
            if old_digest != new_digest:
                # Check if the new value already exists, if not, create a new one. The old one will be obsoleted.
                if KeyValue.objects.filter(digest=new_digest).count() == 0:
                    kvs = KeyValue.objects.filter(digest=old_digest)
                    for kv in kvs:
                        new_value = instance.__dict__[field.name] if kv.language == default_lang else kv.value
                        new_kv = KeyValue(digest=new_digest, language=kv.language, edited=kv.edited, fuzzy=True, value=new_value)
                        new_kv.save()


def _post_save(sender, instance, created, **kwargs):
    translation.activate(getattr(instance, 'datatrans_old_language', get_default_language()))

def register(model, modeltranslation):
    '''
    modeltranslation must be a class with the following attribute:

    fields = ('field1', 'field2', ...)

    For example:

    class BlogPostTranslation(object):
        fields = ('title', 'content',)

    '''

    if not model in REGISTRY:
        # create a fields dict (models apparently lack this?!)
        fields = dict([(f.name, f) for f in model._meta._fields() if f.name in modeltranslation.fields])

        REGISTRY[model] = fields
        models.signals.pre_save.connect(_pre_save, sender=model)
        models.signals.post_save.connect(_post_save, sender=model)

        for field in fields.values():
            setattr(model, field.name, FieldDescriptor(field.name))


def make_messages(build_digest_list=False):
    '''
    This function loops over all the registered models and, when necessary,
    creates KeyValue entries for the fields specified.

    When build_digest_list is True, a list of digests will be created
    for all the translatable data. When it is False, it will return
    the number of processed objects.
    '''
    object_count = 0
    digest_list = []

    for model in REGISTRY:
        fields = REGISTRY[model].values()
        objects = model.objects.all()
        for object in objects:
            for field in fields:
                for lang_code, lang_human in settings.LANGUAGES:
                    value = object.__dict__[field.name]
                    if build_digest_list:
                        digest_list.append(make_digest(value))
                    KeyValue.objects.lookup(value, lang_code)
            object_count += 1

    if build_digest_list:
        return digest_list
    else:
        return object_count

def find_obsoletes():
    digest_list = make_messages(build_digest_list=True)
    obsoletes = KeyValue.objects.exclude(digest__in=digest_list)
    return obsoletes

