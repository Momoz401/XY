# Generated by Django 4.1 on 2024-06-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0045_alter_salary_by_plople_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary_by_daily',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('工人', models.CharField(max_length=100)),
                ('基地', models.CharField(max_length=100)),
                ('负责人', models.CharField(max_length=100)),
                ('月份', models.CharField(max_length=6)),
                ('day_1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_3', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_4', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_5', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_6', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_7', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_8', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_9', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_10', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_11', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_12', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_13', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_14', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_15', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_16', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_17', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_18', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_19', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_20', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_21', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_22', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_23', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_24', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_25', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_26', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_27', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_28', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_29', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_30', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_31', models.DecimalField(decimal_places=2, max_digits=10)),
                ('合计', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': '每日工资表',
                'verbose_name_plural': '每日工资表',
                'db_table': 'views_每日工资表',
                'managed': False,
            },
        ),
    ]