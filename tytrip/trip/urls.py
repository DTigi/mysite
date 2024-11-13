from django.urls import path, register_converter
from . import views
from . import  converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('articles/', views.articles, name='articles'),
    path('tags/', views.tags, name='tags'),
    path('topics/<slug:topic_slug>/', views.topics, name='topics'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]
