# Generated by Django 4.1 on 2024-06-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0047_workhour_by_daily'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workhour_by_daily',
            options={'managed': False, 'verbose_name': '每月工时表', 'verbose_name_plural': '每月工时表'},
        ),
        migrations.AddField(
            model_name='baseinfoworkhour',
            name='默认计入成本',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.CharField(max_length=64, verbose_name='上传时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '移栽'), (2, '采收')], default=1, verbose_name='类型'),
        ),
        migrations.AlterModelTable(
            name='workhour_by_daily',
            table='views_每月工时表',
        ),
    ]
