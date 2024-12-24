from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from datetime import datetime

from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from taggit.models import Tag

from .forms import AddPostForm, UploadFileForm, ContactForm, CommentForm, SignUpForm, SignInForm, FeedBackForm
from .models import Trip, Topics, TagPost, Comment
from .permissions import IsAdminOrReadOnly
from .serializers import TripSerializer
from .utils import DataMixin



# Create your views here.

class IndexView(DataMixin, ListView):
    # model = Trip
    template_name = 'trip/index_new.html'
    context_object_name = 'posts'
    queryset = Trip.published.all().select_related('topic').prefetch_related('tags')
    # def get_queryset(self):
    #     return Trip.published.all().select_related('topic').prefetch_related('tags')
    extra_context = {
        'title': 'Главная страница',
        'newest_posts': queryset.order_by('-time_create')[:3],
        }


class AddPage(PermissionRequiredMixin, CreateView):
    # model = Trip
    # fields = ['title', 'slug', 'content', 'is_published', 'topic']
    form_class = AddPostForm
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Добавление статьи',
    }
    permission_required = 'trip.add_trip'
    # login_url = '/admin/'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, UpdateView):
    model = Trip
    fields = ['title', 'content', 'image', 'is_published', 'topic']
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование статьи',
    }
    permission_required = 'trip.change_trip'


class DeletePage(PermissionRequiredMixin, DeleteView):
    model = Trip
    fields = ['title', 'content', 'image', 'is_published', 'topic']
    template_name = 'trip/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': f'Удаление статьи:',
    }
    permission_required = 'trip.delete_trip'

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
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

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'trip/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

################### alternative-views ###########################
class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Trip.objects.all().order_by('-time_create')
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'trip/index.html', context={
            'page_obj': page_obj
        })


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Trip, slug=slug)
        common_tags = Trip.tag.most_common()
        last_posts = Trip.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'trip/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Trip, url=slug)
            Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'trip/post_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'trip/signup.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'trip/signup.html', context={'form': form})


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'trip/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "trip/signin.html", {"form": form})
        return render(request, 'trip/signin.html', context={
            'form': form,
        })


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'trip/contact_new.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, ['tgnudev@gmail.com',])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'trip/contact_new.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'trip/success.html', context={
            'title': 'Спасибо'
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ""
        if query:
            results = Trip.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'trip/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Trip.objects.filter(tag=tag)
        common_tags = Trip.tag.most_common()
        return render(request, 'trip/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


########################  API-Views ############################################
# class TripAPIView(generics.ListCreateAPIView):
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#
# class TripAPIUpdate(generics.UpdateAPIView):
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#
# class TripAPIDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (IsAdminOrReadOnly,)
    # authentication_classes = (TokenAuthentication,) # аутентификация только по токенам

    @action(methods=['get'], detail=False)
    def topics(self, request):
        topics = Topics.objects.all()
        return Response({'topic': [c.name for c in topics]})

    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #
    #     if not pk:
    #         return Trip.objects.all()[:3]
    #
    #     return Trip.objects.filter(pk=pk)

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