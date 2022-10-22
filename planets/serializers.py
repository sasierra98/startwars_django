from rest_framework import serializers

from planets.models import Planet

class PlanetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Planet
    fields = '__all__'
    read_only_fields = ['id', 'created_at', 'updated_at']
