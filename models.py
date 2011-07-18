from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import signals
from django.db.models.query import QuerySet

from hashlib import sha1

def make_digest(key):
    return sha1(key.encode('utf-8')).hexdigest()

def _get_cache_keys(self):
    return ('datatrans_%s_%s' % (self.language, self.digest),
            'datatrans_%s' % self.id)

CACHE_DURATION = getattr(settings, 'DATATRANS_CACHE_DURATION', 60 * 60) # cache for an hour

class KeyValueManager(models.Manager):
    def get_query_set(self):
        return KeyValueQuerySet(self.model)

    def get_keyvalue(self, key, language):
        digest = make_digest(key)
        keyvalue, created = self.get_or_create(digest=digest, language=language, defaults={'value': key})
        return keyvalue

    def lookup(self, key, language):
        kv = self.get_keyvalue(key, language)
        if kv.edited:
            return kv.value
        else:
            return key

    def for_model(self, model, fields, modelfield=None):
        '''
        Get KeyValues for a model. The fields argument is a list of model fields.
        If modelfield is specified, only KeyValue entries for that field will be returned.
        '''
        objects = model.objects.all()
        digests = []

        for object in objects:
            if modelfield is None:
                for field in fields:
                    digests.append(make_digest(object.__dict__[field.name]))
            else:
                digests.append(make_digest(object.__dict__[modelfield]))

        return self.filter(digest__in=digests)

    def contribute_to_class(self, model, name):
        signals.post_save.connect(self._post_save, sender=model)
        signals.post_delete.connect(self._post_delete, sender=model)
        setattr(model, '_get_cache_keys', _get_cache_keys)
        setattr(model, 'cache_keys', property(_get_cache_keys))
        return super(KeyValueManager, self).contribute_to_class(model, name)

    def _invalidate_cache(self, instance):
        '''
        Explicitly set a None value instead of just deleting so we don't have
        any race conditions where.
        '''
        for key in instance.cache_keys:
            cache.set(key, None, 5)

    def _post_save(self, instance, **kwargs):
        self._invalidate_cache(instance)

    def _post_delete(self, instance, **kwargs):
        self._invalidate_cache(instance)


class KeyValueQuerySet(QuerySet):
    def iterator(self):
        superiter = super(KeyValueQuerySet, self).iterator()
        while True:
            obj = superiter.next()
            # Use cache.add instead of cache.set to prevent race conditions
            for key in obj.cache_keys:
                cache.add(key, obj, CACHE_DURATION)
            yield obj

    def get(self, *args, **kwargs):
        '''
        Checks the cache to see if there's a cached entry for this pk. If not, fetches
        using super then stores the result in cache.

        Most of the logic here was gathered from a careful reading of
        ``django.db.models.sql.query.add_filter``
        '''
        if self.query.where:
            # If there is any other ``where`` filter on this QuerySet just call
            # super. There will be a where clause if this QuerySet has already
            # been filtered/cloned.
            return super(KeyValueQuerySet, self).get(*args, **kwargs)

        # Punt on anything more complicated than get by pk/id only...
        if len(kwargs) == 1:
            k = kwargs.keys()[0]
            if k in ('pk', 'pk__exact', 'id', 'id__exact'):
                obj = cache.get('datatrans_%s' % kwargs.values()[0])
                if obj is not None:
                    return obj
        elif 'digest' in kwargs and 'language' in kwargs:
            obj = cache.get('datatrans_%s_%s' % (kwargs['language'], kwargs['digest']))
            if obj is not None:
                return obj

        # Calls self.iterator to fetch objects, storing object in cache.
        return super(KeyValueQuerySet, self).get(*args, **kwargs)


class KeyValue(models.Model):
    digest = models.CharField(max_length=40, db_index=True)
    language = models.CharField(max_length=5, db_index=True, choices=settings.LANGUAGES)
    value = models.TextField(blank=True)
    edited = models.BooleanField(blank=True, default=False)
    fuzzy = models.BooleanField(blank=True, default=False)

    objects = KeyValueManager()

    def __unicode__(self):
        return u'%s: %s' % (self.language, self.value)


