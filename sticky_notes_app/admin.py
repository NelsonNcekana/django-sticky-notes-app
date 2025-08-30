from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin configuration for Note model."""

    list_display = ('title', 'category', 'priority', 'created_at',
                    'updated_at', 'is_archived')
    list_filter = ('category', 'priority', 'is_archived', 'created_at',
                   'updated_at')
    search_fields = ('title', 'content')
    list_editable = ('is_archived',)
    readonly_fields = ('created_at', 'updated_at')

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

    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        """Show all notes including archived ones in admin."""
        return super().get_queryset(request)

    def get_list_display(self, request):
        """Customize list display based on user permissions."""
        list_display = list(super().get_list_display(request))
        if not request.user.is_superuser:
            # Remove is_archived from editable list for non-superusers
            if 'is_archived' in list_display:
                list_display.remove('is_archived')
        return list_display
