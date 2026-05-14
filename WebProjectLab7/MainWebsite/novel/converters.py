from django.urls import register_converter

class NovelSlugConverter:
    regex = r'[\w-]+'

    def to_python(self, value):
        return value.replace('-', ' ').title()

    def to_url(self, value):
        return value.lower().replace(' ', '-')


def register_converters():
    register_converter(NovelSlugConverter, 'novel_slug')