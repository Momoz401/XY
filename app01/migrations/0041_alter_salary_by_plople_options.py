# Generated by Django 4.1 on 2024-06-06 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0040_salary_by_plople'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary_by_plople',
            options={'managed': False, 'verbose_name': '工资花名册', 'verbose_name_plural': '工资花名册'},
        ),
    ]