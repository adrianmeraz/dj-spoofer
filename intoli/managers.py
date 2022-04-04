import random

from django.db import models

from . import exceptions


class ProfileManager(models.Manager):
    SUPPORTED_BROWSERS = ('Chrome', 'Firefox')

    def all_oids(self):
        return super().get_queryset().values_list('oid', flat=True)

    def all_user_agents(self):
        return super().get_queryset().values_list('user_agent', flat=True)

    def all_desktop_profiles(self):
        return super().get_queryset().filter(device_category='desktop', browser__in=self.SUPPORTED_BROWSERS)

    def all_mobile_profiles(self):
        return super().get_queryset().filter(device_category='mobile')

    def random_desktop_profile(self):
        try:
            return self.all_desktop_profiles().order_by('?')[0]
        except Exception:
            raise exceptions.IntoliError('No Desktop Profiles Exist')

    def random_mobile_profile(self):
        try:
            return self.all_mobile_profiles().order_by('?')[0]
        except Exception:
            raise exceptions.IntoliError('No Mobile Profiles Exist')

    def weighted_desktop_profile(self):
        try:
            desktop_profiles = self.all_desktop_profiles()
            weights = [float(p.weight) for p in desktop_profiles]
            return random.choices(population=desktop_profiles, weights=weights, k=1)[0]
        except IndexError:
            raise exceptions.IntoliError('No Desktop Profiles Exist')

    def weighted_mobile_profile(self):
        try:
            mobile_profiles = self.all_mobile_profiles()
            weights = [float(p.weight) for p in mobile_profiles]
            return random.choices(population=mobile_profiles, weights=weights, k=1)[0]
        except IndexError:
            raise exceptions.IntoliError('No Mobile Profiles Exist')

    def bulk_delete(self, oids):
        return super().get_queryset().filter(oid__in=oids).delete()

