from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0117_alter_depreciationallocation_月份'),
    ]

    operations = [
        # 删除视图（避免表结构变更时视图依赖引发错误）
        migrations.RunSQL(
            "DROP VIEW IF EXISTS views_批次计划内成本汇总;",
            reverse_sql="CREATE VIEW views_批次计划内成本汇总 AS SELECT ...;"  # 如果需要支持回滚，填入完整的视图创建SQL
        ),
        migrations.RunSQL(
            "DROP VIEW IF EXISTS views_批次计划内成本;",
            reverse_sql="CREATE VIEW views_批次计划内成本 AS SELECT ...;"  # 填入完整的SQL
        ),
        migrations.RunSQL(
            "DROP VIEW IF EXISTS view_baseinfoworkhour_with_names;",
            reverse_sql="CREATE VIEW view_baseinfoworkhour_with_names AS SELECT ...;"  # 填入完整的SQL
        ),

        # 添加字段
        migrations.AddField(
            model_name='baseinfoworkhour',
            name='上传人',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='上传人'),
        ),
        migrations.AddField(
            model_name='baseinfoworkhour',
            name='上传时间',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='上传时间'),
        ),
        migrations.AddField(
            model_name='baseinfoworkhour',
            name='最后更新时间',
            field=models.DateTimeField(auto_now=True, verbose_name='最后更新时间'),
        ),

        # 重新创建视图
        migrations.RunSQL(
            """
            CREATE VIEW view_baseinfoworkhour_with_names AS
            SELECT
                t.工种ID,
                t.一级工种_id,
                t.二级工种_id,
                t.单价,
                t.单位,
                t.备注,
                t.一级分类_id,
                t.二级分类_id,
                t.默认计入成本,
                jc_primary.category_name AS 一级分类名称,
                jc_secondary.category_name AS 二级分类名称,
                jt_primary.job_name AS 一级工种名称,
                jt_secondary.job_name AS 二级工种名称
            FROM
                main.app01_baseinfoworkhour t
            LEFT JOIN
                main.app01_JobCategoryInfo jc_primary ON t.一级分类_id = jc_primary.id
            LEFT JOIN
                main.app01_JobCategoryInfo jc_secondary ON t.二级分类_id = jc_secondary.id
            LEFT JOIN
                main.app01_JobTypeDetailInfo jt_primary ON t.一级工种_id = jt_primary.id
            LEFT JOIN
                main.app01_JobTypeDetailInfo jt_secondary ON t.二级工种_id = jt_secondary.id;
            """,
            reverse_sql="DROP VIEW IF EXISTS view_baseinfoworkhour_with_names;"
        ),
        migrations.RunSQL(
            """
            CREATE VIEW views_批次计划内成本 AS
            SELECT
                pb.批次ID,
                pb.种植日期,
                pb.一级分类 AS 批次一级分类,
                pb.二级分类 AS 批次二级分类,
                pb.面积,
                biw.二级工种名称,
                biw.单价,
                IFNULL(o.price, 1) AS 计量系数,
                round((pb.面积 * biw.单价 * IFNULL(o.price, 1)),3) AS 计划内成本
            FROM
                main.app01_plant_batch pb
            JOIN
                main.view_baseinfoworkhour_with_names biw ON pb.一级分类 = biw.一级分类名称
            LEFT JOIN
                main.app01_Order o ON pb.一级分类 = o.title
                         AND (CASE
                                 WHEN o.status = 1 THEN '移栽'
                                 WHEN o.status = 2 THEN '采收'
                              END) = biw.一级工种名称
            WHERE
                biw.默认计入成本 = '是';
            """,
            reverse_sql="DROP VIEW IF EXISTS views_批次计划内成本;"
        ),
        migrations.RunSQL(
            """
            CREATE VIEW views_批次计划内成本汇总 AS
            SELECT
                批次ID,
                种植日期,
                批次一级分类,
                批次二级分类,
                面积,
                SUM(计划内成本) AS 总计划内成本
            FROM
                main.views_批次计划内成本
            GROUP BY
                批次ID,
                种植日期,
                批次一级分类,
                批次二级分类,
                面积
            ORDER BY
                批次ID;
            """,
            reverse_sql="DROP VIEW IF EXISTS views_批次计划内成本汇总;"
        )
    ]