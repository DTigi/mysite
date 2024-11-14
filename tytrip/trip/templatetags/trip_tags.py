from django.db.models import Count

from trip.models import Topics, TagPost
from django import template

register = template.Library()

@register.inclusion_tag('trip/topic_list.html')
def show_topics(cat_selected_id=0):
    topics = Topics.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {"topics": topics, "cat_selected": cat_selected_id,}

@register.inclusion_tag('trip/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count('posts')).filter(total__gt=0)}