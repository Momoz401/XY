# Generated by Django 4.1 on 2024-10-21 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0088_remove_userinfo_account_userinfo_bank_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategoryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('category_level', models.IntegerField(choices=[(1, '一级分类'), (2, '二级分类')], verbose_name='分类级别')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='app01.jobcategoryinfo', verbose_name='父分类')),
            ],
        ),
        migrations.CreateModel(
            name='JobTypeDetailInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=50, verbose_name='工种名称')),
                ('job_level', models.IntegerField(choices=[(1, '一级工种'), (2, '二级工种')], verbose_name='工种级别')),
                ('job_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.jobcategoryinfo', verbose_name='所属二级分类')),
                ('parent_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_work_types', to='app01.jobtypedetailinfo', verbose_name='父工种')),
            ],
        ),
    ]