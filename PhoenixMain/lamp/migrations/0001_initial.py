# Generated by Django 4.2.5 on 2023-10-31 18:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lamps',
            fields=[
                ('ipaddressV4', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('macaddress', models.CharField(max_length=12)),
                ('state', models.BooleanField(default=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
