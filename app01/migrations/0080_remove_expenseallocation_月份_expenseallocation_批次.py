# Generated by Django 4.1 on 2024-08-21 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0079_remove_expenseallocation_出勤奖金_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenseallocation',
            name='月份',
        ),
        migrations.AddField(
            model_name='expenseallocation',
            name='批次',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
