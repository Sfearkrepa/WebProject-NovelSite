from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Novel
from .forms import NovelForm


def home(request):
    return render(request, 'home.html')


# ====================== CRUD Новелл ======================

def novel_list(request):
    """Список новелл с использованием кастомного менеджера"""
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-published_date')
    filter_type = request.GET.get('filter', 'all')  # новый параметр

    # Используем кастомный менеджер
    if filter_type == 'published':
        novels = Novel.objects.published()
    elif filter_type == 'completed':
        novels = Novel.objects.completed()
    elif filter_type == 'popular':
        novels = Novel.objects.popular()
    else:
        novels = Novel.objects.all()

    # Поиск
    if query:
        novels = novels.search(query)  # используем метод search из менеджера

    # Сортировка
    valid_sorts = ['published_date', 'title', 'author', 'chapters_count', 'status',
                   '-published_date', '-title', '-author', '-chapters_count', '-status']

    if sort_by in valid_sorts:
        novels = novels.order_by(sort_by)
    else:
        novels = novels.order_by('-published_date')

    context = {
        'novels': novels,
        'total_novels': novels.count(),
        'title': 'Список новелл',
        'query': query,
        'sort_by': sort_by,
        'filter_type': filter_type,
    }
    return render(request, 'novel_list.html', context)


def novel_detail(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    return render(request, 'novel_detail.html', {'novel': novel})


def novel_create(request):
    if request.method == 'POST':
        form = NovelForm(request.POST)
        if form.is_valid():
            novel = form.save(commit=False)  # ← важно: commit=False

            # Генерируем slug здесь, если его нет
            if not novel.slug and novel.title:
                from django.utils.text import slugify
                base_slug = slugify(novel.title)
                slug = base_slug
                counter = 1
                while Novel.objects.filter(slug=slug).exclude(pk=novel.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                novel.slug = slug

            novel.save()  # ← теперь сохраняем с slug
            messages.success(request, f'Новелла "{novel.title}" успешно создана!')
            return redirect('novel_detail', slug=novel.slug)
    else:
        form = NovelForm()

    return render(request, 'novel_form.html', {'form': form, 'title': 'Добавить новеллу'})


def novel_update(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.method == 'POST':
        form = NovelForm(request.POST, instance=novel)
        if form.is_valid():
            novel = form.save(commit=False)

            if not novel.slug and novel.title:
                from django.utils.text import slugify
                base_slug = slugify(novel.title)
                slug_temp = base_slug
                counter = 1
                while Novel.objects.filter(slug=slug_temp).exclude(pk=novel.pk).exists():
                    slug_temp = f"{base_slug}-{counter}"
                    counter += 1
                novel.slug = slug_temp

            novel.save()
            messages.success(request, f'Новелла "{novel.title}" обновлена!')
            return redirect('novel_detail', slug=novel.slug)
    else:
        form = NovelForm(instance=novel)
    return render(request, 'novel_form.html', {'form': form, 'title': 'Редактировать новеллу'})


def novel_delete(request, slug):
    novel = get_object_or_404(Novel, slug=slug)
    if request.method == 'POST':
        title = novel.title
        novel.delete()
        messages.success(request, f'Новелла "{title}" удалена!')
        return redirect('novel_list')
    return render(request, 'novel_confirm_delete.html', {'novel': novel})


# ====================== Заглушки для остальных страниц ======================

def author_list(request):
    return HttpResponse(
        "<h2>Писатели</h2><p>Страница со списком авторов (в разработке).</p>",
        content_type="text/html; charset=utf-8"
    )


def ratings(request):
    return HttpResponse(
        "<h2>Оценки и рейтинги</h2><p>Страница рейтингов новелл (в разработке).</p>",
        content_type="text/html; charset=utf-8"
    )


def go_novels(request):
    return redirect('novel_list')


def page_not_found(request, exception):
    return HttpResponse("Страница не найдена (404)", status=404)