"""
App configuration for sticky_notes_app.

This module contains the Django app configuration for the sticky notes
application, defining the app's metadata and initialization settings.
"""

from django.apps import AppConfig


class StickyNotesAppConfig(AppConfig):
    """
    App configuration for the sticky_notes_app.
    
    This class defines the configuration for the sticky notes Django application,
    including the app name, default auto field, and any app-specific settings.
    It's used by Django to manage the application lifecycle and configuration.
    
    Attributes:
        default_auto_field: The default auto field for model primary keys
        name: The full Python path to the application
    """
    
    # The default auto field for model primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The full Python path to the application
    name = 'sticky_notes_app'