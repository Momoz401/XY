import csv

from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce, Cast, TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl.workbook import Workbook

from app01.models import MonthlyPlan, DailyPlan


def monthly_plan_rate(request):
    # 获取所有不重复的月份
    unique_months = MonthlyPlan.objects.annotate(month=TruncMonth('日期')).values('month').distinct()

    # 获取用户选择的月份（从查询参数中获取）
    selected_month = request.GET.get('q', '')

    # 按照用户选择的月份进行过滤
    if selected_month:
        year, month = selected_month.split('-')
        monthly_plans = MonthlyPlan.objects.filter(日期__year=year, 日期__month=month)
    else:
        monthly_plans = MonthlyPlan.objects.all()

    # 准备统计结果
    report_data = []

    for monthly_plan in monthly_plans:
        # 获取二级分类名称
        category_name = monthly_plan.二级分类.category_name
        未达成反馈 = monthly_plan.未达成反馈

        # 按月份和二级分类查询日计划完成情况
        daily_plans = DailyPlan.objects.filter(
            种植日期__year=monthly_plan.日期.year,
            种植日期__month=monthly_plan.日期.month,
            批次ID__contains=category_name
        )

        # 统计日计划的总面积
        total_daily_plan_area = daily_plans.aggregate(
            total=Coalesce(Sum(Cast('面积', output_field=DecimalField())), Value(0, output_field=DecimalField()))
        )['total']

        # 计算计划实现率
        if monthly_plan.面积 > 0:
            completion_rate = round(float(total_daily_plan_area / monthly_plan.面积 * 100), 2)
        else:
            completion_rate = 0

        # 准备表格行数据
        report_data.append({
            'id': monthly_plan.id,
            '月份': monthly_plan.日期.strftime('%Y-%m'),
            '二级分类': category_name,
            '月计划': monthly_plan.面积,
            '日计划实现': total_daily_plan_area,
            '计划实现率': completion_rate,
            '未达成反馈': 未达成反馈
        })

    context = {
        'report_data': report_data,
        'unique_months': unique_months,  # 传递不重复的月份数据到前端
        'selected_month': selected_month  # 将选中的月份传递回前端
    }
    return render(request, 'plan_completion_report.html', context)
def monthly_plan_download(request):
    # 获取查询条件中的月份
    selected_month = request.GET.get('q', '')

    # 根据用户选择的月份进行过滤
    if selected_month:
        year, month = selected_month.split('-')
        monthly_plans = MonthlyPlan.objects.filter(日期__year=year, 日期__month=month)
    else:
        monthly_plans = MonthlyPlan.objects.all()

    # 创建 Excel 工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly Plan Completion"

    # 写入表头
    ws.append(['月份', '二级分类', '月计划面积', '日计划实现', '计划实现率', '未达成反馈'])

    # 写入表格数据
    for plan in monthly_plans:
        # 获取二级分类名称
        category_name = plan.二级分类.category_name

        # 按月份和二级分类查询日计划完成情况
        daily_plans = DailyPlan.objects.filter(
            种植日期__year=plan.日期.year,
            种植日期__month=plan.日期.month,
            批次ID__contains=category_name
        )

        # 统计日计划的总面积
        total_daily_plan_area = daily_plans.aggregate(
            total=Coalesce(Sum('面积'), Value(0, output_field=DecimalField()))
        )['total']

        # 计算计划实现率
        completion_rate = (total_daily_plan_area / plan.面积) * 100 if plan.面积 > 0 else 0

        # 获取反馈信息
        feedback = plan.未达成反馈 or '无'

        # 写入每一行
        ws.append([plan.日期.strftime('%Y-%m'), category_name, plan.面积, total_daily_plan_area, f"{completion_rate:.2f}%", feedback])

    # 创建 HttpResponse 对象并设置响应的内容类型
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="monthly_plan_completion.xlsx"'

    # 将 Excel 写入到响应中
    wb.save(response)

    return response
def plan_feedback(request, plan_id):
    plan = get_object_or_404(MonthlyPlan, id=plan_id)
    if request.method == 'POST':
        # 处理反馈数据
        feedback = request.POST.get('feedback')
        # 保存反馈逻辑
        plan.未达成反馈 = feedback
        plan.save()
        return redirect('monthly_plan_rate')

    return render(request, 'plan_feedback_form.html', {'plan': plan})