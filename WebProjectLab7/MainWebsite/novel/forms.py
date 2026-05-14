from django import forms
from .models import Novel


class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ['title', 'author', 'published_date', 'chapters_count', 'description', 'status']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }