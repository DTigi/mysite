from trip.models import Topics
from django import template

register = template.Library()

@register.inclusion_tag('trip/topic_list.html')
def show_topics(cat_selected_id=0):
    topics = Topics.objects.all()
    return {"topics": topics, "cat_selected": cat_selected_id,}