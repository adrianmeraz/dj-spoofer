from django.db import models
from djstarter.models import BaseModel

from . import managers


class Profile(BaseModel):
    objects = managers.ProfileManager()

    browser = models.CharField(max_length=32)
    device_category = models.CharField(max_length=32)
    os = models.CharField(max_length=32)
    platform = models.CharField(max_length=32)
    screen_height = models.IntegerField()
    screen_width = models.IntegerField()
    user_agent = models.TextField()
    viewport_height = models.IntegerField()
    viewport_width = models.IntegerField()
    weight = models.DecimalField(max_digits=25, decimal_places=24)

    class Meta:
        db_table = 'intoli_profile'
        ordering = ['-weight']
        app_label = 'intoli'

        indexes = [
            models.Index(fields=['browser', ], name='profile_browser'),
            models.Index(fields=['device_category', ], name='profile_device_category'),
            models.Index(fields=['os', ], name='profile_os'),
            models.Index(fields=['platform', ], name='profile_platform'),
        ]

    def __str__(self):
        return (f'Profile -> user_agent: {self.user_agent}, device_category: {self.device_category}, '
                f'platform: {self.platform}')

    @property
    def is_desktop(self):
        return self.device_category == 'desktop'

    @property
    def is_mobile(self):
        return self.device_category == 'mobile'
