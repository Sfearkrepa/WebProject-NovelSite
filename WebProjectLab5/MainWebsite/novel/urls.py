from django.urls import path
from . import views
from .converters import register_converters

# Регистрируем кастомный конвертер
register_converters()

urlpatterns = [
    path('', views.home, name='home'),

    # Динамические URL
    path('novels/', views.novel_list, name='novel_list'),
    path('novels/<int:page>/', views.novel_list, name='novel_list_paged'),
    path('novels/<novel_slug:slug>/', views.novel_detail, name='novel_detail'),

    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),

    path('ratings/', views.ratings, name='ratings'),

    # Redirect
    path('go-novels/', views.go_to_novels, name='go_novels'),
]