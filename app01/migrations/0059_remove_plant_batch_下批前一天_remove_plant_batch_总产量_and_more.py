# Generated by Django 4.1 on 2024-07-18 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0058_alter_planplantbatch_下批前一天时间_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant_batch',
            name='下批前一天',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='总产量',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='总亩产',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='总周期天数',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='批次',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='栽种方式',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='正常产量',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='正常亩产',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='生长周期',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='采收初期',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='采收末期',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='销毁备注',
        ),
        migrations.RemoveField(
            model_name='plant_batch',
            name='销毁面积',
        ),
    ]
