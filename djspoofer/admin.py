from django.conf.locale.en import formats as en_formats
from django.contrib import admin
from djstarter import admin as core_admin

from . import const
from .models import Fingerprint, Proxy

en_formats.DATETIME_FORMAT = "M d y H:i"


@admin.register(Fingerprint)
class FingerprintAdmin(core_admin.BaseAdmin):
    list_display = ['created', 'device_category', 'platform', 'user_agent']
    list_filter = ('device_category', 'platform',)
    ordering = ['-created']
    search_fields = ['user_agent']

    show_full_result_count = False

    def bulk_delete(self, request, queryset):
        queryset.delete()

    bulk_delete.short_description = 'Bulk Delete'

    actions = ['export_as_csv', bulk_delete]


@admin.register(Proxy)
class ProxyAdmin(core_admin.BaseAdmin):
    list_display = ['url', 'mode', 'cooldown', 'last_used', 'used_count', 'country', 'city']
    list_filter = ('mode', 'country', 'city')
    ordering = ['mode', 'url']
    search_fields = ['url']

    show_full_result_count = False
    read_only_exclude = ('url', 'mode', 'country')

    def set_rotating(self, request, queryset):
        queryset.update(mode=const.ProxyModes.ROTATING.value)

    set_rotating.short_description = 'Set as Rotating'

    def set_sticky(self, request, queryset):
        queryset.update(mode=const.ProxyModes.STICKY.value)

    set_sticky.short_description = 'Set as Sticky'

    def set_general(self, request, queryset):
        queryset.update(mode=const.ProxyModes.GENERAL.value)

    set_general.short_description = 'Set as General'

    def bulk_delete(self, request, queryset):
        queryset.delete()

    bulk_delete.short_description = 'Bulk Delete'

    actions = ['export_as_csv', set_rotating, set_sticky, set_general, bulk_delete]
