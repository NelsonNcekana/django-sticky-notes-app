"""
Views for the sticky_notes_app.

This module contains all the view classes and functions for the sticky notes
application, including class-based views for CRUD operations and function-based
views for additional functionality like archiving and searching.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm, NoteSearchForm


class NoteListView(ListView):
    """
    View for displaying a list of notes with search and filter capabilities.
    """
    model = Note
    template_name = 'sticky_notes_app/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        """
        Filter notes based on search and filter parameters.

        Returns:
            QuerySet: Filtered queryset of non-archived notes
        """
        queryset = Note.objects.filter(is_archived=False)

        search_query = self.request.GET.get('search_query', '')
        category_filter = self.request.GET.get('category_filter', '')
        priority_filter = self.request.GET.get('priority_filter', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        if category_filter:
            queryset = queryset.filter(category=category_filter)

        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the template.

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            dict: Context dictionary with search form and choices
        """
        context = super().get_context_data(**kwargs)
        context['search_form'] = NoteSearchForm(self.request.GET)
        context['categories'] = Note.CATEGORY_CHOICES
        context['priorities'] = Note.PRIORITY_CHOICES
        return context


class NoteCreateView(CreateView):
    """
    View for creating new notes.

    This view handles the creation of new notes using the NoteForm.
    It provides success and error messages to the user.

    Attributes:
        model: The Note model to create
        form_class: Form class to use for note creation
        template_name: Template used to render the form
        success_url: URL to redirect to after successful creation
    """
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def form_valid(self, form):
        """
        Handle valid form submission.

        Args:
            form: The validated form instance

        Returns:
            HttpResponseRedirect: Redirect to success URL
        """
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Args:
            form: The invalid form instance

        Returns:
            HttpResponse: Response with form errors
        """
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDetailView(DetailView):
    """
    View for displaying a single note's details.

    This view displays the full details of a specific note.
    Only non-archived notes are accessible through this view.

    Attributes:
        model: The Note model to display
        template_name: Template used to render the detail view
        context_object_name: Name of the context variable containing the note
    """
    model = Note
    template_name = 'sticky_notes_app/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        """
        Filter queryset to only include non-archived notes.

        Returns:
            QuerySet: Filtered queryset of non-archived notes
        """
        return Note.objects.filter(is_archived=False)  # type: ignore


class NoteUpdateView(UpdateView):
    """
    View for updating existing notes.

    This view handles the editing of existing notes using the NoteForm.
    It provides success and error messages to the user.
    Only non-archived notes can be updated.

    Attributes:
        model: The Note model to update
        form_class: Form class to use for note editing
        template_name: Template used to render the form
        success_url: URL to redirect to after successful update
    """
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        """
        Filter queryset to only include non-archived notes.

        Returns:
            QuerySet: Filtered queryset of non-archived notes
        """
        return Note.objects.filter(is_archived=False)  # type: ignore

    def form_valid(self, form):
        """
        Handle valid form submission.

        Args:
            form: The validated form instance

        Returns:
            HttpResponseRedirect: Redirect to success URL
        """
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Args:
            form: The invalid form instance

        Returns:
            HttpResponse: Response with form errors
        """
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDeleteView(DeleteView):
    """
    View for deleting notes.

    This view handles the deletion of notes with confirmation.
    It provides success messages to the user.
    Only non-archived notes can be deleted.

    Attributes:
        model: The Note model to delete
        template_name: Template used to render the confirmation page
        success_url: URL to redirect to after successful deletion
    """
    model = Note
    template_name = 'sticky_notes_app/note_confirm_delete.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        """
        Filter queryset to only include non-archived notes.

        Returns:
            QuerySet: Filtered queryset of non-archived notes
        """
        return Note.objects.filter(is_archived=False)  # type: ignore

    def delete(self, request, *args, **kwargs):
        """
        Handle note deletion.

        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to success URL
        """
        messages.success(request, 'Note deleted successfully!')
        return super().delete(request, *args, **kwargs)


def note_archive(request, pk):
    """
    Toggle the archive status of a note.

    This function-based view toggles the archive status of a note.
    If the note is currently archived, it will be unarchived, and vice versa.

    Args:
        request: The HTTP request object
        pk (int): Primary key of the note to archive/unarchive

    Returns:
        HttpResponseRedirect: Redirect to the note list page
    """
    note = get_object_or_404(Note, pk=pk)
    note.is_archived = not note.is_archived
    note.save()

    action = "archived" if note.is_archived else "not archived"
    messages.success(request, f'Note {action} successfully!')

    return redirect('sticky_notes_app:note_list')


def note_search(request):
    """
    Handle note search functionality.

    This function-based view processes search queries and filters notes
    based on search terms, category, and priority. It renders the search
    results in a dedicated template.

    Args:
        request: The HTTP request object containing search parameters

    Returns:
        HttpResponse: Rendered search results page
    """
    form = NoteSearchForm(request.GET)
    notes = Note.objects.filter(is_archived=False)  # type: ignore

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        category_filter = form.cleaned_data.get('category_filter')
        priority_filter = form.cleaned_data.get('priority_filter')

        if search_query:
            notes = notes.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        if category_filter:
            notes = notes.filter(category=category_filter)

        if priority_filter:
            notes = notes.filter(priority=priority_filter)

    context = {
        'notes': notes,
        'search_form': form,
        'categories': Note.CATEGORY_CHOICES,
        'priorities': Note.PRIORITY_CHOICES,
    }

    return render(request, 'sticky_notes_app/search_results.html', context)


def home(request):
    """
    Home page view that redirects to the note list.

    This simple function-based view serves as the home page and redirects
    users to the main note list view.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponseRedirect: Redirect to the note list page
    """
    return redirect('sticky_notes_app:note_list')