# Generated by Django 3.2.9 on 2022-04-26 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_auto_20220425_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cryptowallet',
            name='quantityDollars',
        ),
    ]
