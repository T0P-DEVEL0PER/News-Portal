from django.forms import DateInput
from django_filters import FilterSet, CharFilter

from .models import Post


class PostFilter(FilterSet):
    datetime_of_creation = CharFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Post
        fields = {'name': ['exact'], 'author': ['exact']}
