# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Production.tags'
        db.add_column('archive_production', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)

        # Adding field 'Location.tags'
        db.add_column('archive_location', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)

        # Adding field 'Stage.tags'
        db.add_column('archive_stage', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)

        # Adding field 'BibliographicRecord.tags'
        db.add_column('archive_bibliographicrecord', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)

        # Adding field 'DigitalObject.tags'
        db.add_column('archive_digitalobject', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)


        # Changing field 'DigitalObject.marks'
        db.alter_column('archive_digitalobject', 'marks', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True))
        # Adding field 'Creator.tags'
        db.add_column('archive_creator', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)

        # Adding field 'WorkRecord.tags'
        db.add_column('archive_workrecord', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)


        # Changing field 'WorkRecord.performance_rights_es'
        db.alter_column('archive_workrecord', 'performance_rights_es', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'WorkRecord.performance_rights_en'
        db.alter_column('archive_workrecord', 'performance_rights_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'WorkRecord.performance_rights'
        db.alter_column('archive_workrecord', 'performance_rights', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'WorkRecord.publication_rights_es'
        db.alter_column('archive_workrecord', 'publication_rights_es', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'WorkRecord.publication_rights_en'
        db.alter_column('archive_workrecord', 'publication_rights_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'WorkRecord.publication_rights'
        db.alter_column('archive_workrecord', 'publication_rights', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Adding field 'FestivalOccurrence.tags'
        db.add_column('archive_festivaloccurrence', 'tags',
                      self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Production.tags'
        db.delete_column('archive_production', 'tags')

        # Deleting field 'Location.tags'
        db.delete_column('archive_location', 'tags')

        # Deleting field 'Stage.tags'
        db.delete_column('archive_stage', 'tags')

        # Deleting field 'BibliographicRecord.tags'
        db.delete_column('archive_bibliographicrecord', 'tags')

        # Deleting field 'DigitalObject.tags'
        db.delete_column('archive_digitalobject', 'tags')


        # Changing field 'DigitalObject.marks'
        db.alter_column('archive_digitalobject', 'marks', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
        # Deleting field 'Creator.tags'
        db.delete_column('archive_creator', 'tags')

        # Deleting field 'WorkRecord.tags'
        db.delete_column('archive_workrecord', 'tags')


        # Changing field 'WorkRecord.performance_rights_es'
        db.alter_column('archive_workrecord', 'performance_rights_es', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'WorkRecord.performance_rights_en'
        db.alter_column('archive_workrecord', 'performance_rights_en', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'WorkRecord.performance_rights'
        db.alter_column('archive_workrecord', 'performance_rights', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'WorkRecord.publication_rights_es'
        db.alter_column('archive_workrecord', 'publication_rights_es', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'WorkRecord.publication_rights_en'
        db.alter_column('archive_workrecord', 'publication_rights_en', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'WorkRecord.publication_rights'
        db.alter_column('archive_workrecord', 'publication_rights', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))
        # Deleting field 'FestivalOccurrence.tags'
        db.delete_column('archive_festivaloccurrence', 'tags')


    models = {
        'archive.advisorymember': {
            'Meta': {'object_name': 'AdvisoryMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.AdvisoryTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.advisoryteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'AdvisoryTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.award': {
            'Meta': {'object_name': 'Award'},
            'award_org': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.awardcandidate': {
            'Meta': {'object_name': 'AwardCandidate'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Award']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_en': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_es': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Production']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.WorkRecord']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'archive.bibliographicrecord': {
            'Meta': {'object_name': 'BibliographicRecord'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_date': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'archive_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'art_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bib_type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'booktitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'issue_num': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'library': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'library_catalog_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_pages': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'num_volumes': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'publication': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'series_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'translator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecord']", 'null': 'True', 'blank': 'True'})
        },
        'archive.bibliographicrecordtype': {
            'Meta': {'object_name': 'BibliographicRecordType'},
            'has_abstract': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_author': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_booktitle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_chapter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_edition': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_editor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_issue_num': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_month': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_num_volumes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_pages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_publisher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_pubtitle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_series': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_shorttitle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_translator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_volume': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_workrecord': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_year': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.castmember': {
            'Meta': {'object_name': 'CastMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.CastMemberFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Role']", 'null': 'True', 'blank': 'True'})
        },
        'archive.castmemberfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'CastMemberFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['archive.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.collection': {
            'Meta': {'object_name': 'Collection'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection_id': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collections'", 'to': "orm['archive.Repository']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'demonym': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'demonym_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'demonym_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.creator': {
            'Meta': {'ordering': "['creator_name']", 'object_name': 'Creator'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'birth_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'born_here'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'creator_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_type': ('django.db.models.fields.CharField', [], {'default': "u'person'", 'max_length': '10'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'death_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'death_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'died_here'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'earliest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'earliest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'earliest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '2'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'latest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_variants': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Country']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.RelatedCreator']", 'blank': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.designmember': {
            'Meta': {'object_name': 'DesignMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DesignTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.designteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DesignTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalfile': {
            'Meta': {'object_name': 'DigitalFile'},
            'digital_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['archive.DigitalObject']"}),
            'filepath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seq_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalobject': {
            'Meta': {'object_name': 'DigitalObject'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'box_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': "orm['archive.Collection']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'digi_object_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObjectType']", 'null': 'True', 'blank': 'True'}),
            'digital_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'folder_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hi_def_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Language']"}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['archive.License']"}),
            'marks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'measurements': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objects_created'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'permission_form': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phys_obj_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phys_obj_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phys_obj_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'phys_obj_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'phys_object_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'digital_objects'", 'null': 'True', 'to': "orm['archive.PhysicalObjectType']"}),
            'poster_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ready_to_stream': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_creator': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Creator']"}),
            'related_festival': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.FestivalOccurrence']"}),
            'related_production': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Production']"}),
            'related_venue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Location']"}),
            'related_work': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restricted_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights_holders': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sponsor_note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collection_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'subseries_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subseries_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalobjecttype': {
            'Meta': {'object_name': 'DigitalObjectType'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'archive.directingmember': {
            'Meta': {'object_name': 'DirectingMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DirectingTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.directingteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DirectingTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.documentationmember': {
            'Meta': {'object_name': 'DocumentationMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DocumentationTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.documentationteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DocumentationTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.festival': {
            'Meta': {'object_name': 'Festival'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivalfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'FestivalFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivaloccurrence': {
            'Meta': {'object_name': 'FestivalOccurrence'},
            'announcement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'edu_program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'festival_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.FestivalParticipant']", 'blank': 'True'}),
            'productions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Production']", 'symmetrical': 'False'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'festival_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Location']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivalparticipant': {
            'Meta': {'object_name': 'FestivalParticipant'},
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalOccurrence']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"})
        },
        'archive.homepageinfo': {
            'Meta': {'object_name': 'HomePageInfo'},
            'box_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_3_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_boxes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'archive.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'archival_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'shortcode': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'archive.license': {
            'Meta': {'object_name': 'License'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'more_info_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'archive.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Country']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_venue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['archive.DigitalObject']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_ascii': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'venue_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.VenueType']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.orgfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'OrgFunction'},
            'func_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.physicalobjecttype': {
            'Meta': {'ordering': "['title']", 'object_name': 'PhysicalObjectType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.production': {
            'Meta': {'object_name': 'Production'},
            'advisory_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advisory_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.AdvisoryMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cast_member_for'", 'symmetrical': 'False', 'through': "orm['archive.CastMember']", 'to': "orm['archive.Creator']"}),
            'design_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'design_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DesignMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'directing_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'directing_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DirectingMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'documentation_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documentation_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DocumentationMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_special_performance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_performances': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'premier': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'production_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'production_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.ProductionMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'productions_related_to'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Creator']"}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'production_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'source_work': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'performances'", 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'special_performance_type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Stage']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'technical_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'technical_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.TechMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'theater_company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_productions'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productions'", 'to': "orm['archive.Location']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.productionmember': {
            'Meta': {'object_name': 'ProductionMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.ProductionTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.productionteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'ProductionTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.relatedcreator': {
            'Meta': {'object_name': 'RelatedCreator'},
            'first_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_creator_to'", 'to': "orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.OrgFunction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'relationship_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_since_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_since_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'relationship_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_until_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_until_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'second_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_creator_to'", 'to': "orm['archive.Creator']"})
        },
        'archive.relatedwork': {
            'Meta': {'object_name': 'RelatedWork'},
            'first_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_work_to'", 'to': "orm['archive.WorkRecord']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'second_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_work_to'", 'to': "orm['archive.WorkRecord']"})
        },
        'archive.repository': {
            'Meta': {'object_name': 'Repository'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']"}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'repository_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_text': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['archive.WorkRecord']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'archive.stage': {
            'Meta': {'object_name': 'Stage'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seating': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'square_footage': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_depth': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_lighting': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_lighting_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_lighting_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'stage_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': "orm['archive.Location']"})
        },
        'archive.subjectheading': {
            'Meta': {'object_name': 'SubjectHeading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_subjects'", 'null': 'True', 'to': "orm['archive.SubjectHeading']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headings'", 'to': "orm['archive.SubjectSource']"}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.subjectsource': {
            'Meta': {'object_name': 'SubjectSource'},
            'ead_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.techmember': {
            'Meta': {'object_name': 'TechMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.TechTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.techteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'TechTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.translatingflatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'TranslatingFlatPage', '_ormbases': ['flatpages.FlatPage']},
            'child_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'flatpage_parent'", 'null': 'True', 'blank': 'True', 'to': "orm['archive.TranslatingFlatPage']"}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.venuetype': {
            'Meta': {'ordering': "['title']", 'object_name': 'VenueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.workculture': {
            'Meta': {'object_name': 'WorkCulture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.workgenre': {
            'Meta': {'object_name': 'WorkGenre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.workrecord': {
            'Meta': {'object_name': 'WorkRecord'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Creator']", 'through': "orm['archive.WorkRecordCreator']", 'symmetrical': 'False'}),
            'creators_display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'culture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkCulture']", 'null': 'True', 'blank': 'True'}),
            'digital_copy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkGenre']", 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Language']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performance_rights': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'performance_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'performance_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'publication_rights': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_works': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'to': "orm['archive.WorkRecord']", 'through': "orm['archive.RelatedWork']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkStyle']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'works'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecordType']"})
        },
        'archive.workrecordcreator': {
            'Meta': {'object_name': 'WorkRecordCreator'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecordFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecord']"})
        },
        'archive.workrecordfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'WorkRecordFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.workrecordtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WorkRecordType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.workstyle': {
            'Meta': {'object_name': 'WorkStyle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage', 'db_table': "'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['archive']