# Generated by Django 4.0.1 on 2022-01-25 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models
import rules.contrib.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to=inventory.models.location_image_upload_handler, verbose_name='image')),
                ('address', models.TextField(blank=True, verbose_name='address')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='longitude')),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'alert'), (20, 'warning'), (30, 'normal')], default=30, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('maintenance_team', models.ForeignKey(blank=True, help_text='Team members can view this location.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_maintenance_team', to='common.team', verbose_name='maintenance team')),
                ('management_team', models.ForeignKey(blank=True, help_text='Team members can view, change or delete this location.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_management_team', to='common.team', verbose_name='management team')),
                ('owner', models.ForeignKey(help_text='Owner can view, change or delete this location.', on_delete=django.db.models.deletion.CASCADE, related_name='location_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'ordering': ['status', 'name'],
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(blank=True, null=True, upload_to=inventory.models.object_image_upload_handler, verbose_name='image')),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'alert'), (20, 'warning'), (30, 'normal')], default=30, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object_location', to='inventory.location', verbose_name='location')),
                ('maintenance_team', models.ForeignKey(blank=True, help_text='Team members can view this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object_maintenance_team', to='common.team', verbose_name='maintenance team')),
                ('management_team', models.ForeignKey(blank=True, help_text='Team members can view or update this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='object_management_team', to='common.team', verbose_name='management team')),
                ('owner', models.ForeignKey(help_text='Owner can view, change or delete this object.', on_delete=django.db.models.deletion.CASCADE, related_name='object_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'object',
                'verbose_name_plural': 'objects',
                'ordering': ['status', 'name'],
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
