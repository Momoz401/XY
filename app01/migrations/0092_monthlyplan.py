# Generated by Django 4.1 on 2024-10-22 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0091_alter_dailypricereport_日期'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('日期', models.DateField(verbose_name='日期')),
                ('面积', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='面积')),
                ('周期', models.IntegerField(verbose_name='周期')),
                ('地块', models.CharField(max_length=255, verbose_name='地块')),
                ('二级分类', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.jobcategoryinfo', verbose_name='二级分类')),
                ('基地', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.baseinfobase', verbose_name='基地')),
            ],
            options={
                'verbose_name': '月度计划',
                'verbose_name_plural': '月度计划',
            },
        ),
    ]
