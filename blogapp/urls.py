from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('post/<int:id>/<slug:slug>/', post, name='post'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('view_all/<str:query>/', view_all, name='view_all'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
]
