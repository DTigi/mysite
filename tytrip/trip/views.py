from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse
from datetime import datetime

from .forms import AddPostForm, UploadFileForm
from .models import Trip, Topics, TagPost

menu = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Статьи", 'url_name': 'articles'},
        {'title': "Теги", 'url_name': 'tags'},
        {'title': "Темы", 'url_name': 'home'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

# Create your views here.
def index(request):
    post_db = Trip.published.all().select_related('topic').prefetch_related('tags')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': post_db,
        'newest_posts': post_db.order_by('-time_create')[:5],
        'cat_selected': 0,
    }
    return render(request, 'trip/index.html', context=data)

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {'title': 'Добавление статьи',
            'menu': menu,
            'form' : form,
            }
    return render(request, 'trip/addpage.html', context=data)


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == "POST":
        # handle_uploaded_file(request.FILES['file_upload'])
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    data = {
        'title': 'Upload file',
        'menu': menu,
        'form': form,}
    return render(request, 'trip/about.html', context=data)

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
    posts_db = Trip.published.filter(topic_id=topic.id).select_related('topic').prefetch_related('tags')
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
    posts = tag.posts.filter(is_published=Trip.Status.PUBLISHED).select_related('topic').prefetch_related('tags')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'trip/index.html', context=data)

def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')