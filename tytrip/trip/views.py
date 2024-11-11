from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse
from datetime import datetime

menu = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "Посты", 'url_name': 'posts'},
        {'title': "Статьи", 'url_name': 'articles'},
        {'title': "Теги", 'url_name': 'tags'},
        {'title': "Темы", 'url_name': 'topics'},
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
    # temp = render_to_string('trip/index_old.html')
    # return HttpResponse(temp)temp
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'url': slugify('Main page'),
        'posts': data_db,
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

def topics(request):
    return HttpResponse(f"Темы")

def get_archive(request, year):
    if year > datetime.now().year:
        uri = reverse('cats', args=('sport',))
        return HttpResponsePermanentRedirect(uri) # redirect(uri, permanent=True)

    return HttpResponse(f'<h1>Архив</h1><p>Архив: {year}</p>')

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')