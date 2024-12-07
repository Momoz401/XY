# Generated by Django 4.1 on 2024-11-02 05:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0098_plant_batch_种植日期_alter_depreciationallocation_月份'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant_batch',
            name='基地',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='uploader',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='批次ID',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='种植日期',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
