"""
Forms for the sticky_notes_app.
"""
from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and editing notes.
    """

    class Meta:
        """Meta configuration for NoteForm."""
        model = Note
        fields = ['title', 'content', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter note title...',
                    'maxlength': '200'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter note content...',
                    'rows': '5',
                    'cols': '40'
                }
            ),
            'category': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'priority': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_title(self):
        """
        Validate title field.
        """
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError("Title is required.")
        return title.strip()

    def clean_content(self):
        """Validate content field."""
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Content is required.")
        return content.strip()


class NoteSearchForm(forms.Form):
    """
    Form for searching notes.
    """

    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search notes...',
                'aria-label': 'Search notes'
            }
        )
    )

    category_filter = forms.ChoiceField(
        choices=[('', 'All Categories')] + Note.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    priority_filter = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Note.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
