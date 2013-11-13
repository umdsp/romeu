# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from modeltranslation.translator import translator, TranslationOptions
from archive.models import SubjectSource, SubjectHeading, Creator, RelatedCreator, Location, Stage, WorkRecord, WorkRecordCreator, Production, DirectingMember, CastMember, DesignMember, TechMember, ProductionMember, Festival, FestivalOccurrence, FestivalParticipant, Repository, Collection, DigitalObject, Award, AwardCandidate, Country, City, Language, WorkRecordType, WorkRecordFunction, DirectingTeamFunction, CastMemberFunction, DesignTeamFunction, TechTeamFunction, ProductionTeamFunction, AdvisoryTeamFunction, OrgFunction, FestivalFunction, PhysicalObjectType, VenueType, License
from archive.models import TranslatingFlatPage, HomePageInfo


class SubjectSourceTranslationOptions(TranslationOptions):
    fields = ('title',)

class SubjectHeadingTranslationOptions(TranslationOptions):
    fields = ('title',)

class CreatorTranslationOptions(TranslationOptions):
    fields = ('biography', 'notes',)

class LocationTranslationOptions(TranslationOptions):
    fields = ('title', 'state', 'summary', 'notes',)

class StageTranslationOptions(TranslationOptions):
    fields = ('stage_lighting', 'stage_sound', 'notes',)
    
class WorkRecordTranslationOptions(TranslationOptions):
    fields = ('publication_rights', 'performance_rights', 'summary', 'notes',)    

class ProductionTranslationOptions(TranslationOptions):
    fields = ('notes',)

class FestivalTranslationOptions(TranslationOptions):
    fields = ('title',)

class FestivalOccurrenceTranslationOptions(TranslationOptions):
    fields = ('notes',)

class RepositoryTranslationOptions(TranslationOptions):
    fields = ('summary', 'notes',)

class CollectionTranslationOptions(TranslationOptions):
    fields = ('summary', 'notes',)

class DigitalObjectTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'notes',)

class AwardTranslationOptions(TranslationOptions):
    fields = ('notes',)

class AwardCandidateTranslationOptions(TranslationOptions):
    fields = ('category', 'notes',)

class TranslatingFlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)

class CountryTranslationOptions(TranslationOptions):
    fields = ('name', 'demonym',)

class CityTranslationOptions(TranslationOptions):
    fields = ('name', 'state',)

class LanguageTranslationOptions(TranslationOptions):
    fields = ('name',)

class WorkRecordTypeTranslationOptions(TranslationOptions):
    fields = ('name',)
    
class WorkRecordFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)
    
class DirectingTeamFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class CastMemberFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class DesignTeamFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class TechTeamFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class ProductionTeamFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class AdvisoryTeamFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class OrgFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class FestivalFunctionTranslationOptions(TranslationOptions):
    fields = ('title',)

class PhysicalObjectTypeTranslationOptions(TranslationOptions):
    fields = ('title',)

class VenueTypeTranslationOptions(TranslationOptions):
    fields = ('title',)

class LicenseTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class HomePageInfoTranslationOptions(TranslationOptions):
    fields = ('content',)

translator.register(SubjectSource, SubjectSourceTranslationOptions)
translator.register(SubjectHeading, SubjectHeadingTranslationOptions)
translator.register(Creator, CreatorTranslationOptions)
translator.register(Location, LocationTranslationOptions)
translator.register(Stage, StageTranslationOptions)
translator.register(WorkRecord, WorkRecordTranslationOptions)
translator.register(Production, ProductionTranslationOptions)
translator.register(Festival, FestivalTranslationOptions)
translator.register(FestivalOccurrence, FestivalOccurrenceTranslationOptions)
translator.register(Repository, RepositoryTranslationOptions)
translator.register(Collection, CollectionTranslationOptions)
translator.register(DigitalObject, DigitalObjectTranslationOptions)
translator.register(Award, AwardTranslationOptions)
translator.register(AwardCandidate, AwardCandidateTranslationOptions)

translator.register(Country, CountryTranslationOptions)
translator.register(City, CityTranslationOptions)
translator.register(Language, LanguageTranslationOptions)
translator.register(WorkRecordType, WorkRecordTypeTranslationOptions)
translator.register(WorkRecordFunction, WorkRecordFunctionTranslationOptions)
translator.register(DirectingTeamFunction, DirectingTeamFunctionTranslationOptions)
translator.register(CastMemberFunction, CastMemberFunctionTranslationOptions)
translator.register(DesignTeamFunction, DesignTeamFunctionTranslationOptions)
translator.register(TechTeamFunction, TechTeamFunctionTranslationOptions)
translator.register(ProductionTeamFunction, ProductionTeamFunctionTranslationOptions)
translator.register(AdvisoryTeamFunction, AdvisoryTeamFunctionTranslationOptions)
translator.register(OrgFunction, OrgFunctionTranslationOptions)
translator.register(FestivalFunction, FestivalFunctionTranslationOptions)
translator.register(PhysicalObjectType, PhysicalObjectTypeTranslationOptions)
translator.register(VenueType, VenueTypeTranslationOptions)
translator.register(License, LicenseTranslationOptions)

translator.register(TranslatingFlatPage, TranslatingFlatPageTranslationOptions)
translator.register(HomePageInfo, HomePageInfoTranslationOptions)
