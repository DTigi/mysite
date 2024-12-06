from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core.validators import MaxLengthValidator, MinLengthValidator

from .models import Topics, Capital, Trip


### форма, не связанная с моделью forms.Form ###
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, min_length=5, widget=forms.TextInput(), label='Название',
#                             error_messages={'min_length': 'Слишком короткий заголовок', 'required': 'Без заголовка - никак'})
#     slug = forms.SlugField(max_length=255, label='URL', validators=[
#         MinLengthValidator(5, message="Минимум 5 символов"),
#         MaxLengthValidator(100, message="Максимум 100 символов"),
#     ])
#     content = forms.CharField(widget=forms.Textarea(), required=False, label='Текст статьи')
#     is_published = forms.BooleanField(required=False, initial=True, label='Опубликовать')
#     topic = forms.ModelChoiceField(queryset=Topics.objects.all(), empty_label='Не выбрано', label='Тема статьи')
#     capital = forms.ModelChoiceField(queryset=Capital.objects.all(), required=False, label='Столица')
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны быть только русские символы, дефис и пробел.")
#
#         return title


### форма связанная с моделью forms.ModelForm ###
class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255, min_length=5, widget=forms.TextInput(), label='Название',
    #                         error_messages={'min_length': 'Слишком короткий заголовок', 'required': 'Без заголовка - никак'})

    class Meta:
        model = Trip
        fields = ['title', 'slug', 'content', 'image', 'topic', 'is_published', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъьэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")

        return title


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")