# Generated by Django 3.2.9 on 2022-04-11 14:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crypto', '0011_auto_20220411_1606'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transcaction',
            new_name='Transaction',
        ),
    ]