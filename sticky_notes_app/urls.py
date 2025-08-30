"""
URL configuration for sticky_notes_app.
"""
from django.urls import path
from . import views

app_name = 'sticky_notes_app'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Note CRUD operations
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('note/new/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/edit/',
         views.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/',
         views.NoteDeleteView.as_view(), name='note_delete'),

    # Additional functionality
    path('note/<int:pk>/archive/', views.note_archive, name='note_archive'),
    path('search/', views.note_search, name='note_search'),
]
