# Generated by Django 4.1 on 2024-07-18 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0056_alter_plant_batch_采收初期_alter_plant_batch_采收末期'),
    ]

    operations = [
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
    ]
