# Generated by Django 4.2.13 on 2024-05-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0023_productionwage_工人'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionwage',
            name='工价',
            field=models.FloatField(null=True),
        ),
    ]
