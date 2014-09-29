
"""
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
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from selectable.base import LookupBase
from selectable.registry import registry

from archive.models import (Creator, Location, Production, WorkRecord, Role,
                            Country, DigitalObject, Festival, City, Award,
                            DesignTeamFunction, FestivalOccurrence, Collection,
                            AwardCandidate)


class ArchiveLookup(LookupBase):

    """
        API Class for every lookups
    """

    filters = {}
    model = ""

    def __init__(self):
        self.lookup_base = "Archive Lookup"

    def get_queryset(self):

        """
            Main method which takes the current request
            and returns the data which matches the search
        """

        query_set = self.model._default_manager.get_query_set()
        if self.filters:
            query_set = query_set.filter(**self.filters)
        return query_set

    @staticmethod
    def get_item_id(item):

        """
           Returns a string representation of the item
           to be returned by the field/widget.
        """

        return item.pk

    def get_item(self, value):

        """
            take the value from the form initial values
            and return the current item
        """

        item = None
        if value:
            try:
                item = self.get_queryset().filter(pk=value)[0]
            except IndexError:
                pass
        return item

    @staticmethod
    def get_item_value(item):

        """
            Returns: A string representation of the
                    item to be shown in the input.
        """

        return item.__unicode__()


class CreatorLookup(ArchiveLookup):

    """
        lookup with a search filed for the Creator Model
    """

    model = Creator

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Creator.objects.filter(
            Q(creator_ascii_name__icontains=term) |
            Q(creator_name__icontains=term) |
            Q(name_variants__icontains=term) |
            Q(creator_display_name__icontains=term) |
            Q(creator_display_ascii_name__icontains=term))


class TheaterCompanyLookup(ArchiveLookup):

    """
        lookup with a search filed for the Theater Company Model
    """

    model = Creator

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Creator.objects.filter(org_name__icontains=term)


class LocationLookup(ArchiveLookup):

    """
        lookup with a search filed for the Location Model
    """

    model = Location

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Location.objects.filter(
            Q(title_ascii__icontains=term) |
            Q(title__icontains=term) |
            Q(title_variants__icontains=term))


class ProductionLookup(ArchiveLookup):

    """
        lookup with a search filed for the Production Model
    """

    model = Production

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Production.objects.filter(
            Q(ascii_title__icontains=term) |
            Q(title__icontains=term) |
            Q(title_variants__icontains=term))


class WorkRecordLookup(ArchiveLookup):

    """
        lookup with a search filed for the WorkRecord Model
    """

    model = WorkRecord

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """

        return WorkRecord.objects.filter(
            Q(ascii_title__icontains=term) |
            Q(title__icontains=term) |
            Q(title_variants__icontains=term))


class RoleLookup(ArchiveLookup):

    """
        lookup with a search filed for the Role Model
    """

    model = Role

    @staticmethod
    def get_query(request, term):

        """
            Returns: An iterable set of data of items matching
                    the search term.
        """

        production = None
        work_record_list = request.GET.get('source_text', None)
        if work_record_list is None:
            production_id = request.GET.get('production', None)
            try:
                production = Production.objects.get(pk=production_id)
                work_record_list = production.source_work.all().values_list(
                    'id', flat=True)
            except ObjectDoesNotExist:
                production = None
        else:
            work_record_list = list(work_record_list.split(","))

        if work_record_list:
            return Role.objects.filter(
                Q(source_text__id__in=work_record_list),
                (Q(source_text__title__icontains=term) |
                 Q(source_text__ascii_title__icontains=term) |
                 Q(source_text__title_variants__icontains=term) |
                 Q(title__icontains=term)))
        else:
            return Role.objects.filter(
                Q(source_text__title__icontains=term) |
                Q(source_text__ascii_title__icontains=term) |
                Q(source_text__title_variants__icontains=term) |
                Q(title__icontains=term))


class CountryLookup(ArchiveLookup):

    """
        lookup with a search filed for the Country Model
    """
    model = Country

    @staticmethod
    def get_query(request, term):

        """
            Returns: An iterable set of data of items matching
                    the search term.
        """

        return Country.objects.filter(
            Q(name__icontains=term) |
            Q(demonym__icontains=term))


class DigitalObjectLookup(ArchiveLookup):

    """
        lookup with a search filed for the Digital Object Model
    """

    model = DigitalObject

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return DigitalObject.objects.filter(
            Q(object_id__icontains=term) |
            Q(digital_id__icontains=term) |
            Q(identifier__icontains=term) |
            Q(title__icontains=term) |
            Q(title_variants__icontains=term) |
            Q(summary__icontains=term))


class FestivalLookup(ArchiveLookup):

    """
        lookup with a search filed for the Festival Model
    """

    model = Festival

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Festival.objects.filter(title__icontains=term)


class FestivalOccurrenceLookup(ArchiveLookup):

    """
        lookup with a search filed for the FestivalOccurrence Model
    """

    model = FestivalOccurrence

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return FestivalOccurrence.objects.filter(
            Q(title__icontains=term) |
            Q(title_variants__icontains=term) |
            Q(festival_series__title__icontains=term))

class CollectionLookup(ArchiveLookup):

    """
        lookup with a search filed for the Collection Model
    """

    model = Collection

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Collection.objects.filter(
            Q(collection_id__icontains=term) |
            Q(title__icontains=term)).order_by('title')


class CityLookup(ArchiveLookup):

    """
        lookup with a search filed for the City Model
    """

    model = City

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        results = City.objects.filter(name__icontains=term)
        country = request.GET.get('country', '')
        if country:
            results = results.filter(country__name__icontains=country)

        return results


class AwardLookup(ArchiveLookup):

    """
        lookup with a search filed for the Award Model
    """

    model = Award

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return Award.objects.filter(title__icontains=term)


class AwardCandidateLookup(ArchiveLookup):

    """
        lookup with a search filed for the Award Candidate Model
    """

    model = AwardCandidate

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return AwardCandidate.objects.filter(
            Q(recipient__creator_ascii_name__icontains=term) |
            Q(recipient__creator_name__icontains=term) |
            Q(award__title__icontains=term))


class DesignTeamFunctionLookup(ArchiveLookup):

    """
        lookup with a search filed for the Design Team Function Model
    """

    model = DesignTeamFunction

    @staticmethod
    def get_query(request, term):
        """
            Returns: An iterable set of data of items matching
                    the search term.
        """
        return DesignTeamFunction.objects.filter(title__icontains=term)


registry.register(CreatorLookup)
registry.register(TheaterCompanyLookup)
registry.register(LocationLookup)
registry.register(ProductionLookup)
registry.register(WorkRecordLookup)
registry.register(RoleLookup)
registry.register(CountryLookup)
registry.register(DigitalObjectLookup)
registry.register(FestivalLookup)
registry.register(FestivalOccurrenceLookup)
registry.register(AwardCandidateLookup)
registry.register(CollectionLookup)
registry.register(CityLookup)
registry.register(AwardLookup)
registry.register(DesignTeamFunctionLookup)
