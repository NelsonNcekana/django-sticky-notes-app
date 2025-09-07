"""
Models for the sticky_notes_app.

This module contains the data models for the sticky notes application,
including the main Note model with all its fields, choices, and methods.
"""

from django.db import models


class Note(models.Model):
    """
    Model representing a sticky note in the application.

    This model stores all the information for a sticky note including
    title, content, category, priority, timestamps, and archive status.

    Attributes:
        title (CharField): The title of the note (max 200 characters)
        content (TextField): The main content/body of the note
        category (CharField): Category classification with predefined choices
        priority (CharField): Priority level with predefined choices
        created_at (DateTimeField): Timestamp when note was created
        updated_at (DateTimeField): Timestamp when note was last modified
        is_archived (BooleanField): Whether the note is archived or not

    Meta:
        ordering: Notes are ordered by updated_at in descending order
        verbose_name: Human-readable name for the model
        verbose_name_plural: Human-readable plural name for the model
    """

    # Category choices for note classification
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('shopping', 'Shopping'),
        ('ideas', 'Ideas'),
        ('reminders', 'Reminders'),
        ('other', 'Other'),
    ]

    # Priority choices for note importance
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(
        max_length=200,
        help_text="The title of the note"
    )
    content = models.TextField(
        help_text="The main content of the note"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Category classification for the note"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Priority level of the note"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the note was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the note was last updated"
    )
    is_archived = models.BooleanField(
        default=False,
        help_text="Whether the note is archived or not"
    )

    class Meta:
        """Meta options for the Note model."""
        ordering = ['-updated_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        """
        String representation of the Note instance.

        Returns:
            str: The title of the note
        """
        return str(self.title)

    def get_priority_color(self):
        """
        Get CSS class name for priority-based styling.

        Returns:
            str: CSS class name corresponding to the note's priority level
        """
        priority_colors = {
            'low': 'priority-low',
            'medium': 'priority-medium',
            'high': 'priority-high',
            'urgent': 'priority-urgent',
        }
        return priority_colors.get(self.priority, 'priority-medium')

    def get_category_color(self):
        """
        Get CSS class name for category-based styling.

        Returns:
            str: CSS class name corresponding to the note's category
        """
        category_colors = {
            'personal': 'category-personal',
            'work': 'category-work',
            'shopping': 'category-shopping',
            'ideas': 'category-ideas',
            'reminders': 'category-reminders',
            'other': 'category-other',
        }
        return category_colors.get(self.category, 'category-other')