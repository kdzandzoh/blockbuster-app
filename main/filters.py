import django_filters
from .models import Movie
from django_filters import CharFilter, NumberFilter


class MovieFilter(django_filters.FilterSet):
    s_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte', label='Start year')
    e_year = django_filters.NumberFilter(field_name='year', lookup_expr='lte', label='End year')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Title')    # ignore case
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='icontains', label='Genre')    # ignore case

    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ['movie_id', 'image_url', 'description', 'year', 'owner', 'due_date']