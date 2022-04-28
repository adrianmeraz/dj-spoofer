# Generated by Django 3.2.12 on 2022-04-16 13:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0016_auto_20220414_2228'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='ipfingerprint',
            name='ip_fp_last_ip',
        ),
        migrations.RemoveField(
            model_name='ipfingerprint',
            name='last_ip',
        ),
        migrations.AddField(
            model_name='ipfingerprint',
            name='ips',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.GenericIPAddressField(), default=list, size=None),
        ),
        migrations.AddIndex(
            model_name='ipfingerprint',
            index=models.Index(fields=['city'], name='ip_fp_city'),
        ),
        migrations.AddIndex(
            model_name='ipfingerprint',
            index=models.Index(fields=['country'], name='ip_fp_country'),
        ),
        migrations.AddIndex(
            model_name='ipfingerprint',
            index=models.Index(fields=['isp'], name='ip_fp_isp'),
        ),
    ]
