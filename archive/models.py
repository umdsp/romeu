# coding: utf-8
import os
from django.core.files.storage import FileSystemStorage

from django.db import models
from django.db.models import Min, Max, Avg, Count
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

from unidecode import unidecode

from smart_selects.db_fields import ChainedForeignKey
from taggit.managers import TaggableManager
from archive.utils import display_date
from archive import constants

import reversion

from random import choice

class OverwriteStorage(FileSystemStorage):
    """
    Returns same name for existing file and deletes existing file on save.
    """                                                              
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

def check_attention(sender, **kwargs):
    obj = kwargs['instance']
    try:
        if obj.attention == None or obj.attention == u'':
            att = False
        else:
            att = True
        obj.has_attention = att
    except:
        pass
pre_save.connect(check_attention)


def make_unique(seq, idfun=None):  
    # order preserving 
    if idfun is None: 
        def idfun(x): return x 
    seen = {} 
    result = [] 
    for item in seq: 
        marker = idfun(item) 
        # in old Python versions: 
        # if seen.has_key(marker) 
        # but in new ones: 
        if marker in seen: continue 
        seen[marker] = 1 
        result.append(item) 
    return result

# Subject heading models
class SubjectSource(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    ead_title = models.CharField(max_length=50, verbose_name=_("EAD title"))

    def __unicode__(self):
        return self.title

class SubjectHeading(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    subject_type = models.CharField(max_length=10, choices=constants.SUBJECT_TYPE_CHOICES, verbose_name=_("subject type"))
    source = models.ForeignKey(SubjectSource, related_name="headings", verbose_name=_("source"))
    parent_subject = models.ForeignKey("self", null=True, blank=True, related_name="child_subjects", verbose_name=_("parent subject"))
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.get_subject_type_display())

class Creator(models.Model):
    creator_type = models.CharField(max_length=10, choices=constants.CREATOR_TYPE_CHOICES, default=u'person', verbose_name=_("creator type"))
    prefix = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("name prefix"))
    given_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("given name(s)"))
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("middle name(s)"))
    family_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("family name(s)"))
    suffix = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("name suffix"))
    org_name = models.CharField(max_length=255, null=True, blank=True, help_text=_("For corporate creators, enter an organization name here instead of using the other name fields."), verbose_name=_("organization / corporate name"))
    creator_name = models.CharField(max_length=255, verbose_name=_("creator name"))
    creator_ascii_name = models.CharField(max_length=255, verbose_name=_("creator ASCII name"))
    name_variants = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("name variants"))
    # Dates
    birth_location = models.ForeignKey("Location", null=True, blank=True, related_name="born_here", verbose_name=_("birth location"))
    birth_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("birth date"))
    birth_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', null=True, blank=True, verbose_name=_("Precision"))
    birth_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    death_location = models.ForeignKey("Location", null=True, blank=True, related_name="died_here", verbose_name=_("death location"))
    death_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("death date"))
    death_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', null=True, blank=True, verbose_name=_("Precision"))
    death_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    earliest_active = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("earliest active"))
    earliest_active_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    earliest_active_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    latest_active = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("latest active"))
    latest_active_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    latest_active_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    # More info
    gender = models.CharField(max_length=2, choices=constants.GENDER_CHOICES, default=u'N', verbose_name=_("gender"))
    nationality = models.ForeignKey("Country", null=True, blank=True, verbose_name=_("nationality"))
    location = models.ForeignKey("Location", null=True, blank=True, help_text=_("Office / headquarters location (for corporate creators only)"), verbose_name=_("office / headquarters"))
    related_creators = models.ManyToManyField("self", through="RelatedCreator", symmetrical=False, null=True, blank=True, verbose_name=_("related creators"))
    biography = models.TextField(null=True, blank=True, verbose_name=_("biographical / historical note"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    photo = models.ForeignKey("DigitalObject", null=True, blank=True, verbose_name=_("photo"))
    primary_bibliography = models.ManyToManyField("BibliographicRecord", null=True, blank=True, related_name="primary_bibliography_for", verbose_name=_("primary bibliography"))
    secondary_bibliography = models.ManyToManyField("BibliographicRecord", null=True, blank=True, related_name="secondary_bibliography_for", verbose_name=_("secondary bibliography"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    
    class Meta:
        ordering = ['creator_name']
    
    def birth_date_display(self):
        return display_date(self.birth_date, self.birth_date_precision, self.birth_date_BC)
    birth_date_display.short_description = _("Birth date")
        
    def death_date_display(self):
        return display_date(self.death_date, self.death_date_precision, self.death_date_BC)
    death_date_display.short_description = _("Death date")
        
    def earliest_active_display(self):
        return display_date(self.earliest_active, self.earliest_active_precision, self.earliest_active_BC)
    earliest_active_display.short_description = _("Earliest active")
    
    def latest_active_display(self):
        return display_date(self.latest_active, self.latest_active_precision, self.latest_active_BC)
    latest_active_display.short_description = _("Latest active")
    
    def display_name_lastfirst(self):
        if self.creator_type == u'corp':
            name = self.org_name
        elif self.creator_type == u'family':
            name = "The " + self.family_name + " Family"
        else:
            name = ''
            if self.family_name:
                name += self.family_name
                if self.suffix:
                    name += ' ' + self.suffix + ', '
                else:
                    name += ', '
            if self.prefix:
                name += self.prefix + ' '
            if self.given_name:
                name += self.given_name + ' '
            if self.middle_name:
                name += self.middle_name + ' '
            name = name.rstrip(', ')
        return name
    
    def display_name(self):
        if self.creator_type == u'corp':
            name = self.org_name
        elif self.creator_type == u'family':
            name = "The " + self.family_name + " Family"
        else:
            name = ''
            if self.prefix:
                name += self.prefix + ' '
            if self.given_name:
                name += self.given_name + ' '
            if self.middle_name:
                name += self.middle_name + ' '
            if self.family_name:
                name += self.family_name + ' '
            if self.suffix:
                name += self.suffix
            name = name.rstrip()
        return name
    
    def has_system_links(self):
        if RelatedCreator.objects.filter(first_creator=self).exists():
            return True
        if RelatedCreator.objects.filter(second_creator=self).exists():
            return True
        if WorkRecordCreator.objects.filter(creator=self).exists():
            return True
        if Production.objects.filter(theater_company=self).exists():
            return True
        if DirectingMember.objects.filter(person=self).exists():
            return True
        if CastMember.objects.filter(person=self).exists():
            return True
        if DesignMember.objects.filter(person=self).exists():
            return True
        if TechMember.objects.filter(person=self).exists():
            return True
        if ProductionMember.objects.filter(person=self).exists():
            return True
        if DocumentationMember.objects.filter(person=self).exists():
            return True
        if AdvisoryMember.objects.filter(person=self).exists():
            return True
        if FestivalParticipant.objects.filter(participant=self).exists():
            return True
        if DigitalObject.objects.filter(object_creator=self).exists():
            return True
        if DigitalObject.objects.filter(related_creator=self).exists():
            return True
        if AwardCandidate.objects.filter(recipient=self).exists():
            return True
        if Production.objects.filter(related_organizations=self).exists():
            return True
        return False
    
    def system_links(self):
        works = ''
        if RelatedCreator.objects.filter(first_creator=self).exists():
            for obj in RelatedCreator.objects.filter(first_creator=self):
                works += "RelatedCreator: " + str(obj.pk) + "\n"
        if RelatedCreator.objects.filter(second_creator=self).exists():
            for obj in RelatedCreator.objects.filter(second_creator=self):
                works += "RelatedCreator: " + str(obj.pk) + "\n"
        if WorkRecordCreator.objects.filter(creator=self).exists():
            for obj in WorkRecordCreator.objects.filter(creator=self):
                works += "WorkRecordCreator: " + str(obj.pk) + "\n"
        if Production.objects.filter(theater_company=self).exists():
            for obj in Production.objects.filter(theater_company=self):
                works += "Production: " + str(obj.pk) + "\n"
        if Production.objects.filter(related_organizations=self).exists():
            for obj in Production.objects.filter(related_organizations=self):
                works += "Production: " + str(obj.pk) + "\n"
        if DirectingMember.objects.filter(person=self).exists():
            for obj in DirectingMember.objects.filter(person=self):
                works += "DirectingMember: " + str(obj.pk) + "\n"
        if CastMember.objects.filter(person=self).exists():
            for obj in CastMember.objects.filter(person=self):
                works += "CastMember: " + str(obj.pk) + "\n"
        if DesignMember.objects.filter(person=self).exists():
            for obj in DesignMember.objects.filter(person=self):
                works += "DesignMember: " + str(obj.pk) + "\n"
        if TechMember.objects.filter(person=self).exists():
            for obj in TechMember.objects.filter(person=self):
                works += "TechMember: " + str(obj.pk) + "\n"
        if ProductionMember.objects.filter(person=self).exists():
            for obj in ProductionMember.objects.filter(person=self):
                works += "ProductionMember: " + str(obj.pk) + "\n"
        if DocumentationMember.objects.filter(person=self).exists():
            for obj in DocumentationMember.objects.filter(person=self):
                works += "DocumentationMember: " + str(obj.pk) + "\n"
        if AdvisoryMember.objects.filter(person=self).exists():
            for obj in AdvisoryMember.objects.filter(person=self):
                works += "AdvisoryMember: " + str(obj.pk) + "\n"
        if FestivalParticipant.objects.filter(participant=self).exists():
            for obj in FestivalParticipant.objects.filter(participant=self):
                works += "FestivalParticipant: " + str(obj.pk) + "\n"
        if DigitalObject.objects.filter(object_creator=self).exists():
            for obj in DigitalObject.objects.filter(object_creator=self):
                works += "DigitalObject: " + str(obj.pk) + "\n"
        if DigitalObject.objects.filter(related_creator=self).exists():
            for obj in DigitalObject.objects.filter(related_creator=self):
                works += "DigitalObject: " + str(obj.pk) + "\n"
        if AwardCandidate.objects.filter(recipient=self).exists():
            for obj in AwardCandidate.objects.filter(recipient=self):
                works += "AwardCandidate: " + str(obj.pk) + "\n"
        if works == "":
            return False
        else:
            return works
    
    def has_works(self):
        if WorkRecordCreator.objects.filter(creator=self).exists():
            return True
        else:
            return False
            
    def works(self):
        records = []
        wrc = WorkRecordCreator.objects.filter(creator=self)
        for record in wrc:
            if record.work_record.creation_date:
                date = record.work_record.creation_date_display()
            else:
                date = "N/A"
            x = { 'record_id': record.work_record.pk, 'record_title': record.work_record.title, 'function': record.function.title, 'date': date }
            records.append(x)
        return records
    
    def has_productions(self):
        result = False
        if self.directing_team_for.count() > 0:
            result = True
        elif self.cast_member_for.count() > 0:
            result = True
        elif self.design_team_for.count() > 0:
            result = True
        elif self.technical_team_for.count() > 0:
            result = True
        elif self.production_team_for.count() > 0:
            result = True
        elif self.documentation_team_for.count() > 0:
            result = True
        elif self.advisory_team_for.count() > 0:
            result = True
        elif self.company_productions.count() > 0:
            result = True
        elif self.productions_related_to.count() > 0:
            result = True
        return result
    
    def productions(self):
        prods = []
        if self.directing_team_for.count() > 0:
            for dt in self.directing_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': DirectingMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.cast_member_for.count() > 0:
            for cm in self.cast_member_for.all():
                x = { 'prod_id': cm.pk, 'prod_title': cm.title, 'venue': cm.venue.title, 'date_range': cm.begin_date_display() + '&mdash;' + cm.end_date_display(), 'role': CastMember.objects.filter(person=self, production=cm)[0].function.title }
                prods.append(x)
        if self.design_team_for.count() > 0:
            for dt in self.design_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': DirectingMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.technical_team_for.count() > 0:
            for dt in self.technical_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': TechMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.production_team_for.count() > 0:
            for dt in self.production_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': ProductionMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.documentation_team_for.count() > 0:
            for dt in self.documentation_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': DocumentationMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.advisory_team_for.count() > 0:
            for dt in self.advisory_team_for.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': AdvisoryMember.objects.filter(person=self, production=dt)[0].function.title }
                prods.append(x)
        if self.company_productions.count() > 0:
            for dt in self.company_productions.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': 'Theater company' }
                prods.append(x)
        if self.productions_related_to.count() > 0:
            for dt in self.productions_related_to.all():
                x = { 'prod_id': dt.pk, 'prod_title': dt.title, 'venue': dt.venue.title, 'date_range': dt.begin_date_display() + '&mdash;' + dt.end_date_display(), 'role': 'Related organization' }
                prods.append(x)
        return prods
        
    def display_roles(self):
        roles = []
        rolestring = ""
        if self.org_name:
            roles.append('organization')
        dm = DirectingMember.objects.filter(person=self)
        if dm:
            for time in dm:
                roles.append(time.function.title)
        if CastMember.objects.filter(person=self):
            if self.gender == 'f':
                roles.append('actress')
            else:
                roles.append('actor')
        wrc = WorkRecordCreator.objects.filter(creator=self)
        if wrc:
            for time in wrc:
                roles.append(time.function.title)
        # now put them in a list
        roles = make_unique(roles)
        for r in roles:
            rolestring += r
            rolestring += ", "
        rolestring = rolestring.rstrip(', ')
        rolestring = rolestring.capitalize()
        
        return rolestring
    display_roles.short_description = _("Roles")
    
    def has_related_creators(self):
        if self.first_creator_to.all() or self.second_creator_to.all():
            return True
        else:
            return False
    
    def same_birthplace_creators(self):
        if not self.birth_location:
            return False
        else:
            bp = self.birth_location
            rc = Creator.objects.filter(birth_location=bp).filter(published=True)
            rel = 'location'
        if not rc:
            bc = bp.city
            rc = Creator.objects.filter(birth_location__city=bc).filter(published=True)
            rel = 'city'
        
        x = {'rc': rc, 'rel': rel}
        return x
    
    def same_production_creators(self):
        if not self.has_productions():
            return False
        else:
            productions = self.productions()
            # Pick one at random
            p = choice(productions)['prod_id']
            p = Production.objects.get(id=p)
            # TODO: Pick up here after you write the function to get people from a production
        
            return True
    
    def __unicode__(self):
        if self.birth_date and self.death_date:
            return "%s, %s-%s" % (self.creator_name, self.birth_date_display(), self.death_date_display())
        if self.birth_date:
            return "%s, %s-" % (self.creator_name, self.birth_date_display())
        else:
            return self.creator_name

def update_creator_name(sender, **kwargs):
    obj = kwargs['instance']
    obj.creator_name = obj.display_name_lastfirst()
    obj.creator_ascii_name = unidecode(obj.creator_name)

pre_save.connect(update_creator_name, sender=Creator)

class RelatedCreator(models.Model):
    """Information about relationships between creators - members of organizations, family members, etc.
    """
    first_creator = models.ForeignKey(Creator, related_name="first_creator_to", verbose_name=_("creator 1"))
    relationship = models.CharField(max_length=12, choices=constants.CREATOR_RELATIONSHIP_TYPES, verbose_name=_("relationship"))
    second_creator = models.ForeignKey(Creator, related_name="second_creator_to", verbose_name=_("related creator"))
    function = models.ForeignKey("OrgFunction", null=True, blank=True, help_text=_("If the relationship is membership in an organization, select the member's function in the organization here."), verbose_name=_("function"))
    relationship_since = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_("relationship since"))
    relationship_since_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("precision"))
    relationship_since_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    relationship_until = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_("relationship until"))
    relationship_until_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("precision"))
    relationship_until_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    
    def relationship_since_display(self):
        return display_date(self.relationship_since, self.relationship_since_precision, self.relationship_since_BC)
    relationship_since_display.short_description = _("Relationship since")
    
    def relationship_until_display(self):
        return display_date(self.relationship_until, self.relationship_until_precision, self.relationship_until_BC)
    relationship_until_display.short_description = _("Relationship until")
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_creator.display_name(), self.get_relationship_display(), self.second_creator.display_name())

class Location(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    title_ascii = models.CharField(max_length=255, verbose_name=_("title (ASCII)"))
    title_variants = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("title variants"))
    is_venue = models.BooleanField(default=False, verbose_name=_("Is a venue"), help_text=_("Check this box if productions / festivals occur at this location"))
    venue_type = models.ForeignKey("VenueType", null=True, blank=True, verbose_name=_("venue type"))
    address = models.CharField(max_length=100, verbose_name=_("street address"), null=True, blank=True)
    address2 = models.CharField(max_length=100, verbose_name=_("street address (line 2)"), null=True, blank=True)
    city = models.ForeignKey("City", null=True, blank=True, verbose_name=_("city"))
    state = models.CharField(max_length=100, verbose_name=_("state/province"), null=True, blank=True)
    postal_code = models.CharField(max_length=20, verbose_name=_("postal code"), null=True, blank=True)
    country = models.ForeignKey("Country", verbose_name=_("country"))
    lat = models.CharField(max_length=20, verbose_name=_("latitude"), null=True, blank=True)
    lon = models.CharField(max_length=20, verbose_name=_("longitude"), null=True, blank=True)
    altitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("altitude"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    photo = models.ForeignKey("DigitalObject", related_name="locations", null=True, blank=True, verbose_name=_("photo"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.country.name)

    def has_system_links(self):
        if Stage.objects.filter(venue=self).exists():
            return True
        if Production.objects.filter(venue=self).exists():
            return True
        if FestivalOccurrence.objects.filter(venue=self).exists():
            return True
        if Repository.objects.filter(location=self).exists():
            return True
        if DigitalObject.objects.filter(phys_obj_location=self).exists():
            return True
        if DigitalObject.objects.filter(related_venue=self).exists():
            return True
        if AwardCandidate.objects.filter(place=self).exists():
            return True
        if Creator.objects.filter(birth_location=self).exists():
            return True
        if Creator.objects.filter(death_location=self).exists():
            return True
        if Creator.objects.filter(location=self).exists():
            return True
        return False

def update_location_name(sender, **kwargs):
    obj = kwargs['instance']
    obj.title_ascii = unidecode(obj.title)

pre_save.connect(update_location_name, sender=Location)

class Stage(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    venue = models.ForeignKey(Location, related_name="stages", verbose_name=_("venue"))
    square_footage = models.PositiveIntegerField(null=True, blank=True, help_text=_("Number only, no commas"), verbose_name=_("square footage"))
    stage_type = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("stage type"))
    stage_width = models.PositiveIntegerField(null=True, blank=True, help_text=_("Width of the stage, in feet"), verbose_name=_("stage width"))
    stage_depth = models.PositiveIntegerField(null=True, blank=True, help_text=_("Depth of the stage, in feet"), verbose_name=_("stage depth"))
    stage_height = models.PositiveIntegerField(null=True, blank=True, help_text=_("Amount of vertical space on stage, in feet"), verbose_name=_("stage height"))
    stage_lighting = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("stage lighting"))
    stage_sound = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("stage sound"))
    seating = models.PositiveIntegerField(null=True, blank=True, help_text=_("Number of audience members that can be accommodated"), verbose_name=_("seating"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.venue.country.name)
    
class WorkRecord(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    creators = models.ManyToManyField(Creator, through="WorkRecordCreator", verbose_name=_("creators"))
    creators_display = models.CharField(max_length=255, verbose_name=_("creators"))
    work_type = models.ForeignKey("WorkRecordType", verbose_name=_("work type"))
    subject = models.ManyToManyField(SubjectHeading, null=True, blank=True, related_name="works", verbose_name=_("subject"))
    genre = models.ForeignKey("WorkGenre", null=True, blank=True, help_text=_("The work's genre - e.g. drama, comedy"), verbose_name=_("genre"))
    culture = models.ForeignKey("WorkCulture", null=True, blank=True, help_text=_("The culture the work is a part of"), verbose_name=_("culture"))
    style = models.ForeignKey("WorkStyle", null=True, blank=True, help_text=_("A movement or period the work belongs to"), verbose_name=_("style"))
    lang = models.ManyToManyField("Language", null=True, blank=True, verbose_name=_("language"))
    creation_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("creation date"))
    creation_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    creation_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    publication_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("creation date"))
    publication_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    publication_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    publication_rights = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("publication rights"))
    performance_rights = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("performance rights"))
    website = models.URLField(null=True, blank=True, help_text=_("A site where users can find the text of this work"), verbose_name=_("website"))
    digital_copy = models.ForeignKey("DigitalObject", null=True, blank=True, verbose_name=_("digital copy"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    related_works = models.ManyToManyField("self", through="RelatedWork", symmetrical=False, null=True, blank=True, related_name="related_to", verbose_name=_("related works"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))

    def creation_date_display(self):
        return display_date(self.creation_date, self.creation_date_precision, self.creation_date_BC)
    creation_date_display.short_description = _("Creation date")
    
    def publication_date_display(self):
        return display_date(self.publication_date, self.publication_date_precision, self.publication_date_BC)
    publication_date_display.short_description = _("Publication date")

    def creators_display_links(self):
        cs = ""
        for wrc in WorkRecordCreator.objects.filter(work_record=self):
            cs += "<a href='/creator/" + str(wrc.creator.id) + "'>"
            cs += wrc.creator.display_name()
            cs += "</a>, "
        cs = cs.rstrip(', ')
        return cs

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.work_type.name)

def update_wr_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_wr_title, sender=WorkRecord)

def update_workrecord_creators(sender, **kwargs):
    record = kwargs['instance'].work_record
    textstring = ''
    for c in WorkRecordCreator.objects.filter(work_record=record):
        textstring += c.creator.creator_name + ", "
    textstring = textstring.rstrip(', ')
    textstring = textstring[:255] if len(textstring) > 255 else textstring
    record.creators_display = textstring
    record.save()

class RelatedWork(models.Model):
    first_work = models.ForeignKey(WorkRecord, related_name="first_work_to", verbose_name=_("work"))
    relationship = models.CharField(max_length=5, choices=constants.RELATIONSHIP_TYPE_CHOICES, verbose_name=_("relationship"))
    second_work = models.ForeignKey(WorkRecord, related_name="second_work_to", verbose_name=_("related work"))
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_work.title, self.get_relationship_display(), self.second_work.title)

class WorkRecordCreator(models.Model):
    creator = models.ForeignKey(Creator, verbose_name=_("creator"))
    work_record = models.ForeignKey(WorkRecord, verbose_name=_("work record"))
    function = models.ForeignKey("WorkRecordFunction", verbose_name=_("function"))
    
    def __unicode__(self):
        return self.creator.creator_name

post_save.connect(update_workrecord_creators, sender=WorkRecordCreator)
    
class Role(models.Model):
    source_text = models.ForeignKey(WorkRecord, related_name="roles", verbose_name=_("source text"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.source_text.title)

class WorkGenre(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title

class WorkCulture(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title

class WorkStyle(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title
    
class Production(models.Model):
    source_work = models.ManyToManyField(WorkRecord, related_name="performances", verbose_name=_("source work"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("subtitle"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    venue = models.ForeignKey(Location, related_name="productions", verbose_name=_("venue"))
    stage = ChainedForeignKey(Stage, chained_field="venue", chained_model_field="venue", show_all=False, auto_choose=False, null=True, blank=True, verbose_name=_("stage"))
    begin_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("begin date"))
    begin_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    begin_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    end_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("end date"))
    end_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    end_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    num_performances = models.IntegerField(null=True, blank=True, verbose_name=_("Number of performances"))
    is_special_performance = models.BooleanField(default=False, verbose_name=_("Special performance?"))
    special_performance_type = models.CharField(max_length=12, choices=constants.SPECIAL_PERFORMANCE_CHOICES, null=True, blank=True, verbose_name=_("Type"))
    directing_team = models.ManyToManyField(Creator, through="DirectingMember", null=True, blank=True, related_name="directing_team_for", verbose_name=_("directing team"))
    cast = models.ManyToManyField(Creator, through="CastMember", related_name="cast_member_for", verbose_name=_("cast"))
    design_team = models.ManyToManyField(Creator, through="DesignMember", null=True, blank=True, related_name="design_team_for", verbose_name=_("design team"))
    technical_team = models.ManyToManyField(Creator, through="TechMember", null=True, blank=True, related_name="technical_team_for", verbose_name=_("technical team"))
    production_team = models.ManyToManyField(Creator, through="ProductionMember", null=True, blank=True, related_name="production_team_for", verbose_name=_("production team"))
    documentation_team = models.ManyToManyField(Creator, through="DocumentationMember", null=True, blank=True, related_name="documentation_team_for", verbose_name=_("documentation team"))
    advisory_team = models.ManyToManyField(Creator, through="AdvisoryMember", null=True, blank=True, related_name="advisory_team_for", verbose_name=_("advisory team"))
    related_organizations = models.ManyToManyField(Creator, null=True, blank=True, related_name="productions_related_to", verbose_name=_("related organizations"))
    premier = models.CharField(max_length=2, choices=constants.PREMIER_CHOICES, null=True, blank=True, verbose_name=_("premier"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    secondary_bibliography = models.ManyToManyField("BibliographicRecord", null=True, blank=True, related_name="production_secondary_bibliography_for", verbose_name=_("secondary bibliography"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    theater_company = models.ForeignKey(Creator, null=True, blank=True, related_name="company_productions")

    def begin_date_display(self):
        return display_date(self.begin_date, self.begin_date_precision, self.begin_date_BC)
    begin_date_display.short_description = _("Begin date")
    
    def end_date_display(self):
        return display_date(self.end_date, self.end_date_precision, self.end_date_BC)
    end_date_display.short_description = _("End date")

    def display_directors(self):
        ds = ""
        for person in self.directing_team.all():
            ds += person.display_name()
            ds += ", "
        ds = ds[:-2]
        return ds
    display_directors.short_description = _("Directors")

    def display_directors_links(self):
        ds = ""
        for person in self.directing_team.all():
            ds += "<a href='/creator/" + str(person.id) + "'>"
            ds += person.display_name()
            ds += "</a>, "
        ds = ds[:-2]
        return ds
    display_directors_links.short_description = _("Directors")

    def all_production_creators(self):
        """
        Return a list of IDs of all creators attached to this production (directors, cast, tech, etc.) with function
        Format: [{'id': 123, 'function': x}, {'id': 124, 'function': y}]
        """
        allpeople = []
        for p in DirectingMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in CastMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in DesignMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in TechMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in ProductionMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in DocumentationMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        for p in AdvisoryMember.objects.filter(production=self).filter(published=True):
            allpeople.append({'id': p.person.id, 'function': p.function})
        return allpeople

    def __unicode__(self):
        if self.begin_date:
            return "%s (%s, %s)" % (self.title, self.venue.title, self.begin_date_display())
        else:
            return "%s (%s)" % (self.title, self.venue.title)

def update_prod_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_prod_title, sender=Production)

class DirectingMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("DirectingTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class CastMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("CastMemberFunction", verbose_name=_("function"))
    role = models.ForeignKey(Role, null=True, blank=True, verbose_name=_("role"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class DesignMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("DesignTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class TechMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("TechTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class ProductionMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("ProductionTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class DocumentationMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("DocumentationTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class AdvisoryMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("AdvisoryTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s)" % (self.person.creator_name, self.function.title)

class Festival(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))

    def __unicode__(self):
        return self.title

class FestivalOccurrence(models.Model):
    festival_series = models.ForeignKey(Festival, verbose_name=_("festival series"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    venue = models.ForeignKey(Location, verbose_name=_("venue"))
    begin_date = models.DateField(help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("begin date"))
    begin_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    begin_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    end_date = models.DateField(help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("end date"))
    end_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    end_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    participants = models.ManyToManyField(Creator, through="FestivalParticipant", null=True, blank=True, verbose_name=_("participants"))
    productions = models.ManyToManyField(Production, verbose_name=_("productions"))
    secondary_bibliography = models.ManyToManyField("BibliographicRecord", null=True, blank=True, related_name="festival_secondary_bibliography_for", verbose_name=_("secondary bibliography"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))

    def begin_date_display(self):
        return display_date(self.begin_date, self.begin_date_precision, self.begin_date_BC)
        
    def end_date_display(self):
        return display_date(self.end_date, self.end_date_precision, self.end_date_BC)

    def __unicode__(self):
        return "%s (%s, %s - %s)" % (self.title, self.venue.title, self.begin_date_display(), self.end_date_display())

class FestivalParticipant(models.Model):
    participant = models.ForeignKey(Creator, verbose_name=_("participant"))
    festival = models.ForeignKey(FestivalOccurrence, verbose_name=_("festival"))
    function = models.ForeignKey("FestivalFunction", verbose_name=_("function"))
    
class Repository(models.Model):
    repository_id = models.CharField(max_length=3, null=True, blank=True, verbose_name=_("repository ID"))
    title = models.CharField(max_length=200, verbose_name=_("title"))
    location = models.ForeignKey(Location, verbose_name=_("location"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    
    class Meta:
        verbose_name_plural = "repositories"
    
    def __unicode__(self):
        return "Repository: %s" % (self.title,)
    
class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    repository = models.ForeignKey(Repository, related_name="collections", verbose_name=_("repository"))
    collection_id = models.CharField(max_length=4, verbose_name=_("collection ID"))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))

    def __unicode__(self):
        return "Collection: %s" % (self.title,)

def object_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    rep_code = instance.digital_object.collection.repository.repository_id
    col_code = instance.digital_object.collection.collection_id
    obj_code = instance.digital_object.object_id
    seq_code = instance.seq_id
    
    new_filename = ''.join([rep_code, col_code, obj_code, seq_code, '001.', extension])
    
    instance.digital_object.attention += ''.join(['File: ', new_filename, 'Original filename: ', filename])
    
    return '/'.join(['digitalobjects', rep_code, col_code, new_filename])

def setup_new_object(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.object_id:
        try:
            biggest_id = DigitalObject.objects.filter(collection=instance.collection).aggregate(Max('object_id'))
            biggest_id = '%06d' % (biggest_id['object_id__max'] + 1)
            instance.object_id = biggest_id
        except:
            instance.object_id = '000001'

def setup_digital_file(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.seq_id:
        try:
            biggest_id = DigitalFile.objects.filter(digital_object=instance.digital_object).aggregate(Max('seq_id'))
            biggest_id = '%04d' % (biggest_id['seq_id__max'] + 1)
            instance.seq_id = biggest_id
        except:
            instance.seq_id = '0001'

class DigitalObject(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    collection = models.ForeignKey(Collection, related_name="collection_objects", verbose_name=_("collection"))
    object_creator = models.ForeignKey(Creator, null=True, blank=True, related_name="objects_created", verbose_name=_("object creator"))
    language = models.ForeignKey("Language", null=True, blank=True, verbose_name=_("language"))
    subject = models.ManyToManyField(SubjectHeading, null=True, blank=True, related_name="collection_objects", verbose_name=_("subject"))
    object_id = models.CharField(max_length=6, null=True, blank=True, verbose_name=_("object ID"))
    digital_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("digital ID"))
    rights_holders = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("rights holder(s)"))
    license_type = models.ForeignKey("License", default=1, verbose_name=_("license type"))
    permission_form = models.FileField(upload_to='permissionforms', verbose_name=_("permission form"), null=True, blank=True)
    # Physical object info
    identifier = models.CharField(max_length=60, help_text=_("e.g. ISBN, ISSN, DOI"), null=True, blank=True, verbose_name=_("identifier"))
    marks = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("marks/inscriptions"))
    measurements = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("physical description"))
    phys_object_type = models.ForeignKey("PhysicalObjectType", verbose_name=_("Physical object type"), null=True, blank=True)
    donor = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("donor"))
    sponsor_note = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("sponsor note"))
    phys_obj_date = models.DateField(null=True, blank=True, verbose_name=_("physical object date"))
    phys_obj_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', null=True, blank=True, verbose_name=_("Precision"))
    phys_obj_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    phys_obj_location = models.ForeignKey("Location", null=True, blank=True, verbose_name=_("physical object location"))
    # Digital object info
    digi_object_format = models.ForeignKey("DigitalObjectType", verbose_name=_("Digital object format"), null=True, blank=True)
    # Container info
    series_num = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("series #"))
    series_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("series name"))
    subseries_num = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("subseries #"))
    subseries_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("subseries name"))
    box_num = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("box #"))
    folder_num = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("folder #"))
    folder_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("folder name"))
    folder_date = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("folder date"))
    # Relationships
    related_production = models.ManyToManyField(Production, related_name="related_objects", null=True, blank=True, verbose_name=_("related production"))
    related_festival = models.ManyToManyField(FestivalOccurrence, related_name="related_objects", null=True, blank=True, verbose_name=_("related festival"))
    related_venue = models.ManyToManyField(Location, related_name="related_objects", null=True, blank=True, verbose_name=_("related venue"))
    related_creator = models.ManyToManyField(Creator, related_name="related_objects", null=True, blank=True, verbose_name=_("related creator"))
    related_work = models.ManyToManyField(WorkRecord, related_name="related_objects", null=True, blank=True, verbose_name=_("related work"))
    # extra details
    tags = TaggableManager(verbose_name=_("tags"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    creation_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("creation date"))
    creation_date_precision = models.CharField(max_length=1, null=True, blank=True, choices=constants.DATE_PRECISION_CHOICES, default=u'y', verbose_name=_("Precision"))
    creation_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    
    def contribution_date_display(self):
        return display_date(self.contribution_date, self.contribution_date_precision, self.contribution_date_BC)
    
    def creation_date_display(self):
        return display_date(self.creation_date, self.creation_date_precision, self.creation_date_BC)
    
    def object_number(self):
        num = ''
        num += self.collection.repository.repository_id
        num += self.collection.collection_id
        num += self.object_id
        return num
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, str(self.object_number()))

class License(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    image = models.FileField(upload_to='license_images', verbose_name=_("image"), null=True, blank=True)

    def __unicode__(self):
        return self.title

class DigitalObjectType(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    category = models.CharField(max_length=50, verbose_name=_("category"))
    
    def __unicode__(self):
        return self.title
    
class DigitalFile(models.Model):
    filepath = models.FileField(upload_to=object_upload_path, storage=OverwriteStorage(), verbose_name=_("File"), null=True, blank=True)
    seq_id = models.CharField(max_length=4, null=True, blank=True, verbose_name=_("sequence ID"))
    digital_object = models.ForeignKey(DigitalObject, related_name="files", verbose_name=_("digital object"))
    
    def __unicode__(self):
        return self.filepath.name
    
pre_save.connect(setup_new_object, sender=DigitalObject)
pre_save.connect(setup_digital_file, sender=DigitalFile)
    
# Awards
class Award(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"), help_text=_("For a series of awards (e.g. Tony Award, Drama Desk Award), not award categories (Tony Award for Best Musical, etc.)"))
    award_org = models.CharField(max_length=200, verbose_name=_("award organization"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    
    def __unicode__(self):
        return "%s" % (self.title)
    
class AwardCandidate(models.Model):
    award = models.ForeignKey(Award, verbose_name=_("award"))
    year = models.PositiveIntegerField(max_length=4, help_text=_("Please enter a 4-digit year (e.g. 1999, not 99)"), verbose_name=_("year"))
    category = models.CharField(max_length=140, null=True, blank=True, help_text=_("e.g. Best Performance, Best Musical"), verbose_name=_("category"))
    result = models.CharField(max_length=1, choices=constants.AWARD_RESULT_CHOICES, verbose_name=_("result"))
    recipient = models.ForeignKey(Creator, null=True, blank=True, related_name="awards", help_text=_("A specific person or organization receiving the award"), verbose_name=_("recipient"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    production = models.ForeignKey(Production, null=True, blank=True, related_name="awards", verbose_name=_("production"))
    place = models.ForeignKey(Location, null=True, blank=True, related_name="awards", verbose_name=_("place"))
    festival = models.ForeignKey(Festival, null=True, blank=True, related_name="awards", verbose_name=_("festival"))
    work_record = models.ForeignKey(WorkRecord, null=True, blank=True, related_name="awards", verbose_name=_("work record"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s for %s, %d (%s)" % (self.award.title, self.category, self.year, self.get_result_display())

# Enumeration fields - countries, languages, functions, etc.
class Country(models.Model):
    name = models.CharField(max_length=100, help_text=_("Name of the country (e.g. Cuba)"), verbose_name=_("name"))
    demonym = models.CharField(max_length=100, help_text=_("What someone from this country is called (e.g. Cuban)"), verbose_name=_("demonym"))
    
    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    state = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("state"))
    country = models.ForeignKey(Country, related_name="cities", verbose_name=_("country"))
    
    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        ordering = ['name']
    
    def __unicode__(self):
        if self.state:
            return "%s, %s, %s" % (self.name, self.state, self.country.name)
        else:
            return "%s, %s" % (self.name, self.country.name)

class Language(models.Model):
    name = models.CharField(max_length=60, verbose_name=_("name"))
    shortcode = models.CharField(max_length=2, help_text=_("This language's 2-letter shortcode ('en', 'es', etc.)"), verbose_name=_("shortcode"))
    archival_code = models.CharField(max_length=10, help_text=_("A longer archival language code ('eng', 'spa', etc.)"), verbose_name=_("archival code"))
    
    class Meta:
        verbose_name=_("language")
        verbose_name_plural=_("languages")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WorkRecordType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    
    class Meta:
        verbose_name = _("work record type")
        verbose_name_plural = _("work record types")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WorkRecordFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("work record function")
        verbose_name_plural = _("work record functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class DirectingTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("directing team function")
        verbose_name_plural = _("directing team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class CastMemberFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("cast member function")
        verbose_name_plural = _("cast member functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class DesignTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("design team function")
        verbose_name_plural = _("design team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class TechTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("technical team function")
        verbose_name_plural = _("technical team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class ProductionTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("production team function")
        verbose_name_plural = _("production team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class DocumentationTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("documentation team function")
        verbose_name_plural = _("documentation team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class AdvisoryTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("advisory team function")
        verbose_name_plural = _("advisory team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class OrgFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    func_type = models.CharField(max_length=6, choices=constants.CREATOR_RELATIONSHIP_TYPES, verbose_name=_("function type"))
    
    class Meta:
        verbose_name = _("organizational function")
        verbose_name_plural = _("organizational functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class FestivalFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("festival function")
        verbose_name_plural = _("festival functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class PhysicalObjectType(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("physical object type")
        verbose_name_plural = _("physical object types")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class VenueType(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("venue type")
        verbose_name_plural = _("venue types")
        ordering = ['title']

    def __unicode__(self):
        return self.title

class BibliographicRecord(models.Model):
    bib_type = models.CharField(max_length=5, choices=constants.BIB_TYPE_CHOICES, verbose_name=_("bibliography type"))
    abstract = models.TextField(null=True, blank=True, verbose_name=_("abstract"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    short_title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("short title"))
    booktitle = models.CharField(max_length=255, null=True, blank=True, help_text=_("Only for works contained in a larger book"), verbose_name=_("book title"))
    publication = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publication title"))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"))
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("author(s)"))
    editor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("editor(s)"))
    translator = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("translator(s)"))
    volume = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("volume"))
    num_volumes = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("number of volumes"))
    issue_num = models.CharField(max_length=40, null=True, blank=True, help_text=_("Issue number"), verbose_name=_("issue number"))
    series = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series title"), verbose_name=_("series"))
    series_text = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series subtitle"), verbose_name=_("series text"))
    series_num = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("series number"))
    chapter = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("chapter"))
    edition = models.CharField(max_length=30, null=True, blank=True, help_text=_("Enter as an ordinal number ('Second', 'Third')"), verbose_name=_("edition"))
    section = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("section"))
    pub_date = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("publication date"))
    access_date = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("access date"))
    num_pages = models.CharField(max_length=60, null=True, blank=True, verbose_name=_("number of pages"))
    language = models.CharField(max_length=60, null=True, blank=True, verbose_name=_("language"))
    isbn = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("ISBN"))
    issn = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("ISSN"))
    doi = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("DOI"))
    pages = models.CharField(max_length=30, null=True, blank=True, help_text=_("Enter one or more pages / page ranges"), verbose_name=_("pages"))
    publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publisher"))
    address = models.CharField(max_length=255, null=True, blank=True, help_text=_("Publisher's address; omit for major publishers"), verbose_name=_("address"))
    medium = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("medium"))
    format = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("format"))
    art_size = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("artwork size"))
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("label"))
    runtime = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("running time"))
    archive = models.CharField(max_length=255, null=True, blank=True, help_text=_("An archive that holds this item"), verbose_name=_("archive"))
    archive_location = models.CharField(max_length=200, null=True, blank=True, help_text=_("A call number or location within the archive holding this item"), verbose_name=_("location in archive"))
    version = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("version"))
    system = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("system"))
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("type"))
    university = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("university"))
    library = models.CharField(max_length=255, null=True, blank=True, help_text=_("A library that holds this item"), verbose_name=_("library"))
    library_catalog_num = models.CharField(max_length=255, null=True, blank=True, help_text=_("The catalog call number for the library holding this item"), verbose_name=_("library catalog number"))
    rights = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("rights"))
    extra = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("extra"))
    work_record = models.ForeignKey("WorkRecord", null=True, blank=True, verbose_name=_("work record"))
    
    class Meta:
        verbose_name = _("bibliographic record")
        verbose_name_plural = _("bibliographic records")
    
    def __unicode__(self):
        if self.journal:
            return "%s, %s. %s. %s" % (self.author, self.title, self.journal, self.year)
        else:
            return "%s, %s (%s)" % (self.author, self.title, self.year)

class BibliographicRecordType(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    has_abstract = models.BooleanField(default=True, verbose_name=_("has an abstract"))
    has_title = models.BooleanField(default=True, verbose_name=_("has a title"))
    has_shorttitle = models.BooleanField(default=False, verbose_name=_("has a short title"))
    has_booktitle = models.BooleanField(default=False, verbose_name=_("has a book title"))
    has_pubtitle = models.BooleanField(default=False, verbose_name=_("has a publication title"))
    has_url = models.BooleanField(default=False, verbose_name=_("has a URL"))
    has_author = models.BooleanField(default=True, verbose_name=_("has an author / creator"))
    has_editor = models.BooleanField(default=False, verbose_name=_("has an editor"))
    has_translator = models.BooleanField(default=False, verbose_name=_("has a translator"))
    has_volume = models.BooleanField(default=False, verbose_name=_("has a volume number"))
    has_num_volumes = models.BooleanField(default=False, verbose_name=_("has a fixed number of volumes"))
    has_issue_num = models.BooleanField(default=False, verbose_name=_("has an issue number"))
    has_series = models.BooleanField(default=False, verbose_name=_("has a book series title"))
    has_chapter = models.BooleanField(default=False, verbose_name=_("has chapter numbers"))
    has_edition = models.BooleanField(default=False, verbose_name=_("has editions"))
    has_month = models.BooleanField(default=False, verbose_name=_("has a month designation"))
    has_year = models.BooleanField(default=False, verbose_name=_("has a year designation"))
    has_pages = models.BooleanField(default=False, verbose_name=_("has a page range / ranges"))
    has_publisher = models.BooleanField(default=False, verbose_name=_("has a publisher"))
    has_address = models.BooleanField(default=False, verbose_name=_("has a publisher's address"))
    has_workrecord = models.BooleanField(default=False, verbose_name=_("is linked to a work record"))
    
# register version control
reversion.register(Creator)
reversion.register(Location)
reversion.register(WorkRecord)
reversion.register(Production)
reversion.register(FestivalOccurrence)
reversion.register(DigitalObject)