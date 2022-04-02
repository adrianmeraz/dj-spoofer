from django.conf.locale.en import formats as en_formats
from django.contrib import admin

from djstarter import admin as core_admin
from .models import Profile

en_formats.DATETIME_FORMAT = "M d y H:i"


@admin.register(Profile)
class ProfileAdmin(core_admin.BaseAdmin):
    list_display = ['created', 'device_category', 'platform', 'user_agent', 'weight']
    list_filter = ('device_category', 'platform',)
    ordering = ['-created']
    search_fields = ['user_agent']

    show_full_result_count = False

    def bulk_delete(self, request, queryset):
        queryset.delete()

    bulk_delete.short_description = 'Bulk Delete'

    actions = ['export_as_csv', bulk_delete]
