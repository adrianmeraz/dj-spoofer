import datetime
import random

from django.db import models
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from . import const, exceptions


class ProfileManager(models.Manager):
    def all_oids(self):
        return super().get_queryset().values_list('oid', flat=True)

    def all_user_agents(self):
        return super().get_queryset().values_list('user_agent', flat=True)

    def all_desktop_profiles(self):
        return super().get_queryset().filter(device_category='desktop')

    def all_mobile_profiles(self):
        return super().get_queryset().filter(device_category='mobile')

    def random_desktop_profile(self):
        try:
            return random.choice(list(self.all_desktop_profiles()))
        except Exception:
            raise exceptions.DJSpooferError('No Desktop Profiles Exist')

    def random_mobile_profile(self):
        try:
            return random.choice(list(self.all_mobile_profiles()))
        except Exception:
            raise exceptions.DJSpooferError('No Mobile Profiles Exist')

    def weighted_desktop_profile(self):
        try:
            desktop_profiles = self.all_desktop_profiles()
            weights = [float(p.weight) for p in desktop_profiles]
            return random.choices(population=desktop_profiles, weights=weights, k=1)[0]
        except IndexError:
            raise exceptions.DJSpooferError('No Desktop Profiles Exist')

    def weighted_mobile_profile(self):
        try:
            mobile_profiles = self.all_mobile_profiles()
            weights = [float(p.weight) for p in mobile_profiles]
            return random.choices(population=mobile_profiles, weights=weights, k=1)[0]
        except IndexError:
            raise exceptions.DJSpooferError('No Mobile Profiles Exist')

    def older_than_n_minutes(self, minutes=5):
        q = Q(created__lt=timezone.now() - datetime.timedelta(minutes=minutes))
        return super().get_queryset().filter(q)

    def bulk_delete(self, oids):
        return super().get_queryset().filter(oid__in=oids).delete()


class ProxyManager(models.Manager):
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
