# Generated by Django 4.1 on 2024-07-18 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0053_alter_uploader_update_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant_batch',
            name='下批前一天',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='总产量',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='总亩产',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='总周期天数',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='批次',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='栽种方式',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='正常产量',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='正常亩产',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='生长周期',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='采收初期',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='采收末期',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='销毁备注',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='plant_batch',
            name='销毁面积',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
