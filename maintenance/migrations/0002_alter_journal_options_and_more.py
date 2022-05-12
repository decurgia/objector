# Generated by Django 4.0.4 on 2022-05-12 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterField(
            model_name='trigger',
            name='jsonpath_expression',
            field=models.CharField(max_length=200, verbose_name='JSONPath expression'),
        ),
    ]
