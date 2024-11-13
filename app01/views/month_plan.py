from datetime import date, datetime

from django.core.paginator import Paginator
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import MonthlyPlan, JobCategoryInfo, BaseInfoBase
from app01.utils.form import MonthlyPlanForm
from app01.utils.pagination import Pagination


# 显示月度计划列表（带分页和搜索功能）
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
            # 将选中的月份进行拆分，获取年和月
            search_year, search_month = selected_month.split('-')
            data_dict["日期__year"] = int(search_year)
            data_dict["日期__month"] = int(search_month)
        except ValueError:
            pass  # 如果格式不对，忽略并不应用筛选条件

    # 根据筛选条件和排序规则获取月度计划数据
    queryset = MonthlyPlan.objects.filter(**data_dict).order_by("-id")

    # 使用自定义分页类进行分页处理
    page_object = Pagination(request, queryset)

    # 渲染模板并传递相关上下文数据
    context = {
        "selected_month": selected_month,  # 选中的月份
        "months": months,  # 所有的月份选项
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码HTML
    }
    return render(request, 'monthly_plan_list.html', context)


# 创建新的月度计划
def monthly_plan_create(request):
    """
    该视图处理新建月度计划的功能。包括显示表单以及表单提交后的数据处理。
    """
    if request.method == "POST":
        form_data = request.POST.copy()

        # 处理日期字段，将 'YYYY-MM' 格式转换为 'YYYY-MM-01'
        if '日期' in form_data and form_data['日期']:
            try:
                form_data['日期'] = datetime.strptime(form_data['日期'], '%Y-%m').strftime('%Y-%m-%d')
            except ValueError:
                form_data['日期'] = None  # 如果日期格式不对，设置为 None

        # 创建表单对象，但暂时不保存
        form = MonthlyPlanForm(form_data)

        if form.is_valid():
            # 获取选定的基地ID，并确保它是BaseInfoBase的实例
            base_id = form_data.get('基地')
            base_instance = get_object_or_404(BaseInfoBase, ID=base_id)

            # 创建新的MonthlyPlan对象，但不保存
            monthly_plan = form.save(commit=False)
            monthly_plan.基地 = base_instance  # 分配BaseInfoBase实例
            monthly_plan.save()  # 保存月度计划对象

            # 重定向到月度计划列表页面
            return redirect('/monthly_plan')
        else:
            print('表单验证失败：', form.errors)
            print('POST 数据：', form_data)  # 输出 POST 数据，调试查看提交内容

    else:
        form = MonthlyPlanForm(initial={'日期': date.today().strftime('%Y-%m')})  # 初始日期为当前月份

    # 获取所有的二级分类和基地信息
    job_categories = JobCategoryInfo.objects.filter(category_level=2)  # 获取所有二级分类
    bases = BaseInfoBase.objects.all()  # 获取所有基地信息

    context = {
        'form': form,
        'job_categories': job_categories,
        'bases': bases,
    }
    return render(request, 'monthly_plan_form.html', context)


# 编辑月度计划
def monthly_plan_edit(request, pk):
    """
    该视图用于编辑现有的月度计划。通过主键查找月度计划，并提供编辑功能。
    """
    plan = get_object_or_404(MonthlyPlan, pk=pk)  # 根据主键获取月度计划

    if request.method == "POST":
        form = MonthlyPlanForm(request.POST, instance=plan)  # 使用已有的计划实例来初始化表单
        if form.is_valid():
            form.save()  # 保存表单数据
            return redirect('monthly_plan_list')  # 重定向到月度计划列表页面
    else:
        form = MonthlyPlanForm(instance=plan)  # GET请求时，使用现有的月度计划数据初始化表单

    # 获取所有的二级分类和基地信息
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    bases = BaseInfoBase.objects.all()

    context = {
        'form': form,
        'job_categories': job_categories,
        'bases': bases,
    }
    return render(request, 'monthly_plan_edit.html', context)


# 删除月度计划
def monthly_plan_delete(request, pk):
    """
    该视图处理月度计划的删除操作。在确认删除时，删除指定ID的月度计划。
    """
    plan = get_object_or_404(MonthlyPlan, pk=pk)  # 获取指定ID的月度计划

    if request.method == "POST":
        plan.delete()  # 删除月度计划
        return redirect('monthly_plan_list')  # 删除后重定向到月度计划列表页面

    return render(request, 'monthly_plan_confirm_delete.html', {'plan': plan})  # GET请求时，确认删除