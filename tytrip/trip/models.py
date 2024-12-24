from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Trip.Status.PUBLISHED)


class Trip(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг", validators=[
        MinLengthValidator(5),
        MaxLengthValidator(100),
    ])
    image = models.ImageField(upload_to="images/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Изображение")
    content = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время редактирования")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус публикации")
    topic = models.ForeignKey('Topics', on_delete=models.PROTECT, related_name='posts', verbose_name="Тема")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='posts', verbose_name="Теги")
    capital = models.OneToOneField('Capital', on_delete=models.SET_NULL, null=True, blank=True, related_name='trip',
                                   verbose_name="Столица")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None, verbose_name="Автор")
    tag = TaggableManager()

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'
        ordering = ['-time_update']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'slug': self.slug})


class Topics(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Тема")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def get_absolute_url(self):
        return reverse('topics', kwargs={'topic_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Capital(models.Model):
    name = models.CharField(max_length=100)
    population = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']

    def __str__(self):
        return self.text


class UploadFile(models.Model):
    file = models.FileField(upload_to="upload_model")