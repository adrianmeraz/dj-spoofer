# Generated by Django 3.2.12 on 2022-04-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0009_remove_tlsfingerprint_user_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingerprint',
            name='browser',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fingerprint',
            name='os',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='device_category',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='fingerprint',
            name='platform',
            field=models.CharField(max_length=32),
        ),
    ]
