# Generated by Django 3.2.13 on 2022-05-15 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0004_h2fingerprint_priority_frames'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='h2fingerprint',
            name='priority_depends_on_id',
        ),
        migrations.RemoveField(
            model_name='h2fingerprint',
            name='priority_exclusive',
        ),
        migrations.RemoveField(
            model_name='h2fingerprint',
            name='priority_stream_id',
        ),
        migrations.RemoveField(
            model_name='h2fingerprint',
            name='priority_weight',
        ),
        migrations.AddField(
            model_name='h2fingerprint',
            name='headers_priority_flags',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
