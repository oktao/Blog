
from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def average(queryset, field_name):
    return queryset.aggregate(avg=Avg(field_name))['avg']
