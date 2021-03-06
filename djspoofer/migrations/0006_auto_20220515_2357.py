# Generated by Django 3.2.13 on 2022-05-15 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0005_auto_20220515_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='h2fingerprint',
            name='headers_priority_flags',
        ),
        migrations.AddField(
            model_name='h2fingerprint',
            name='header_priority_depends_on_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='h2fingerprint',
            name='header_priority_exclusive_bit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='h2fingerprint',
            name='header_priority_stream_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='h2fingerprint',
            name='header_priority_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
