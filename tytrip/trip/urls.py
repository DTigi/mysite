from django.urls import path, register_converter
from . import views
from . import  converters
from .views import IndexView, TopicsListView, TagsListView, ShowPost

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('articles/', views.articles, name='articles'),
    path('tags/', views.tags, name='tags'),
    path('topics/<slug:topic_slug>/', TopicsListView.as_view(), name='topics'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', TagsListView.as_view(), name='tag'),
]
