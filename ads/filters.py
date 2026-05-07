import django_filters
from .models import Ad, Category

class AdFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['category', 'title']