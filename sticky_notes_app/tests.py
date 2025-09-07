"""
Tests for the sticky_notes_app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Note
from .forms import NoteForm, NoteSearchForm
import datetime


class NoteModelTest(TestCase):
    """Test cases for the Note model."""

    def setUp(self):
        """Set up test data."""
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note content",
            category="personal",
            priority="high"
        )

    def test_note_creation(self):
        """Test that a note can be created with all fields."""
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is a test note content")
        self.assertEqual(self.note.category, "personal")
        self.assertEqual(self.note.priority, "high")
        self.assertFalse(self.note.is_archived)
        self.assertIsInstance(self.note.created_at, datetime.datetime)
        self.assertIsInstance(self.note.updated_at, datetime.datetime)

    def test_note_string_representation(self):
        """Test the __str__ method returns the title."""
        self.assertEqual(str(self.note), "Test Note")

    def test_note_default_values(self):
        """Test default values for optional fields."""
        note = Note.objects.create(            title="Default Note",
            content="Content"
        )
        self.assertEqual(note.category, "other")
        self.assertEqual(note.priority, "medium")
        self.assertFalse(note.is_archived)

    def test_note_choices(self):
        """Test that category and priority choices are valid."""
        valid_categories = [choice[0] for choice in Note.CATEGORY_CHOICES]
        valid_priorities = [choice[0] for choice in Note.PRIORITY_CHOICES]

        self.assertIn(self.note.category, valid_categories)
        self.assertIn(self.note.priority, valid_priorities)

    def test_note_ordering(self):
        """Test that notes are ordered by updated_at descending."""
        note2 = Note.objects.create(            title="Second Note",
            content="Second content"
        )
        note3 = Note.objects.create(            title="Third Note",
            content="Third content"
        )

        # Update the first note to make it most recent
        self.note.save()

        notes = Note.objects.all()
        self.assertEqual(notes[0], self.note)
        self.assertEqual(notes[1], note3)
        self.assertEqual(notes[2], note2)

    def test_note_archiving(self):
        """Test note archiving functionality."""
        self.assertFalse(self.note.is_archived)
        self.note.is_archived = True
        self.note.save()
        self.assertTrue(self.note.is_archived)


class NoteFormTest(TestCase):
    """Test cases for the NoteForm."""

    def test_note_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'title': 'Valid Note',
            'content': 'Valid content for the note',
            'category': 'work',
            'priority': 'urgent'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_note_form_empty_title(self):
        """Test form validation for empty title."""
        form_data = {
            'title': '',
            'content': 'Valid content',
            'category': 'personal',
            'priority': 'medium'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_note_form_whitespace_title(self):
        """Test form validation for whitespace-only title."""
        form_data = {
            'title': '   ',
            'content': 'Valid content',
            'category': 'personal',
            'priority': 'medium'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_note_form_empty_content(self):
        """Test form validation for empty content."""
        form_data = {
            'title': 'Valid Title',
            'content': '',
            'category': 'personal',
            'priority': 'medium'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_note_form_widget_attributes(self):
        """Test that form widgets have correct attributes."""
        form = NoteForm()
        title_widget = form.fields['title'].widget
        content_widget = form.fields['content'].widget

        self.assertIn('form-control', title_widget.attrs['class'])
        self.assertIn('placeholder', title_widget.attrs)
        self.assertIn('maxlength', title_widget.attrs)
        self.assertIn('form-control', content_widget.attrs['class'])
        self.assertIn('rows', content_widget.attrs)


class NoteSearchFormTest(TestCase):
    """Test cases for the NoteSearchForm."""

    def test_search_form_valid_data(self):
        """Test search form with valid data."""
        form_data = {
            'search_query': 'test query',
            'category_filter': 'work',
            'priority_filter': 'high'
        }
        form = NoteSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_empty_data(self):
        """Test search form with empty data."""
        form_data = {}
        form = NoteSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # All fields are optional

    def test_search_form_partial_data(self):
        """Test search form with partial data."""
        form_data = {'search_query': 'test'}
        form = NoteSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class NoteViewsTest(TestCase):
    """Test cases for the Note views."""

    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.note = Note.objects.create(            title="Test Note",
            content="Test content",
            category="personal",
            priority="medium"
        )
        self.note2 = Note.objects.create(            title="Work Note",
            content="Work related content",
            category="work",
            priority="high"
        )

    def test_home_view(self):
        """Test the home view."""
        response = self.client.get(reverse('sticky_notes_app:home'))
        self.assertEqual(response.status_code, 302)  # Redirects to note list
        self.assertEqual(response.url, reverse('sticky_notes_app:note_list'))

    def test_note_list_view(self):
        """Test the note list view."""
        response = self.client.get(reverse('sticky_notes_app:note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/note_list.html')
        self.assertContains(response, "Test Note")
        self.assertContains(response, "Work Note")

    def test_note_list_view_with_search(self):
        """Test note list view with search query."""
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'search_query': 'Test'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertNotContains(response, "Work Note")

    def test_note_list_view_with_category_filter(self):
        """Test note list view with category filter."""
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'category_filter': 'work'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work Note")
        self.assertNotContains(response, "Test Note")

    def test_note_list_view_with_priority_filter(self):
        """Test note list view with priority filter."""
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'priority_filter': 'high'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work Note")
        self.assertNotContains(response, "Test Note")

    def test_note_create_view_get(self):
        """Test note create view GET request."""
        response = self.client.get(reverse('sticky_notes_app:note_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/note_form.html')
        self.assertContains(response, "Create New Note")

    def test_note_create_view_post_valid(self):
        """Test note create view POST with valid data."""
        form_data = {
            'title': 'New Note',
            'content': 'New note content',
            'category': 'ideas',
            'priority': 'low'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Check if note was created
        new_note = Note.objects.get(title='New Note')
        self.assertEqual(new_note.content, 'New note content')
        self.assertEqual(new_note.category, 'ideas')
        self.assertEqual(new_note.priority, 'low')

    def test_note_create_view_post_invalid(self):
        """Test note create view POST with invalid data."""
        form_data = {
            'title': '',  # Invalid: empty title
            'content': 'Valid content',
            'category': 'personal',
            'priority': 'medium'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertContains(response, "This field is required")  # Django's default error message

    def test_note_detail_view(self):
        """Test the note detail view."""
        response = self.client.get(
            reverse('sticky_notes_app:note_detail', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/note_detail.html')
        self.assertContains(response, "Test Note")
        self.assertContains(response, "Test content")

    def test_note_detail_view_nonexistent(self):
        """Test note detail view with non-existent note."""
        response = self.client.get(
            reverse('sticky_notes_app:note_detail', args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_note_update_view_get(self):
        """Test note update view GET request."""
        response = self.client.get(
            reverse('sticky_notes_app:note_update', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/note_form.html')
        self.assertContains(response, "Edit Note")

    def test_note_update_view_post_valid(self):
        """Test note update view POST with valid data."""
        form_data = {
            'title': 'Updated Note',
            'content': 'Updated content',
            'category': 'shopping',
            'priority': 'urgent'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_update', args=[self.note.pk]),
            form_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Check if note was updated
        updated_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(updated_note.title, 'Updated Note')
        self.assertEqual(updated_note.content, 'Updated content')
        self.assertEqual(updated_note.category, 'shopping')
        self.assertEqual(updated_note.priority, 'urgent')

    def test_note_delete_view_get(self):
        """Test note delete view GET request."""
        response = self.client.get(
            reverse('sticky_notes_app:note_delete', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/note_confirm_delete.html')
        self.assertContains(response, "Confirm Deletion")

    def test_note_delete_view_post(self):
        """Test note delete view POST request."""
        note_pk = self.note.pk
        response = self.client.post(
            reverse('sticky_notes_app:note_delete', args=[note_pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Check if note was deleted
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=note_pk)
    def test_note_archive_view(self):
        """Test note archive functionality."""
        self.assertFalse(self.note.is_archived)

        response = self.client.get(
            reverse('sticky_notes_app:note_archive', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Check if note was archived
        archived_note = Note.objects.get(pk=self.note.pk)
        self.assertTrue(archived_note.is_archived)

    def test_note_search_view(self):
        """Test note search functionality."""
        response = self.client.get(
            reverse('sticky_notes_app:note_search'),
            {'search_query': 'Test', 'category_filter': 'personal'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes_app/search_results.html')
        self.assertContains(response, "Test Note")
        self.assertNotContains(response, "Work Note")


class NoteURLsTest(TestCase):
    """Test cases for URL patterns."""

    def test_home_url(self):
        """Test home URL pattern."""
        url = reverse('sticky_notes_app:home')
        self.assertEqual(url, '/')

    def test_note_list_url(self):
        """Test note list URL pattern."""
        url = reverse('sticky_notes_app:note_list')
        self.assertEqual(url, '/notes/')

    def test_note_create_url(self):
        """Test note create URL pattern."""
        url = reverse('sticky_notes_app:note_create')
        self.assertEqual(url, '/note/new/')

    def test_note_detail_url(self):
        """Test note detail URL pattern."""
        url = reverse('sticky_notes_app:note_detail', args=[1])
        self.assertEqual(url, '/note/1/')

    def test_note_update_url(self):
        """Test note update URL pattern."""
        url = reverse('sticky_notes_app:note_update', args=[1])
        self.assertEqual(url, '/note/1/edit/')

    def test_note_delete_url(self):
        """Test note delete URL pattern."""
        url = reverse('sticky_notes_app:note_delete', args=[1])
        self.assertEqual(url, '/note/1/delete/')

    def test_note_archive_url(self):
        """Test note archive URL pattern."""
        url = reverse('sticky_notes_app:note_archive', args=[1])
        self.assertEqual(url, '/note/1/archive/')

    def test_note_search_url(self):
        """Test note search URL pattern."""
        url = reverse('sticky_notes_app:note_search')
        self.assertEqual(url, '/search/')


class NoteIntegrationTest(TestCase):
    """Integration tests for complete workflows."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

    def test_complete_note_workflow(self):
        """Test complete note creation, editing, and deletion workflow."""
        # 1. Create a note
        form_data = {
            'title': 'Workflow Note',
            'content': 'This is a test workflow',
            'category': 'work',
            'priority': 'high'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 302)

        # Get the created note
        note = Note.objects.get(title='Workflow Note')
        self.assertEqual(note.content, 'This is a test workflow')

        # 2. Edit the note
        edit_data = {
            'title': 'Updated Workflow Note',
            'content': 'This is an updated workflow',
            'category': 'ideas',
            'priority': 'medium'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_update', args=[note.pk]),
            edit_data
        )
        self.assertEqual(response.status_code, 302)

        # Check updates
        updated_note = Note.objects.get(pk=note.pk)
        self.assertEqual(updated_note.title, 'Updated Workflow Note')
        self.assertEqual(updated_note.category, 'ideas')

        # 3. Archive the note
        response = self.client.get(
            reverse('sticky_notes_app:note_archive', args=[note.pk])
        )
        self.assertEqual(response.status_code, 302)

        archived_note = Note.objects.get(pk=note.pk)
        self.assertTrue(archived_note.is_archived)

        # 4. Unarchive the note (so we can delete it)
        response = self.client.get(
            reverse('sticky_notes_app:note_archive', args=[note.pk])
        )
        self.assertEqual(response.status_code, 302)

        unarchived_note = Note.objects.get(pk=note.pk)
        self.assertFalse(unarchived_note.is_archived)

        # 5. Delete the note
        response = self.client.post(
            reverse('sticky_notes_app:note_delete', args=[note.pk])
        )
        self.assertEqual(response.status_code, 302)

        # Verify deletion
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=note.pk)
    def test_search_and_filter_workflow(self):
        """Test search and filter functionality workflow."""
        # Create multiple notes
        Note.objects.create(            title="Personal Task",
            content="Personal task content",
            category="personal",
            priority="low"
        )
        Note.objects.create(            title="Work Task",
            content="Work task content",
            category="work",
            priority="high"
        )
        Note.objects.create(            title="Shopping List",
            content="Shopping items",
            category="shopping",
            priority="medium"
        )

        # Test search
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'search_query': 'Task'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Personal Task")
        self.assertContains(response, "Work Task")
        self.assertNotContains(response, "Shopping List")

        # Test category filter
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'category_filter': 'work'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work Task")
        self.assertNotContains(response, "Personal Task")
        self.assertNotContains(response, "Shopping List")

        # Test priority filter
        response = self.client.get(
            reverse('sticky_notes_app:note_list'),
            {'priority_filter': 'high'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work Task")
        self.assertNotContains(response, "Personal Task")
        self.assertNotContains(response, "Shopping List")


class NoteEdgeCasesTest(TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.note = Note.objects.create(            title="Edge Case Note",
            content="Edge case content",
            category="other",
            priority="medium"
        )

    def test_note_with_very_long_title(self):
        """Test note creation with maximum length title."""
        long_title = "A" * 200  # Maximum allowed length
        form_data = {
            'title': long_title,
            'content': 'Content for long title note',
            'category': 'personal',
            'priority': 'low'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 302)

        created_note = Note.objects.get(title=long_title)
        self.assertEqual(len(created_note.title), 200)

    def test_note_with_very_long_content(self):
        """Test note creation with very long content."""
        long_content = "Long content " * 1000  # Very long content
        form_data = {
            'title': 'Long Content Note',
            'content': long_content.strip(),  # Remove trailing whitespace
            'category': 'ideas',
            'priority': 'medium'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 302)

        created_note = Note.objects.get(title='Long Content Note')
        self.assertEqual(created_note.content, long_content.strip())

    def test_note_with_special_characters(self):
        """Test note creation with special characters."""
        special_title = "Note with @#$%^&*()_+-=[]{}|;':\",./<>?"
        special_content = "Content with émojis 🚀 and symbols ©®™"

        form_data = {
            'title': special_title,
            'content': special_content,
            'category': 'personal',
            'priority': 'high'
        }
        response = self.client.post(
            reverse('sticky_notes_app:note_create'),
            form_data
        )
        self.assertEqual(response.status_code, 302)

        created_note = Note.objects.get(title=special_title)
        self.assertEqual(created_note.content, special_content)

    def test_concurrent_note_operations(self):
        """Test concurrent operations on the same note."""
        # Simulate concurrent updates
        note1 = Note.objects.get(pk=self.note.pk)
        note2 = Note.objects.get(pk=self.note.pk)
        note1.title = "First Update"
        note1.save()

        note2.title = "Second Update"
        note2.save()

        # Both should be saved
        final_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(final_note.title, "Second Update")

    def test_note_ordering_with_same_timestamp(self):
        """Test note ordering when multiple notes have same timestamp."""
        # Create notes with same timestamp
        timestamp = timezone.now()
        note1 = Note.objects.create(            title="First Note",
            content="First content",
            created_at=timestamp,
            updated_at=timestamp
        )
        note2 = Note.objects.create(            title="Second Note",
            content="Second content",
            created_at=timestamp,
            updated_at=timestamp
        )

        notes = Note.objects.all()        # Should maintain creation order when timestamps are identical
        self.assertIn(note1, notes)
        self.assertIn(note2, notes)
