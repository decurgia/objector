# Generated by Django 4.0.4 on 2022-05-31 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import maintenance.models
import rules.contrib.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('jsonpath_expression', models.CharField(max_length=200, verbose_name='JSONPath expression')),
                ('condition', models.CharField(choices=[('==', 'equals'), ('!=', 'not equals'), ('<', 'less than'), ('<=', 'less than or equal to'), ('>', 'greater than'), ('>=', 'greater than or equal to')], max_length=2, verbose_name='Condition')),
                ('sensor_value', models.CharField(blank=True, max_length=200, verbose_name='Sensor value')),
                ('amber_value', models.CharField(blank=True, max_length=200, verbose_name='Warning value')),
                ('red_value', models.CharField(blank=True, max_length=200, verbose_name='Alert value')),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Alert'), (20, 'Warning'), (30, 'Normal')], default=30, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trigger_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trigger_sensor', to='inventory.sensor', verbose_name='Sensor')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trigger_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Overdue'), (20, 'Due'), (30, 'Pending'), (40, 'Inactive')], default=30, verbose_name='Status')),
                ('due_at', models.DateTimeField(blank=True, null=True, verbose_name='Due at')),
                ('overdue_at', models.DateTimeField(blank=True, null=True, verbose_name='Overdue at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_object', to='inventory.object', verbose_name='Object')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['status', 'overdue_at', 'due_at', 'updated_at'],
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('image', models.ImageField(blank=True, null=True, upload_to=maintenance.models.journal_image_upload_handler, verbose_name='Image')),
                ('labor_costs', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Labor costs')),
                ('material_costs', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Material costs')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='journal_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_object', to='inventory.object', verbose_name='Object')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='journal_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Journal',
                'verbose_name_plural': 'Journals',
                'ordering': ('-updated_at',),
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
