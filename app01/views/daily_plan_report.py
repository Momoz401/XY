from django.shortcuts import render
from app01.models import DailyPlan, Plant_batch
from django.db.models import Max
from django.utils import timezone

def daily_plan_rate(request):
    # 获取所有可用的月份，格式为 YYYY-MM
    available_months = DailyPlan.objects.dates('种植日期', 'month')

    # 获取最新的月份
    latest_month = available_months.latest('种植日期') if available_months.exists() else None

    # 获取用户选择的月份，如果没有选择，则默认使用最新的月份
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            selected_month_date = timezone.datetime.strptime(selected_month, '%Y-%m')
            filtered_daily_plans = DailyPlan.objects.filter(
                种植日期__year=selected_month_date.year,
                种植日期__month=selected_month_date.month
            )
        except ValueError:
            # 如果月份格式不正确，默认使用最新的月份
            selected_month = latest_month.strftime('%Y-%m') if latest_month else None
            filtered_daily_plans = DailyPlan.objects.all()
    else:
        selected_month = latest_month.strftime('%Y-%m') if latest_month else None
        if latest_month:
            filtered_daily_plans = DailyPlan.objects.filter(
                种植日期__year=latest_month.year,
                种植日期__month=latest_month.month
            )
        else:
            filtered_daily_plans = DailyPlan.objects.all()

    # 获取实际批次数据，转换为字典，方便快速查找
    plant_batches = Plant_batch.objects.all()
    batch_dict = {batch.批次ID: batch for batch in plant_batches}

    # 处理计划和实际数据的计算
    result = []
    for plan in filtered_daily_plans:
        # 查找匹配的实际批次数据
        batch = batch_dict.get(plan.批次ID)

        # 如果找到匹配的批次，获取实际面积，否则设为 0
        actual_area = batch.面积 if batch else 0

        # 计算完成率
        if plan.面积 > 0:
            completion_rate = (actual_area / plan.面积) * 100
        else:
            completion_rate = 0

        # 将数据添加到 result 列表中
        result.append({
            '批次ID': plan.批次ID,
            '计划日期': plan.种植日期.strftime('%Y年%m月%d日'),  # 格式化日期
            '计划面积': plan.面积,
            '实际面积': actual_area,
            '完成率': round(completion_rate, 2)
        })

    # 格式化可用月份为 "YYYY年MM月"
    formatted_months = [
        month.strftime('%Y年%m月') for month in available_months
    ]

    # 将选择的月份格式化为 "YYYY年MM月" 以在模板中显示
    formatted_selected_month = timezone.datetime.strptime(selected_month, '%Y-%m').strftime('%Y年%m月') if selected_month else '全部'

    context = {
        'result': result,
        'available_months': available_months,
        'formatted_months': formatted_months,
        'selected_month': formatted_selected_month
    }

    return render(request, 'daily_plan_rate.html', context)