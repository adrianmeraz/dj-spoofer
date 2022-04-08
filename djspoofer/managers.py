from django.db import models
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from djspoofer import exceptions
from . import const


class FingerprintManager(models.Manager):
    def all_desktop_profiles(self):
        return super().get_queryset().filter(device_category='desktop', browser__in=const.SUPPORTED_BROWSERS)

    def get_random_desktop_fingerprint(self):
        try:
            return self.all_desktop_profiles().order_by('?')[0]
        except Exception:
            raise exceptions.DJSpooferError('No Desktop Fingerprints Exist')


class ProxyManager(models.Manager):

    def create_general_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.GENERAL.value, *args, **kwargs)

    def create_rotating_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.ROTATING.value, *args, **kwargs)

    def create_sticky_proxy(self, *args, **kwargs):
        return self.create(mode=const.ProxyModes.STICKY.value, *args, **kwargs)

    def get_rotating_proxy(self):
        q_filter = Q(mode=const.ProxyModes.ROTATING.value)
        return super().get_queryset().get(q_filter)

    def get_sticky_proxy(self):
        with transaction.atomic():
            q = Q(mode=const.ProxyModes.STICKY.value)
            q &= (Q(last_used__lt=timezone.now() - F('cooldown')) | Q(last_used=None))

            sticky_proxy = super().get_queryset().select_for_update(skip_locked=True).order_by(
                F('last_used').asc(nulls_first=True)).get(q)

            sticky_proxy.set_last_used()
            return sticky_proxy

    def get_all_urls(self):
        return super().get_queryset().values_list('url', flat=True)
