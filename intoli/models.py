from django.db import models
from djstarter.models import BaseModel

from . import managers


class Profile(BaseModel):
    objects = managers.ProfileManager()

    device_category = models.CharField(max_length=16)
    platform = models.CharField(max_length=16)
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
            models.Index(fields=['device_category', ], name='device_category_index'),
            models.Index(fields=['platform', ], name='platform_index'),
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


