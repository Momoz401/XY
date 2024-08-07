# Generated by Django 4.1 on 2024-07-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0069_lossreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salesperson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('姓名', models.CharField(max_length=255, verbose_name='姓名')),
                ('所属公司', models.CharField(max_length=255, verbose_name='所属公司')),
                ('电话', models.CharField(max_length=20, verbose_name='电话')),
            ],
            options={
                'verbose_name': '销售人员',
                'verbose_name_plural': '销售人员',
            },
        ),
    ]
