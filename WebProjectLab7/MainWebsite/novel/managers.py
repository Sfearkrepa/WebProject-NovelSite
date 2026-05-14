from django.db import models
from django.utils import timezone


class NovelManager(models.Manager):

    def published(self):
        return self.filter(published_date__lte=timezone.now())

    def by_author(self, author_name):
        return self.filter(author__icontains=author_name)

    def popular(self):
        return self.filter(chapters_count__gte=50).order_by('-chapters_count')

    def completed(self):
        return self.filter(status='completed')

    def search(self, query):
        if not query:
            return self.all()
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(description__icontains=query)
        )

    def recent(self, limit=10):
        return self.order_by('-created_at')[:limit]