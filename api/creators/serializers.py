from django.forms import widgets
from rest_framework import serializers
from archive.models import Creator
from archive import constants


                    
class CreatorSerializer(serializers.ModelSerializer):

    roles                   = serializers.Field(source='display_roles')
    related_creators        = serializers.Field(source='creator_relationship')
    productions             = serializers.Field(source='productions')
    written_texts           = serializers.Field(source='works')
    
    awards                  = serializers.SerializerMethodField('get_awards')
    primary_bibliography    = serializers.SerializerMethodField('get_primary_publications')
    secondary_bibliography  = serializers.SerializerMethodField('get_secondary_publications')
    data                    = serializers.SerializerMethodField('get_data')

    class Meta:
        model = Creator
        fields = ('id', 'creator_type', 'prefix', 'given_name', 'middle_name',
                  'family_name', 'org_name', 'roles', 'biography', 'notes',
                  'related_creators', 'written_texts', 'productions', 'awards',
                  'primary_bibliography', 'secondary_bibliography',
                  'profiler_name', 'profiler_entry_date', 'data',
                )
    
    def get_data(self, obj):
        data = []
        a_dict={}
        if obj.website:
            a_dict['website'] = obj.website,
        if obj.nationality:
            a_dict['nationality'] = obj.nationality.demonym
        if obj.birth_date:
            if obj.creator_type == 'corp':
              a_dict['earliest_active'] = obj.birth_date_display 
            else:
              a_dict["birthdate"] = obj.birth_date_display
        if obj.birth_city:
            if obj.creator_type == 'corp':
                a_dict['place-of-origination'] = obj.birth_city
            else:
                a_dict['place-of-birth'] = obj.birth_city
        if obj.death_date:
            if obj.creator_type == 'corp':
                a_dict['latest-active'] = obj.death_date_display
            else:
                a_dict['death-date'] =  obj.death_date_display
        if obj.death_city:
            if obj.creator_type == 'corp':
                a_dict['place-of-dissolution'] = obj.death_city
            else:
                a_dict['place-of-death'] =  obj.death_city
        if obj.headquarter_city:
            a_dict['office-hq'] = obj.headquarter_city

        data.append(a_dict)
        return data

    def get_awards(self, obj):
        awards = []
        for award_candidate in obj.recipient.all():
            a_dict = {'year': award_candidate.year,
                      'category': award_candidate.category,
                      'recipient':  award_candidate.recipient,
                      'result': award_candidate.get_result_display 
            }
            awards.append(a_dict)
        return awards
    
    def get_primary_publications(self, obj):
        primary_pub = []
        for citation in obj.primary_publications.all():
            a_dict={'title': citation.title
            }
            primary_pub.append(a_dict)
        return primary_pub
    
    def get_secondary_publications(self, obj):
        secondary_pub = []
        for citation in obj.secondary_publications.all():
            a_dict={'title': citation.title
            }
            secondary_pub.append(a_dict)
        return secondary_pub