from django import forms
from .models import Topics, Capital


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(), label='Название')
    slug = forms.SlugField(max_length=255, label='Слаг')
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Текст статьи')
    is_published = forms.BooleanField(required=False, initial=True, label='Опубликовать')
    topic = forms.ModelChoiceField(queryset=Topics.objects.all(), empty_label='Не выбрано', label='Тема статьи')
    capital = forms.ModelChoiceField(queryset=Capital.objects.all(), required=False, label='Столица')