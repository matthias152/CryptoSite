# Generated by Django 3.2.9 on 2022-04-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0017_rename_buyprices_buyprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buyprice',
            options={'ordering': ['crypto']},
        ),
        migrations.AlterModelOptions(
            name='cryptowallet',
            options={'ordering': ['cryptoName']},
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='quantityDollars',
            new_name='price',
        ),
        migrations.AddField(
            model_name='buyprice',
            name='cryptoQuantity',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
    ]
