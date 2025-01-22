from django.urls import path, register_converter
from . import views
from . import  converters
from .views import SearchResultsView, SignUpView, SignInView, log_out, PostDetailView, FeedBackView, SuccessView, \
    TagView

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    # path('about/', views.about, name='about'),
    # path('topics/<slug:topic_slug>/', views.TopicsListView.as_view(), name='topics'),
    # path('addpage/', views.AddPage.as_view(), name='add_page'),
    # path('contact_old/', views.ContactFormView.as_view(), name='contact_old'),
    # path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('tag/<slug:tag_slug>/', views.TagsListView.as_view(), name='tag'),
    # path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    # path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', log_out, name='logout',),
    path('post/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
]
