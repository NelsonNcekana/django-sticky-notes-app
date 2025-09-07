"""
Admin configuration for sticky_notes_app.

This module contains Django admin configurations for the sticky notes
application, providing a comprehensive admin interface for managing notes
with filtering, searching, and bulk operations.
"""

from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Note model.
    
    This class provides a comprehensive admin interface for managing notes
    with features like list display, filtering, searching, and field organization.
    It includes custom methods for handling user permissions and queryset filtering.
    
    Attributes:
        list_display: Fields to display in the admin list view
        list_filter: Fields available for filtering in the admin
        search_fields: Fields searchable in the admin interface
        list_editable: Fields that can be edited directly in the list view
        readonly_fields: Fields that are read-only in the admin
        fieldsets: Organization of fields in the admin form
        list_per_page: Number of items per page in the list view
        date_hierarchy: Field to use for date-based navigation
        ordering: Default ordering for the admin list view
    """

    # Fields to display in the admin list view
    list_display = ('title', 'category', 'priority', 'created_at',
                    'updated_at', 'is_archived')
    
    # Fields available for filtering
    list_filter = ('category', 'priority', 'is_archived', 'created_at',
                   'updated_at')
    
    # Fields searchable in the admin interface
    search_fields = ('title', 'content')
    
    # Fields that can be edited directly in the list view
    list_editable = ('is_archived',)
    
    # Fields that are read-only in the admin form
    readonly_fields = ('created_at', 'updated_at')

    # Organization of fields in the admin form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content')
        }),
        ('Classification', {
            'fields': ('category', 'priority')
        }),
        ('Status', {
            'fields': ('is_archived',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Number of items per page in the list view
    list_per_page = 20
    
    # Field to use for date-based navigation
    date_hierarchy = 'created_at'
    
    # Default ordering for the admin list view
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        """
        Customize the queryset for the admin list view.
        
        This method allows showing all notes including archived ones in the admin,
        providing full administrative control over the note collection.
        
        Args:
            request: The HTTP request object
            
        Returns:
            QuerySet: The queryset to use in the admin interface
        """
        return super().get_queryset(request)

    def get_list_display(self, request):
        """
        Customize the list display based on user permissions.
        
        This method modifies the list display fields based on the user's
        permissions, ensuring that sensitive operations are only available
        to appropriate users.
        
        Args:
            request: The HTTP request object
            
        Returns:
            list: List of fields to display in the admin list view
        """
        list_display = list(super().get_list_display(request))
        if not request.user.is_superuser:
            # Remove is_archived from editable list for non-superusers
            if 'is_archived' in list_display:
                list_display.remove('is_archived')
        return list_display