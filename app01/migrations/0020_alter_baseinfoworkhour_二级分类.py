# Generated by Django 4.1 on 2024-05-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0019_alter_baseinfoworkhour_二级分类'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinfoworkhour',
            name='二级分类',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
