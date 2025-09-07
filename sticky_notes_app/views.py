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
    model = Note
    template_name = 'sticky_notes_app/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        """Filter notes based on search and filter parameters."""
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
        context = super().get_context_data(**kwargs)
        context['search_form'] = NoteSearchForm(self.request.GET)
        context['categories'] = Note.CATEGORY_CHOICES
        context['priorities'] = Note.PRIORITY_CHOICES
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def form_valid(self, form):
        messages.success(self.request, 'Note created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDetailView(DetailView):
    model = Note
    template_name = 'sticky_notes_app/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(is_archived=False)  # type: ignore


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'sticky_notes_app/note_form.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        return Note.objects.filter(is_archived=False)  # type: ignore

    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'sticky_notes_app/note_confirm_delete.html'
    success_url = reverse_lazy('sticky_notes_app:note_list')

    def get_queryset(self):
        return Note.objects.filter(is_archived=False)  # type: ignore

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Note deleted successfully!')
        return super().delete(request, *args, **kwargs)


def note_archive(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.is_archived = not note.is_archived
    note.save()

    action = "archived" if note.is_archived else "not archived"
    messages.success(request, f'Note {action} successfully!')

    return redirect('sticky_notes_app:note_list')


def note_search(request):
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
    return redirect('sticky_notes_app:note_list')
