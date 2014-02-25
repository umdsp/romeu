# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Type'
        db.create_table(u'publications_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('bibtex_types', self.gf('django.db.models.fields.CharField')(default='article', max_length=256)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('publications', ['Type'])

        # Adding model 'Publication'
        db.create_table(u'publications_publication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Type'])),
            ('annote', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('citekey', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('book_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('how_published', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=4)),
            ('month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('table_of_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('translator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series_num', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('access_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('art_size', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('runtime', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('archive_location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('university', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('library', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('library_catalog_num', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('publications', ['Publication'])

        # Adding model 'CustomLink'
        db.create_table(u'publications_customlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Publication'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('publications', ['CustomLink'])

        # Adding model 'CustomFile'
        db.create_table(u'publications_customfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['publications.Publication'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('publications', ['CustomFile'])


    def backwards(self, orm):
        # Deleting model 'Type'
        db.delete_table(u'publications_type')

        # Deleting model 'Publication'
        db.delete_table(u'publications_publication')

        # Deleting model 'CustomLink'
        db.delete_table(u'publications_customlink')

        # Deleting model 'CustomFile'
        db.delete_table(u'publications_customfile')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'publications.customfile': {
            'Meta': {'object_name': 'CustomFile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Publication']"})
        },
        'publications.customlink': {
            'Meta': {'object_name': 'CustomLink'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Publication']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'publications.publication': {
            'Meta': {'ordering': "['-year', '-month', '-id']", 'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'annote': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'archive_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'art_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'book_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'citekey': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'how_published': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'library': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'library_catalog_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'series_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'table_of_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'translator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Type']"}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'publications.type': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Type'},
            'bibtex_types': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '256'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['publications']