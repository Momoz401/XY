# Generated by Django 4.1 on 2024-12-07 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0126_alter_customer_创建时间'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('渠道名称', models.CharField(max_length=255, unique=True, verbose_name='渠道名称')),
                ('地区', models.CharField(max_length=255, verbose_name='地区')),
                ('联系人', models.CharField(max_length=255, verbose_name='联系人')),
                ('插入时间', models.DateTimeField(auto_now_add=True, verbose_name='插入时间')),
            ],
            options={
                'verbose_name': '报价渠道信息',
            },
        ),
    ]
