from django.urls import path, register_converter
from . import views
from . import  converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts, name='posts'),
    path('articles/', views.articles, name='articles'),
    path('tags/', views.tags, name='tags'),
    path('topics/<slug:topic_slug>/', views.TopicsListView.as_view(), name='topics'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', views.TagsListView.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
]
