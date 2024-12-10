from django.shortcuts import render
from app01.models import DailyPlan, Plant_batch  # 使用 DailyPlan 模型

from django.shortcuts import render
from app01.models import DailyPlan, Plant_batch

def daily_plan_rate(request):
    # 获取所有日计划数据
    daily_plans = DailyPlan.objects.all()

    # 获取实际批次数据，转换为字典，方便快速查找
    plant_batches = Plant_batch.objects.all()
    batch_dict = {batch.批次ID: batch for batch in plant_batches}

    # 处理计划和实际数据的计算
    result = []
    for plan in daily_plans:
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
            '计划日期':plan.种植日期,
            '计划面积': plan.面积,
            '实际面积': actual_area,
            '完成率': round(completion_rate, 2)
        })

    context = {
        'result': result
    }

    return render(request, 'daily_plan_rate.html', context)