"""
Forms for the sticky_notes_app.

This module contains Django forms for the sticky notes application,
including the NoteForm for creating/editing notes and the NoteSearchForm
for searching and filtering notes.
"""

from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """
    Form for creating and editing notes.
    
    This form provides fields for all note attributes with appropriate
    widgets, validation, and styling. It includes custom validation
    for title and content fields to ensure they are not empty or
    whitespace-only.
    
    Attributes:
        Meta.model: The Note model this form is based on
        Meta.fields: List of fields to include in the form
        Meta.widgets: Custom widgets for form fields
    """

    class Meta:
        """Meta configuration for the NoteForm."""
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
        Validate the title field.
        
        Ensures the title is not empty or whitespace-only.
        
        Returns:
            str: The cleaned and stripped title
            
        Raises:
            ValidationError: If the title is empty or whitespace-only
        """
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError("Title is required.")
        return title.strip()

    def clean_content(self):
        """
        Validate the content field.
        
        Ensures the content is not empty or whitespace-only.
        
        Returns:
            str: The cleaned and stripped content
            
        Raises:
            ValidationError: If the content is empty or whitespace-only
        """
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Content is required.")
        return content.strip()


class NoteSearchForm(forms.Form):
    """
    Form for searching and filtering notes.
    
    This form provides fields for searching notes by text content
    and filtering by category and priority. All fields are optional
    to allow flexible searching and filtering.
    
    Attributes:
        search_query: Text field for searching in title and content
        category_filter: Choice field for filtering by category
        priority_filter: Choice field for filtering by priority
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
        ),
        help_text="Search in note titles and content"
    )

    category_filter = forms.ChoiceField(
        choices=[('', 'All Categories')] + Note.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        help_text="Filter by note category"
    )

    priority_filter = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Note.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        help_text="Filter by note priority"
    )