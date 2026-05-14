from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests


def home(request):
    return render(request, 'home.html')


def novel_list(request, page=1):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts', timeout=5)
        response.raise_for_status()
        novels = response.json()[:12]
    except Exception:
        novels = []

    context = {
        'novels': novels,
        'page': page,
        'total_novels': len(novels),
        'current_year': 2026,
        'is_empty': len(novels) == 0,
        'title': 'Список новелл'
    }

    return render(request, 'novel_list.html', context)


def novel_detail(request, slug):
    text = f"Новелла: {slug.title()}<br><br>Здесь будет подробная информация о новелле."
    return HttpResponse(text, content_type="text/html; charset=utf-8")


def author_list(request):
    return HttpResponse(
        "Писатели<br><br>Список авторов новелл.",
        content_type="text/html; charset=utf-8"
    )


def author_detail(request, pk):
    return HttpResponse(
        f"Писатель №{pk}<br><br>Информация об авторе.",
        content_type="text/html; charset=utf-8"
    )


def ratings(request):
    return HttpResponse(
        "Оценки и рейтинги<br><br>Страница с оценками новелл.",
        content_type="text/html; charset=utf-8"
    )


def go_to_novels(request):
    """Пример перенаправления"""
    return redirect('novel_list')


def page_not_found(request, exception):
    """Кастомная страница 404"""
    return HttpResponse("Page not found", status=404)