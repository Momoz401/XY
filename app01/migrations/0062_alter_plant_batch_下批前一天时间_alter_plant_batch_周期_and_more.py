# Generated by Django 4.1 on 2024-07-18 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0061_plant_batch_下批前一天时间_plant_batch_周期_plant_batch_周期批次_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant_batch',
            name='下批前一天时间',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='周期',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='总产量',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='总亩产',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='总周期天数',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='栽种方式',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='正常产量',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='正常亩产',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='采收初期',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='采收末期',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='销毁备注',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='plant_batch',
            name='销毁面积',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
