#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import psycopg2 as Database
    import psycopg2.extensions
except ImportError, e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)


from django.db.backends.postgresql_psycopg2 import base as psqlbase
from django.conf import settings

class DatabaseOperations(psqlbase.DatabaseOperations):
    def lookup_cast(self, lookup_type):
        if lookup_type in('icontains', 'istartswith'):
            return "UPPER(unaccent(%s::text))"
        else:
            return super(DatabaseOperations, self).lookup_cast(lookup_type)

class DatabaseWrapper(psqlbase.DatabaseWrapper):
    
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.server_version = None
        self.features = psqlbase.DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = psqlbase.DatabaseClient(self)
        self.creation = psqlbase.DatabaseCreation(self)
        self.introspection = psqlbase.DatabaseIntrospection(self)
 
        self.operators['icontains'] = 'LIKE UPPER(unaccent(%s))'
        self.operators['istartswith'] = 'LIKE UPPER(unaccent(%s))'
