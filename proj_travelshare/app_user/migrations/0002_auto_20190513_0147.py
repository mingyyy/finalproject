# Generated by Django 2.2 on 2019-05-13 01:47

from django.db import migrations
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilehost',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profilehost',
            name='address',
            field=django_google_maps.fields.AddressField(max_length=200),
        ),
    ]
