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

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return str(self.title)

    def get_priority_color(self):
        priority_colors = {
            'low': 'priority-low',
            'medium': 'priority-medium',
            'high': 'priority-high',
            'urgent': 'priority-urgent',
        }
        return priority_colors.get(self.priority, 'priority-medium')

    def get_category_color(self):
        category_colors = {
            'personal': 'category-personal',
            'work': 'category-work',
            'shopping': 'category-shopping',
            'ideas': 'category-ideas',
            'reminders': 'category-reminders',
            'other': 'category-other',
        }
        return category_colors.get(self.category, 'category-other')
