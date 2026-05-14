from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('novels/', views.novel_list, name='novel_list'),
    path('novels/create/', views.novel_create, name='novel_create'),
    path('novels/<slug:slug>/', views.novel_detail, name='novel_detail'),
    path('novels/<slug:slug>/edit/', views.novel_update, name='novel_update'),
    path('novels/<slug:slug>/delete/', views.novel_delete, name='novel_delete'),

    path('authors/', views.author_list, name='author_list'),
    path('ratings/', views.ratings, name='ratings'),

    path('go-novels/', views.go_novels, name='go_novels'),
]