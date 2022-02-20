import datetime

from django.db import models
from django.utils import timezone
from djstarter.models import BaseModel

from . import const, managers


class Proxy(BaseModel):
    objects = managers.ProxyManager()

    url = models.TextField(unique=True, blank=False)
    mode = models.IntegerField(default=const.ProxyModes.GENERAL.value, choices=const.ProxyModes.choices())
    country = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    last_used = models.DateTimeField(blank=True, null=True)
    used_count = models.IntegerField(default=0)
    cooldown = models.DurationField(default=datetime.timedelta(minutes=10))

    class Meta:
        db_table = 'djspoofer_proxy'
        ordering = ['url']
        app_label = 'djspoofer'

    def __str__(self):
        return f'Proxy: {self.url} - {self.pretty_mode}'

    @property
    def is_on_cooldown(self):
        if self.last_used:
            return self.last_used > timezone.now() - self.cooldown
        return False

    @property
    def pretty_mode(self):
        return self.get_mode_display()

    def set_last_used(self):
        self.last_used = timezone.now()
        self.used_count += 1
        self.save()


class Fingerprint(BaseModel):
    objects = managers.FingerprintManager()

    device_category = models.CharField(max_length=16)
    platform = models.CharField(max_length=16)
    screen_height = models.IntegerField()
    screen_width = models.IntegerField()
    user_agent = models.TextField()
    viewport_height = models.IntegerField()
    viewport_width = models.IntegerField()
    proxy = models.ForeignKey(to=Proxy, related_name='fingerprints', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'djspoofer_fingerprint'
        ordering = ['-created']
        app_label = 'djspoofer'

        indexes = [
            models.Index(fields=['device_category', ], name='fp_device_category_index'),
            models.Index(fields=['platform', ], name='fp_platform_index'),
        ]

    def __str__(self):
        return f'Fingerprint -> user_agent: {self.user_agent}'

    @property
    def is_desktop(self):
        return self.device_category == 'desktop'

    @property
    def is_mobile(self):
        return self.device_category == 'mobile'
