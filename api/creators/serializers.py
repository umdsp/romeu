from django.forms import widgets
from rest_framework import serializers
from archive.models import Creator
from archive import constants

class CreatorSerializer(serializers.ModelSerializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    creator_type = serializers.ChoiceField(choices=constants.CREATOR_TYPE_CHOICES,
                                         default=u'person')
    prefix      = serializers.CharField(required=False,
                                        max_length=100)
    given_name  = serializers.CharField(required=False,
                                        max_length=255)
    middle_name = serializers.CharField(required=False,
                                        max_length=255)
    family_name = serializers.CharField(required=False,
                                        max_length=255)


    def restore_object(self, attrs, instance=None):
        """
        Update a creator instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.creator_type = attrs.get('creator_type', instance.creator_type)
            instance.prefix = attrs.get('prefix', instance.prefix)
            instance.given_name = attrs.get('given_name', instance.given_name)
            instance.middle_name = attrs.get('middle_name', instance.middle_name)
            instance.family_name = attrs.get('family_name', instance.family_name)
            return instance

        # Create new instance
        return Creator(**attrs)
    
    class Meta:
        model = Creator
        fields = ('id', 'creator_type', 'prefix', 'given_name', 'middle_name', 'family_name')
