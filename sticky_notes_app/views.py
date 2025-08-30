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
    """View for displaying list of notes."""
    model = Note
    template_name = 'sticky_notes_app/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        """Filter notes based on search and filter parameters."""
        queryset = Note.objects.filter(is_archived=False)  # type: ignore

        # Get search parameters
        search_query = self.request.GET.get('search_query', '')
        category_filter = self.request.GET.get('category_filter', '')
        priority_filter = self.request.GET.get('priority_filter', '')

        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Apply category filter
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        # Apply priority filter
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """Add search form to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = NoteSearchForm(self.request.GET)
        context['categories'] = Note.CATEGORY_CHOICES
        context['priorities'] = Note.PRIORITY_CHOICES
        return context


class NoteCreateView(CreateView):
    """View for creating new notes."""
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def form_valid(self, form):
        """Handle successful form submission."""
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDetailView(DetailView):
    """View for displaying note details."""
    model = Note
    template_name = 'sticky_notes_app/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        """Only show non-archived notes."""
        return Note.objects.filter(is_archived=False)  # type: ignore


class NoteUpdateView(UpdateView):
    """View for editing notes."""
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        """Only allow editing non-archived notes."""
        return Note.objects.filter(is_archived=False)  # type: ignore

    def form_valid(self, form):
        """Handle successful form submission."""
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors."""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDeleteView(DeleteView):
    """View for deleting notes."""
    model = Note
    template_name = 'sticky_notes_app/note_confirm_delete.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        """Only allow deleting non-archived notes."""
        return Note.objects.filter(is_archived=False)  # type: ignore

    def delete(self, request, *args, **kwargs):
        """Handle successful deletion."""
        messages.success(request, 'Note deleted successfully!')
        return super().delete(request, *args, **kwargs)


def note_archive(request, pk):
    """View for archive notes."""
    note = get_object_or_404(Note, pk=pk)
    note.is_archived = not note.is_archived
    note.save()

    action = "archived" if note.is_archived else "not archived"
    messages.success(request, f'Note {action} successfully!')

    return redirect('sticky_notes_app:note_list')


def note_search(request):
    """View for searching notes."""
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
    """Home view that redirects to note list."""
    return redirect('sticky_notes_app:note_list')
