"""
Models for the sticky_notes_app.
"""
from django.db import models


class Note(models.Model):
    """Model for sticky notes with all required fields."""

    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('shopping', 'Shopping'),
        ('ideas', 'Ideas'),
        ('reminders', 'Reminders'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200, help_text="Note title")
    content = models.TextField(help_text="Note content")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Note category"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Priority level"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp"
    )
    is_archived = models.BooleanField(
        default=False,
        help_text="Archive status"
    )

    class Meta:
        """Meta configuration for Note."""
        ordering = ['-updated_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return str(self.title)

    def get_priority_color(self):
        """Return CSS class for priority styling."""
        priority_colors = {
            'low': 'priority-low',
            'medium': 'priority-medium',
            'high': 'priority-high',
            'urgent': 'priority-urgent',
        }
        return priority_colors.get(self.priority, 'priority-medium')

    def get_category_color(self):
        """Return CSS class for category styling."""
        category_colors = {
            'personal': 'category-personal',
            'work': 'category-work',
            'shopping': 'category-shopping',
            'ideas': 'category-ideas',
            'reminders': 'category-reminders',
            'other': 'category-other',
        }
        return category_colors.get(self.category, 'category-other')
