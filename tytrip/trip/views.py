from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse
from datetime import datetime

from .models import Trip, Topics, TagPost

menu = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "Посты", 'url_name': 'posts'},
        {'title': "Статьи", 'url_name': 'articles'},
        {'title': "Теги", 'url_name': 'tags'},
        {'title': "Темы", 'url_name': 'home'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': '10 мест, ради которых стоит проснуться на рассвете', 'content': 'Итак, вы в Питере. Раннее утро. Лед с рек и каналов уже ушел, запущены фонтаны города... Музеи еще закрыты. Что посмотреть?', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/coast', 'is_published': True},
    {'id': 2, 'title': 'Йога для начинающих в домашних условиях', 'content': 'Расскажем, какие упражнения выбрать и как сделать коврик для занятий йогой из того, что можно найти в шкафу.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/yoga', 'is_published': True},
    {'id': 3, 'title': 'Лучшие музыкальные фестивали этого лета', 'content': 'Лето на носу, а с ним и музыкальные фестивали. На каком же из них вы разобьёте свою палатку?<br><br>Мы составили список лучших летних фестивалей по всему миру.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/festival', 'is_published': True},
    {'id': 4, 'title': 'Наукоёмкий подход к кулинарии', 'content': 'Узнаем основы проектирования новых пищевых и около-пищевых опытов, вскроем физику, химию и микробиологию еды.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/food', 'is_published': True},
    {'id': 5, 'title': 'делаем модные принты на подушках для интерьера', 'content': 'Подушки для дивана целесообразнее заказать в съемных чехлах на молнии, если потребуется чистка подушек, проще снять чехлы, чем везти подушку в химчистку.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/prints', 'is_published': True},
    {'id': 6, 'title': 'Как первый раз отправиться в горы?', 'content': 'Для начала нужно определиться, в каком формате пройдёт ваше путешествие. Это зависит от многих факторов, не только от ваших желаний и интересов.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/mountain', 'is_published': True},
    {'id': 7, 'title': 'Наукоёмкий подход к кулинарии', 'content': 'Узнаем основы проектирования новых пищевых и около-пищевых опытов, вскроем физику, химию и микробиологию еды.', 'tags': ['travel', 'health'], 'time': '10 июня 2019', 'author': 'Неизвестный автор', 'img': 'trip/images/post_images/coast', 'is_published': True},
]

# Create your views here.
def index(request):
    post_db = Trip.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': post_db,
        'cat_selected': 0,
    }
    return render(request, 'trip/index.html', context=data)

def about(request):
    return render(request, 'trip/about.html', {'title': 'About my site', 'menu': menu})

def posts(request):
    return HttpResponse('<h1>Посты</h1>')

def articles(request):
    if request.GET:
        print(request.GET)

    return HttpResponse('<h1>Статьи</h1>')

def tags(request):
    return HttpResponse(f"Отображение списка тегов")

def topics(request, topic_slug):
    topic = get_object_or_404(Topics, slug=topic_slug)
    posts_db = Trip.published.filter(topic_id=topic.id)
    data = {
        'title': f'Тема статьи: {topic.name}',
        'menu': menu,
        'posts': posts_db,
        'cat_selected': topic.id,
    }

    return render(request, 'trip/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Trip, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'trip/post.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.posts.filter(is_published=Trip.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'trip/index.html', context=data)

def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')