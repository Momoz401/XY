from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import MonthlyPlan, JobCategoryInfo
from app01.utils.form import MonthlyPlanForm
from app01.utils.pagination import Pagination
from datetime import date, datetime

def monthly_plan_list(request):
    """
    该视图用于展示所有月度计划信息，支持根据月份筛选、分页显示。
    """
    data_dict = {}
    selected_month = request.GET.get('month', "")  # 获取用户选择的月份

    # 获取数据库中所有唯一的月份（以月份为单位截断日期）
    months = MonthlyPlan.objects.annotate(month=TruncMonth('日期')).values_list('month', flat=True).distinct()

    # 如果用户选择了月份，进行过滤
    if selected_month:
        try:
            search_year, search_month = selected_month.split('-')
            data_dict["日期__year"] = int(search_year)
            data_dict["日期__month"] = int(search_month)
        except ValueError:
            pass

    # 根据筛选条件和排序规则获取月度计划数据
    queryset = MonthlyPlan.objects.filter(**data_dict).order_by("-id")

    # 使用自定义分页类进行分页处理
    page_object = Pagination(request, queryset)

    context = {
        "selected_month": selected_month,
        "months": months,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'monthly_plan_list.html', context)


def monthly_plan_create(request):
    """
    该视图处理新建月度计划的功能。包括显示表单以及表单提交后的数据处理。
    """
    if request.method == "POST":
        form_data = request.POST.copy()

        if '日期' in form_data and form_data['日期']:
            try:
                form_data['日期'] = datetime.strptime(form_data['日期'], '%Y-%m').strftime('%Y-%m-%d')
            except ValueError:
                form_data['日期'] = None

        form = MonthlyPlanForm(form_data)

        if form.is_valid():
            form.save()
            return redirect('/monthly_plan')
        else:
            print('表单验证失败：', form.errors)

    else:
        form = MonthlyPlanForm(initial={'日期': date.today().strftime('%Y-%m')})

    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    context = {
        'form': form,
        'job_categories': job_categories,
    }
    return render(request, 'monthly_plan_form.html', context)


def monthly_plan_edit(request, pk):
    """
    该视图用于编辑现有的月度计划。通过主键查找月度计划，并提供编辑功能。
    """
    plan = get_object_or_404(MonthlyPlan, pk=pk)

    if request.method == "POST":
        form = MonthlyPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('monthly_plan_list')
    else:
        form = MonthlyPlanForm(instance=plan)

    job_categories = JobCategoryInfo.objects.filter(category_level=2)

    context = {
        'form': form,
        'job_categories': job_categories,
    }
    return render(request, 'monthly_plan_edit.html', context)


def monthly_plan_delete(request, pk):
    """
    该视图处理月度计划的删除操作。在确认删除时，删除指定ID的月度计划。
    """
    plan = get_object_or_404(MonthlyPlan, pk=pk)

    if request.method == "POST":
        plan.delete()
        return redirect('monthly_plan_list')

    return render(request, 'monthly_plan_confirm_delete.html', {'plan': plan})