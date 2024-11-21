from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from datetime import datetime

from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Trip, Topics, TagPost
from .utils import DataMixin


# Create your views here.

class IndexView(DataMixin, ListView):
    # model = Trip
    template_name = 'trip/index.html'
    context_object_name = 'posts'
    queryset = Trip.published.all().select_related('topic').prefetch_related('tags')


    # def get_queryset(self):
    #     return Trip.published.all().select_related('topic').prefetch_related('tags')


    extra_context = {
        'title': 'Главная страница',
        'newest_posts': queryset.order_by('-time_create')[:3],
        }


class AddPage(CreateView):
    # model = Trip
    # fields = ['title', 'slug', 'content', 'is_published', 'topic']
    form_class = AddPostForm
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Добавление статьи',
    }

class UpdatePage(UpdateView):
    model = Trip
    fields = ['title', 'content', 'image', 'is_published', 'topic']
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование статьи',
    }

class DeletePage(DeleteView):
    model = Trip
    fields = ['title', 'content', 'image', 'is_published', 'topic']
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': f'Удаление статьи:',
    }

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


class TopicsListView(DataMixin, ListView):
    template_name = 'trip/index.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_queryset(self):
        return Trip.published.filter(topic__slug=self.kwargs['topic_slug']).select_related('topic').prefetch_related('tags')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topics, slug=self.kwargs['topic_slug'])
        context['title'] = 'Тема - ' + topic.name
        context['newest_posts'] = *self.get_queryset().order_by('-time_create')[:3],
        return context


class ShowPost(DetailView):
    # model = Trip
    template_name = 'trip/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


    def get_object(self, queryset=None):
        return get_object_or_404(Trip.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title # self.get_object().title
        return context


class TagsListView(DataMixin, ListView):
    template_name = 'trip/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Trip.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('topic').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег - ' + tag.tag
        context['newest_posts'] = *self.get_queryset().order_by('-time_create')[:3],
        return context

def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация Trip_app")

def logout(request):
    return HttpResponse("logout Trip_app")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

##################### views-functions ##################################################

# def index(request):
#     post_db = Trip.published.all().select_related('topic').prefetch_related('tags')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': post_db,
#         'newest_posts': post_db.order_by('-time_create')[:3],
#         'cat_selected': 0,
#     }
#     return render(request, 'trip/index.html', context=data)

# def addpost(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {'title': 'Добавление статьи',
#             'menu': menu,
#             'form' : form,
#             }
#     return render(request, 'trip/addpage.html', context=data)

# def topics(request, topic_slug):
#     topic = get_object_or_404(Topics, slug=topic_slug)
#     posts_db = Trip.published.filter(topic_id=topic.id).select_related('topic').prefetch_related('tags')
#     data = {
#         'title': f'Тема статьи: {topic.name}',
#         'menu': menu,
#         'posts': posts_db,
#         'newest_posts': posts_db.order_by('-time_create')[:3],
#         'cat_selected': topic.id,
#     }
#
#     return render(request, 'trip/index.html', context=data)

# def show_post(request, post_slug):
#     post = get_object_or_404(Trip, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'trip/post.html', context=data)

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.posts.filter(is_published=Trip.Status.PUBLISHED).select_related('topic').prefetch_related('tags')
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'newest_posts': posts.order_by('-time_create')[:3],
#         'cat_selected': None,
#     }
#
#     return render(request, 'trip/index.html', context=data)