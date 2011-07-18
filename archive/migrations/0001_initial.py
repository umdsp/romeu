# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SubjectSource'
        db.create_table('archive_subjectsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ead_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('archive', ['SubjectSource'])

        # Adding model 'SubjectHeading'
        db.create_table('archive_subjectheading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='headings', to=orm['archive.SubjectSource'])),
            ('parent_subject', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child_subjects', null=True, to=orm['archive.SubjectHeading'])),
        ))
        db.send_create_signal('archive', ['SubjectHeading'])

        # Adding model 'Creator'
        db.create_table('archive_creator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator_type', self.gf('django.db.models.fields.CharField')(default=u'person', max_length=10)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('given_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('org_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('creator_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creator_ascii_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_variants', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('birth_location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='born_here', null=True, to=orm['archive.Location'])),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birth_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1, null=True, blank=True)),
            ('birth_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('death_location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='died_here', null=True, to=orm['archive.Location'])),
            ('death_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1, null=True, blank=True)),
            ('death_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('earliest_active', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('earliest_active_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('earliest_active_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('latest_active', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('latest_active_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('latest_active_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gender', self.gf('django.db.models.fields.CharField')(default=u'N', max_length=2)),
            ('nationality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Country'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'], null=True, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('biography_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('biography_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DigitalObject'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['Creator'])

        # Adding M2M table for field primary_bibliography on 'Creator'
        db.create_table('archive_creator_primary_bibliography', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique('archive_creator_primary_bibliography', ['creator_id', 'bibliographicrecord_id'])

        # Adding M2M table for field secondary_bibliography on 'Creator'
        db.create_table('archive_creator_secondary_bibliography', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique('archive_creator_secondary_bibliography', ['creator_id', 'bibliographicrecord_id'])

        # Adding model 'RelatedCreator'
        db.create_table('archive_relatedcreator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator_1', to=orm['archive.Creator'])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('creator_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator_2', to=orm['archive.Creator'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.OrgFunction'], null=True, blank=True)),
            ('relationship_since', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('relationship_since_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('relationship_since_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('relationship_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('relationship_until_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('relationship_until_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['RelatedCreator'])

        # Adding model 'Location'
        db.create_table('archive_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_ascii', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_venue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('venue_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.VenueType'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.City'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Country'])),
            ('lat', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('altitude', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DigitalObject'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['Location'])

        # Adding model 'Stage'
        db.create_table('archive_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stages', to=orm['archive.Location'])),
            ('square_footage', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('stage_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('stage_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('stage_depth', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('stage_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('stage_lighting', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stage_lighting_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stage_lighting_es', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stage_sound', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stage_sound_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stage_sound_es', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('seating', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Stage'])

        # Adding model 'WorkRecord'
        db.create_table('archive_workrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('ascii_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creators_display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkRecordType'])),
            ('genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkGenre'], null=True, blank=True)),
            ('culture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkCulture'], null=True, blank=True)),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkStyle'], null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('creation_date_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('creation_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publication_rights', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('publication_rights_en', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('publication_rights_es', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('performance_rights', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('performance_rights_en', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('performance_rights_es', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('digital_copy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DigitalObject'], null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['WorkRecord'])

        # Adding M2M table for field subject on 'WorkRecord'
        db.create_table('archive_workrecord_subject', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workrecord', models.ForeignKey(orm['archive.workrecord'], null=False)),
            ('subjectheading', models.ForeignKey(orm['archive.subjectheading'], null=False))
        ))
        db.create_unique('archive_workrecord_subject', ['workrecord_id', 'subjectheading_id'])

        # Adding M2M table for field lang on 'WorkRecord'
        db.create_table('archive_workrecord_lang', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workrecord', models.ForeignKey(orm['archive.workrecord'], null=False)),
            ('language', models.ForeignKey(orm['archive.language'], null=False))
        ))
        db.create_unique('archive_workrecord_lang', ['workrecord_id', 'language_id'])

        # Adding model 'RelatedWork'
        db.create_table('archive_relatedwork', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='text_1', to=orm['archive.WorkRecord'])),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('work_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='text_2', to=orm['archive.WorkRecord'])),
        ))
        db.send_create_signal('archive', ['RelatedWork'])

        # Adding model 'WorkRecordCreator'
        db.create_table('archive_workrecordcreator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('work_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkRecord'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkRecordFunction'])),
        ))
        db.send_create_signal('archive', ['WorkRecordCreator'])

        # Adding model 'Role'
        db.create_table('archive_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_text', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['archive.WorkRecord'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('archive', ['Role'])

        # Adding model 'WorkGenre'
        db.create_table('archive_workgenre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('archive', ['WorkGenre'])

        # Adding model 'WorkCulture'
        db.create_table('archive_workculture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('archive', ['WorkCulture'])

        # Adding model 'WorkStyle'
        db.create_table('archive_workstyle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('archive', ['WorkStyle'])

        # Adding model 'Production'
        db.create_table('archive_production', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ascii_title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Stage'], null=True, blank=True)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('begin_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1)),
            ('begin_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1)),
            ('end_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_performances', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_special_performance', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('special_performance_type', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('premier', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('theater_company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='productions', null=True, to=orm['archive.Creator'])),
        ))
        db.send_create_signal('archive', ['Production'])

        # Adding M2M table for field source_work on 'Production'
        db.create_table('archive_production_source_work', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['archive.production'], null=False)),
            ('workrecord', models.ForeignKey(orm['archive.workrecord'], null=False))
        ))
        db.create_unique('archive_production_source_work', ['production_id', 'workrecord_id'])

        # Adding M2M table for field related_organizations on 'Production'
        db.create_table('archive_production_related_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['archive.production'], null=False)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False))
        ))
        db.create_unique('archive_production_related_organizations', ['production_id', 'creator_id'])

        # Adding M2M table for field secondary_bibliography on 'Production'
        db.create_table('archive_production_secondary_bibliography', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['archive.production'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique('archive_production_secondary_bibliography', ['production_id', 'bibliographicrecord_id'])

        # Adding model 'DirectingMember'
        db.create_table('archive_directingmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DirectingTeamFunction'])),
        ))
        db.send_create_signal('archive', ['DirectingMember'])

        # Adding model 'CastMember'
        db.create_table('archive_castmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.CastMemberFunction'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Role'], null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['CastMember'])

        # Adding model 'DesignMember'
        db.create_table('archive_designmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DesignTeamFunction'])),
        ))
        db.send_create_signal('archive', ['DesignMember'])

        # Adding model 'TechMember'
        db.create_table('archive_techmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.TechTeamFunction'])),
        ))
        db.send_create_signal('archive', ['TechMember'])

        # Adding model 'ProductionMember'
        db.create_table('archive_productionmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.ProductionTeamFunction'])),
        ))
        db.send_create_signal('archive', ['ProductionMember'])

        # Adding model 'DocumentationMember'
        db.create_table('archive_documentationmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DocumentationTeamFunction'])),
        ))
        db.send_create_signal('archive', ['DocumentationMember'])

        # Adding model 'AdvisoryMember'
        db.create_table('archive_advisorymember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Production'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.AdvisoryTeamFunction'])),
        ))
        db.send_create_signal('archive', ['AdvisoryMember'])

        # Adding model 'Festival'
        db.create_table('archive_festival', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Festival'])

        # Adding model 'FestivalOccurrence'
        db.create_table('archive_festivaloccurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('festival_series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Festival'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'])),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('begin_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1)),
            ('begin_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1)),
            ('end_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['FestivalOccurrence'])

        # Adding M2M table for field productions on 'FestivalOccurrence'
        db.create_table('archive_festivaloccurrence_productions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festivaloccurrence', models.ForeignKey(orm['archive.festivaloccurrence'], null=False)),
            ('production', models.ForeignKey(orm['archive.production'], null=False))
        ))
        db.create_unique('archive_festivaloccurrence_productions', ['festivaloccurrence_id', 'production_id'])

        # Adding M2M table for field secondary_bibliography on 'FestivalOccurrence'
        db.create_table('archive_festivaloccurrence_secondary_bibliography', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festivaloccurrence', models.ForeignKey(orm['archive.festivaloccurrence'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique('archive_festivaloccurrence_secondary_bibliography', ['festivaloccurrence_id', 'bibliographicrecord_id'])

        # Adding model 'FestivalParticipant'
        db.create_table('archive_festivalparticipant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Creator'])),
            ('festival', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.FestivalOccurrence'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.FestivalFunction'])),
        ))
        db.send_create_signal('archive', ['FestivalParticipant'])

        # Adding model 'Repository'
        db.create_table('archive_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repository_id', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'])),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['Repository'])

        # Adding model 'Collection'
        db.create_table('archive_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collections', to=orm['archive.Repository'])),
            ('collection_id', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['Collection'])

        # Adding model 'DigitalObject'
        db.create_table('archive_digitalobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_variants', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collection_objects', to=orm['archive.Collection'])),
            ('object_creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='objects_created', null=True, to=orm['archive.Creator'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Language'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('digital_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('marks', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('measurements', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phys_object_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.PhysicalObjectType'], null=True, blank=True)),
            ('donor', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('sponsor_note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('phys_obj_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('phys_obj_precision', self.gf('django.db.models.fields.CharField')(default=u'f', max_length=1, null=True, blank=True)),
            ('phys_obj_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phys_obj_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Location'], null=True, blank=True)),
            ('digi_object_format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.DigitalObjectType'], null=True, blank=True)),
            ('series_num', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('series_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('subseries_num', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('subseries_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('box_num', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('folder_num', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('folder_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('folder_date', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('creation_date_precision', self.gf('django.db.models.fields.CharField')(default=u'y', max_length=1, null=True, blank=True)),
            ('creation_date_BC', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('needs_editing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['DigitalObject'])

        # Adding M2M table for field subject on 'DigitalObject'
        db.create_table('archive_digitalobject_subject', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('subjectheading', models.ForeignKey(orm['archive.subjectheading'], null=False))
        ))
        db.create_unique('archive_digitalobject_subject', ['digitalobject_id', 'subjectheading_id'])

        # Adding M2M table for field related_production on 'DigitalObject'
        db.create_table('archive_digitalobject_related_production', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('production', models.ForeignKey(orm['archive.production'], null=False))
        ))
        db.create_unique('archive_digitalobject_related_production', ['digitalobject_id', 'production_id'])

        # Adding M2M table for field related_festival on 'DigitalObject'
        db.create_table('archive_digitalobject_related_festival', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('festivaloccurrence', models.ForeignKey(orm['archive.festivaloccurrence'], null=False))
        ))
        db.create_unique('archive_digitalobject_related_festival', ['digitalobject_id', 'festivaloccurrence_id'])

        # Adding M2M table for field related_venue on 'DigitalObject'
        db.create_table('archive_digitalobject_related_venue', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('location', models.ForeignKey(orm['archive.location'], null=False))
        ))
        db.create_unique('archive_digitalobject_related_venue', ['digitalobject_id', 'location_id'])

        # Adding M2M table for field related_creator on 'DigitalObject'
        db.create_table('archive_digitalobject_related_creator', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False))
        ))
        db.create_unique('archive_digitalobject_related_creator', ['digitalobject_id', 'creator_id'])

        # Adding M2M table for field related_work on 'DigitalObject'
        db.create_table('archive_digitalobject_related_work', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('digitalobject', models.ForeignKey(orm['archive.digitalobject'], null=False)),
            ('workrecord', models.ForeignKey(orm['archive.workrecord'], null=False))
        ))
        db.create_unique('archive_digitalobject_related_work', ['digitalobject_id', 'workrecord_id'])

        # Adding model 'DigitalObjectType'
        db.create_table('archive_digitalobjecttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('archive', ['DigitalObjectType'])

        # Adding model 'DigitalFile'
        db.create_table('archive_digitalfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filepath', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('seq_id', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('digital_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['archive.DigitalObject'])),
        ))
        db.send_create_signal('archive', ['DigitalFile'])

        # Adding model 'Award'
        db.create_table('archive_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('award_org', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Award'])

        # Adding model 'AwardCandidate'
        db.create_table('archive_awardcandidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Award'])),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=4)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('category_en', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('category_es', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awards', null=True, to=orm['archive.Creator'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awards', null=True, to=orm['archive.Production'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awards', null=True, to=orm['archive.Location'])),
            ('festival', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awards', null=True, to=orm['archive.Festival'])),
            ('work_record', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='awards', null=True, to=orm['archive.WorkRecord'])),
            ('attention', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['AwardCandidate'])

        # Adding model 'Country'
        db.create_table('archive_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('demonym', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('demonym_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('demonym_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['Country'])

        # Adding model 'City'
        db.create_table('archive_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['archive.Country'])),
        ))
        db.send_create_signal('archive', ['City'])

        # Adding model 'Language'
        db.create_table('archive_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('shortcode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('archival_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('archive', ['Language'])

        # Adding model 'WorkRecordType'
        db.create_table('archive_workrecordtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['WorkRecordType'])

        # Adding model 'WorkRecordFunction'
        db.create_table('archive_workrecordfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['WorkRecordFunction'])

        # Adding model 'DirectingTeamFunction'
        db.create_table('archive_directingteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['DirectingTeamFunction'])

        # Adding model 'CastMemberFunction'
        db.create_table('archive_castmemberfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['CastMemberFunction'])

        # Adding model 'DesignTeamFunction'
        db.create_table('archive_designteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['DesignTeamFunction'])

        # Adding model 'TechTeamFunction'
        db.create_table('archive_techteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['TechTeamFunction'])

        # Adding model 'ProductionTeamFunction'
        db.create_table('archive_productionteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['ProductionTeamFunction'])

        # Adding model 'DocumentationTeamFunction'
        db.create_table('archive_documentationteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['DocumentationTeamFunction'])

        # Adding model 'AdvisoryTeamFunction'
        db.create_table('archive_advisoryteamfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['AdvisoryTeamFunction'])

        # Adding model 'OrgFunction'
        db.create_table('archive_orgfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('func_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('archive', ['OrgFunction'])

        # Adding model 'FestivalFunction'
        db.create_table('archive_festivalfunction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['FestivalFunction'])

        # Adding model 'PhysicalObjectType'
        db.create_table('archive_physicalobjecttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['PhysicalObjectType'])

        # Adding model 'VenueType'
        db.create_table('archive_venuetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['VenueType'])

        # Adding model 'BibliographicRecord'
        db.create_table('archive_bibliographicrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bib_type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('booktitle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('publication', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('translator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('num_volumes', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('issue_num', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series_num', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('access_date', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('num_pages', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('art_size', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('runtime', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('archive_location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('university', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('library', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('library_catalog_num', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('work_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkRecord'], null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['BibliographicRecord'])

        # Adding model 'BibliographicRecordType'
        db.create_table('archive_bibliographicrecordtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('has_abstract', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_title', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_shorttitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_booktitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_pubtitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_url', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_author', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_editor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_translator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_volume', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_num_volumes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_issue_num', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_series', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_chapter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_edition', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_month', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_year', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_pages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_publisher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_workrecord', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['BibliographicRecordType'])


    def backwards(self, orm):
        
        # Deleting model 'SubjectSource'
        db.delete_table('archive_subjectsource')

        # Deleting model 'SubjectHeading'
        db.delete_table('archive_subjectheading')

        # Deleting model 'Creator'
        db.delete_table('archive_creator')

        # Removing M2M table for field primary_bibliography on 'Creator'
        db.delete_table('archive_creator_primary_bibliography')

        # Removing M2M table for field secondary_bibliography on 'Creator'
        db.delete_table('archive_creator_secondary_bibliography')

        # Deleting model 'RelatedCreator'
        db.delete_table('archive_relatedcreator')

        # Deleting model 'Location'
        db.delete_table('archive_location')

        # Deleting model 'Stage'
        db.delete_table('archive_stage')

        # Deleting model 'WorkRecord'
        db.delete_table('archive_workrecord')

        # Removing M2M table for field subject on 'WorkRecord'
        db.delete_table('archive_workrecord_subject')

        # Removing M2M table for field lang on 'WorkRecord'
        db.delete_table('archive_workrecord_lang')

        # Deleting model 'RelatedWork'
        db.delete_table('archive_relatedwork')

        # Deleting model 'WorkRecordCreator'
        db.delete_table('archive_workrecordcreator')

        # Deleting model 'Role'
        db.delete_table('archive_role')

        # Deleting model 'WorkGenre'
        db.delete_table('archive_workgenre')

        # Deleting model 'WorkCulture'
        db.delete_table('archive_workculture')

        # Deleting model 'WorkStyle'
        db.delete_table('archive_workstyle')

        # Deleting model 'Production'
        db.delete_table('archive_production')

        # Removing M2M table for field source_work on 'Production'
        db.delete_table('archive_production_source_work')

        # Removing M2M table for field related_organizations on 'Production'
        db.delete_table('archive_production_related_organizations')

        # Removing M2M table for field secondary_bibliography on 'Production'
        db.delete_table('archive_production_secondary_bibliography')

        # Deleting model 'DirectingMember'
        db.delete_table('archive_directingmember')

        # Deleting model 'CastMember'
        db.delete_table('archive_castmember')

        # Deleting model 'DesignMember'
        db.delete_table('archive_designmember')

        # Deleting model 'TechMember'
        db.delete_table('archive_techmember')

        # Deleting model 'ProductionMember'
        db.delete_table('archive_productionmember')

        # Deleting model 'DocumentationMember'
        db.delete_table('archive_documentationmember')

        # Deleting model 'AdvisoryMember'
        db.delete_table('archive_advisorymember')

        # Deleting model 'Festival'
        db.delete_table('archive_festival')

        # Deleting model 'FestivalOccurrence'
        db.delete_table('archive_festivaloccurrence')

        # Removing M2M table for field productions on 'FestivalOccurrence'
        db.delete_table('archive_festivaloccurrence_productions')

        # Removing M2M table for field secondary_bibliography on 'FestivalOccurrence'
        db.delete_table('archive_festivaloccurrence_secondary_bibliography')

        # Deleting model 'FestivalParticipant'
        db.delete_table('archive_festivalparticipant')

        # Deleting model 'Repository'
        db.delete_table('archive_repository')

        # Deleting model 'Collection'
        db.delete_table('archive_collection')

        # Deleting model 'DigitalObject'
        db.delete_table('archive_digitalobject')

        # Removing M2M table for field subject on 'DigitalObject'
        db.delete_table('archive_digitalobject_subject')

        # Removing M2M table for field related_production on 'DigitalObject'
        db.delete_table('archive_digitalobject_related_production')

        # Removing M2M table for field related_festival on 'DigitalObject'
        db.delete_table('archive_digitalobject_related_festival')

        # Removing M2M table for field related_venue on 'DigitalObject'
        db.delete_table('archive_digitalobject_related_venue')

        # Removing M2M table for field related_creator on 'DigitalObject'
        db.delete_table('archive_digitalobject_related_creator')

        # Removing M2M table for field related_work on 'DigitalObject'
        db.delete_table('archive_digitalobject_related_work')

        # Deleting model 'DigitalObjectType'
        db.delete_table('archive_digitalobjecttype')

        # Deleting model 'DigitalFile'
        db.delete_table('archive_digitalfile')

        # Deleting model 'Award'
        db.delete_table('archive_award')

        # Deleting model 'AwardCandidate'
        db.delete_table('archive_awardcandidate')

        # Deleting model 'Country'
        db.delete_table('archive_country')

        # Deleting model 'City'
        db.delete_table('archive_city')

        # Deleting model 'Language'
        db.delete_table('archive_language')

        # Deleting model 'WorkRecordType'
        db.delete_table('archive_workrecordtype')

        # Deleting model 'WorkRecordFunction'
        db.delete_table('archive_workrecordfunction')

        # Deleting model 'DirectingTeamFunction'
        db.delete_table('archive_directingteamfunction')

        # Deleting model 'CastMemberFunction'
        db.delete_table('archive_castmemberfunction')

        # Deleting model 'DesignTeamFunction'
        db.delete_table('archive_designteamfunction')

        # Deleting model 'TechTeamFunction'
        db.delete_table('archive_techteamfunction')

        # Deleting model 'ProductionTeamFunction'
        db.delete_table('archive_productionteamfunction')

        # Deleting model 'DocumentationTeamFunction'
        db.delete_table('archive_documentationteamfunction')

        # Deleting model 'AdvisoryTeamFunction'
        db.delete_table('archive_advisoryteamfunction')

        # Deleting model 'OrgFunction'
        db.delete_table('archive_orgfunction')

        # Deleting model 'FestivalFunction'
        db.delete_table('archive_festivalfunction')

        # Deleting model 'PhysicalObjectType'
        db.delete_table('archive_physicalobjecttype')

        # Deleting model 'VenueType'
        db.delete_table('archive_venuetype')

        # Deleting model 'BibliographicRecord'
        db.delete_table('archive_bibliographicrecord')

        # Deleting model 'BibliographicRecordType'
        db.delete_table('archive_bibliographicrecordtype')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection_id': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'birth_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'born_here'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'creator_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.RelatedCreator']", 'blank': 'True'}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'box_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': "orm['archive.Collection']"}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'digi_object_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObjectType']", 'null': 'True', 'blank': 'True'}),
            'digital_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'folder_date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'folder_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Language']", 'null': 'True', 'blank': 'True'}),
            'marks': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'measurements': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objects_created'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'phys_obj_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phys_obj_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phys_obj_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'phys_obj_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'phys_object_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.PhysicalObjectType']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_creator': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Creator']"}),
            'related_festival': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.FestivalOccurrence']"}),
            'related_production': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Production']"}),
            'related_venue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Location']"}),
            'related_work': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sponsor_note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collection_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'subseries_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subseries_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'festival_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Festival']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.FestivalParticipant']", 'blank': 'True'}),
            'productions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Production']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'festival_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']"})
        },
        'archive.festivalparticipant': {
            'Meta': {'object_name': 'FestivalParticipant'},
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalOccurrence']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"})
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
        'archive.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_venue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.production': {
            'Meta': {'object_name': 'Production'},
            'advisory_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advisory_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.AdvisoryMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cast_member_for'", 'symmetrical': 'False', 'through': "orm['archive.CastMember']", 'to': "orm['archive.Creator']"}),
            'design_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'design_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DesignMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'directing_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'directing_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DirectingMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'documentation_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documentation_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DocumentationMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_special_performance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_performances': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'premier': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'production_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'production_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.ProductionMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'blank': 'True'}),
            'secondary_bibliography': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'production_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.BibliographicRecord']"}),
            'source_work': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'performances'", 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'special_performance_type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Stage']", 'null': 'True', 'blank': 'True'}),
            'technical_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'technical_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.TechMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'theater_company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'productions'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']"}),
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
            'creator_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator_1'", 'to': "orm['archive.Creator']"}),
            'creator_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator_2'", 'to': "orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.OrgFunction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'relationship_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_since_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_since_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'relationship_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_until_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_until_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'archive.relatedwork': {
            'Meta': {'object_name': 'RelatedWork'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'work_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'text_1'", 'to': "orm['archive.WorkRecord']"}),
            'work_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'text_2'", 'to': "orm['archive.WorkRecord']"})
        },
        'archive.repository': {
            'Meta': {'object_name': 'Repository'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']"}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'archive.stage': {
            'Meta': {'object_name': 'Stage'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Creator']", 'through': "orm['archive.WorkRecordCreator']", 'symmetrical': 'False'}),
            'creators_display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'culture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkCulture']", 'null': 'True', 'blank': 'True'}),
            'digital_copy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkGenre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Language']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performance_rights': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'performance_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'performance_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'publication_rights': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'publication_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'publication_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_works': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'to': "orm['archive.WorkRecord']", 'through': "orm['archive.RelatedWork']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkStyle']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'works'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['archive']
