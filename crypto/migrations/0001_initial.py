# Generated by Django 3.2.9 on 2022-04-25 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_created', models.DateField()),
                ('time_created', models.TimeField()),
                ('type', models.CharField(max_length=30)),
                ('coin', models.CharField(max_length=30)),
                ('quantityCrypto', models.FloatField()),
                ('price', models.FloatField()),
                ('balance_after', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-day_created', '-time_created'],
            },
        ),
        migrations.CreateModel(
            name='CryptoWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptoName', models.CharField(max_length=30)),
                ('quantityDollars', models.FloatField()),
                ('cryptoQuantity', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['cryptoName'],
            },
        ),
        migrations.CreateModel(
            name='BuyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_created', models.DateField()),
                ('time_created', models.TimeField()),
                ('cryptoQuantity', models.FloatField()),
                ('price', models.FloatField()),
                ('crypto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crypto.cryptowallet')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['crypto', '-day_created', '-time_created'],
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
