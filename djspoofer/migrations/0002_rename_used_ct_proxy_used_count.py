# Generated by Django 3.2.12 on 2022-02-18 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proxy',
            old_name='used_ct',
            new_name='used_count',
        ),
    ]