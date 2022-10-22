from rest_framework import serializers

from characters.models import People

class PeopleSerializer(serializers.ModelSerializer):
  class Meta:
    model = People
    fields = '__all__'
    read_only_fields = ['id', 'created_at', 'updated_at']
