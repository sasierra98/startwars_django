from django_filters import rest_framework as filters

from movies.models import Movie


class PeopleFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = ['name']
