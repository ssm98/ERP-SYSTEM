# Generated by Django 3.0.3 on 2021-12-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_overtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime',
            name='endtime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='starttime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
