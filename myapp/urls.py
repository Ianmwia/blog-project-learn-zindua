from django.urls import path
from . import views
from .views import BlogListCreateAPIView, AuthorListAPIView, BlogDetailAPIView

urlpatterns = [
    # page views
    path("index", views.index, name='index'),
    path("", views.home, name='home'),
    path("add_blog", views.add_blog, name='add_blog'),
    path("blog_list", views.blog_list, name='blog_list'),
    path("filter_demo", views.filter_demo, name='filter_demo'),
    path("subscribe/", views.subscribe, name='subscribe'),
    path("contact_us", views.contact_us, name='contact_us'),
    path("accounts/register", views.registration, name='register'),

    #api views
    path('blogs/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>', BlogDetailAPIView.as_view(), name='blog-detail'),
    path('author/', AuthorListAPIView.as_view(), name='author-list'),
    

]

