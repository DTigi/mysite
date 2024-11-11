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
    path('topics/', views.topics, name='topics'),
    path('archive/<year4:year>/', views.get_archive, name='archive'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post, name='post'),
]
