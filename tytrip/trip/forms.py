from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core.validators import MaxLengthValidator, MinLengthValidator

from .models import Topics, Capital, Trip, Comment


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


######################## alternative-forms ################

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'type': 'username',
            'placeholder': 'Имя пользователя'
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'type': 'password',
            'placeholder': 'Пароль'
        }),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
            'type': 'password',
            'placeholder': 'Повторите пароль'
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = get_user_model().objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': "Ваше имя"
        })
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': "Ваша почта"
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': "Тема"
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': "Ваше сообщение"
        })
    )
    captcha = CaptchaField()

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 3
            }),
        }
