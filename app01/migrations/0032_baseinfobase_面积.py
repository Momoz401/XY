# Generated by Django 4.1 on 2024-06-03 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0031_alter_productionwage_日期'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseinfobase',
            name='面积',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
