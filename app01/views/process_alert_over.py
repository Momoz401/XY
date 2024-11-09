from django.shortcuts import render
from django.db.models import Min
from datetime import timedelta
from app01.models import ProductionWage, Plant_batch, ProcessAlert

def process_alert_overview(request):
    """ 流程预警概览列表 """

    # 获取查询参数
    search_query = request.GET.get('q', '')

    # 获取批次数据
    batch_queryset = Plant_batch.objects.filter(二级分类__contains=search_query).order_by('种植日期')
    alerts = []

    for batch in batch_queryset:
        print(f"批次ID: {batch.批次ID}, 种植日期: {batch.种植日期}")

        # 获取对应的工时记录
        work_records = ProductionWage.objects.filter(批次=batch.批次ID)
        print(f"批次ID: {batch.批次ID}, 关联的工时记录: {work_records}")

        for work_record in work_records:
            # 获取对应的预警配置
            alert_config = ProcessAlert.objects.filter(
                二级分类=work_record.二级分类,
                二级工种=work_record.二级工种
            ).first()
            print(f"二级分类: {work_record.二级分类}, 二级工种: {work_record.二级工种}, 匹配的预警配置: {alert_config}")

            # 如果没有配置，跳过
            if not alert_config:
                continue

            # 计算应执行的最早和最晚日期
            expected_start_date = batch.种植日期 + timedelta(days=alert_config.最小时间)
            expected_end_date = batch.种植日期 + timedelta(days=alert_config.最大时间)
            print(f"应执行日期范围: {expected_start_date} - {expected_end_date}")

            # 获取最早的执行日期
            earliest_date = work_records.filter(
                二级分类=work_record.二级分类,
                二级工种=work_record.二级工种
            ).aggregate(earliest_date=Min('日期'))['earliest_date']
            print(f"最早执行日期: {earliest_date}")

            if not earliest_date:
                continue

            # 初始化警告信息
            # 示例逻辑
            alert = {
                '批次ID': batch.批次ID,
                '二级工种': work_record.二级工种,
                '种植日期': batch.种植日期,
                '最小工种执行时间': alert_config.最小时间,
                '最大工种执行时间': alert_config.最大时间,
                '最早执行日期': batch.种植日期 + timedelta(days=alert_config.最小时间),
                '最晚执行日期': batch.种植日期 + timedelta(days=alert_config.最大时间),
                '实际执行日期': earliest_date,
                '超期状态': '正常',
                '超期天数': 0,
            }

            # 计算日期差异并确定超期状态
            if earliest_date < expected_start_date:
                alert['超期状态'] = '提前超期'
                alert['超期天数'] = (expected_start_date - earliest_date).days
            elif earliest_date > expected_end_date:
                alert['超期状态'] = '延迟超期'
                alert['超期天数'] = (earliest_date - expected_end_date).days

            alerts.append(alert)

    context = {
        'alerts': alerts,
        'search_query': search_query,
    }

    return render(request, 'process_alert_overview.html', context)