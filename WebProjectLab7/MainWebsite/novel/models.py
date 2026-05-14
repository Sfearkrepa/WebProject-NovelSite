from django.db import models
from django.utils import timezone
from transliterate import translit, slugify as translit_slugify
from .managers import NovelManager


class NovelStatus(models.TextChoices):
    """Класс перечисления для статуса новеллы"""
    DRAFT = 'draft', 'Черновик'
    PUBLISHED = 'published', 'Опубликовано'
    COMPLETED = 'completed', 'Завершено'
    ON_HOLD = 'on_hold', 'На паузе'
    CANCELLED = 'cancelled', 'Отменено'


class Novel(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название новеллы"
    )

    author = models.CharField(
        max_length=100,
        verbose_name="Автор"
    )

    published_date = models.DateField(
        default=timezone.now,
        verbose_name="Дата публикации"
    )

    chapters_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество глав"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Slug (URL)"
    )

    # Новое поле с использованием Enum
    status = models.CharField(
        max_length=20,
        choices=NovelStatus.choices,
        default=NovelStatus.DRAFT,
        verbose_name="Статус"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Подключаем наш пользовательский менеджер
    objects = NovelManager()  # теперь Novel.objects — это наш менеджер
    all_objects = models.Manager()  # оригинальный менеджер (если понадобится)

    class Meta:
        verbose_name = "Новелла"
        verbose_name_plural = "Новеллы"
        ordering = ['-published_date', 'title']

    def __str__(self):
        return f"{self.title} — {self.author}"

    def save(self, *args, **kwargs):
        """Автоматическая генерация slug"""
        if not self.slug and self.title:
            try:
                title_trans = translit(self.title, 'ru', reversed=True)
                base_slug = translit_slugify(title_trans)
                if not base_slug:
                    base_slug = f"novel-{self.pk or 'new'}"

                slug = base_slug
                counter = 1
                while Novel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
            except Exception:
                self.slug = f"novel-{self.pk or 'unknown'}"

        super().save(*args, **kwargs)

    def get_status_display(self):
        """Удобный метод для отображения статуса"""
        return dict(NovelStatus.choices).get(self.status, self.status)