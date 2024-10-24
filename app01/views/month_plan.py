from datetime import date, datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import MonthlyPlan, JobCategoryInfo, BaseInfoBase
from app01.utils.form import MonthlyPlanForm
from app01.utils.pagination import Pagination


# 显示月度计划
# 显示月度计划列表（带分页和搜索功能）
def monthly_plan_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict["二级分类__category_name__icontains"] = search_data  # 搜索二级分类

    # 根据查询条件过滤数据并排序
    queryset = MonthlyPlan.objects.filter(**data_dict).order_by("-id")

    # 使用自定义分页类进行分页处理
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'monthly_plan_list.html', context)
# 创建新的月度计划


def monthly_plan_create(request):
    if request.method == "POST":
        form_data = request.POST.copy()

        # 处理日期字段，将 'YYYY-MM' 格式转换为 'YYYY-MM-01'
        if '日期' in form_data and form_data['日期']:
            try:
                form_data['日期'] = datetime.strptime(form_data['日期'], '%Y-%m').strftime('%Y-%m-%d')
            except ValueError:
                form_data['日期'] = None

        # 创建表单对象，但暂时不保存
        form = MonthlyPlanForm(form_data)

        if form.is_valid():
            # 获取选定的基地ID，并确保它是BaseInfoBase的实例
            base_id = form_data.get('基地')
            print(base_id)
            base_instance = get_object_or_404(BaseInfoBase, ID=base_id)
            print(base_instance)
            # 创建新的MonthlyPlan对象，但不保存
            monthly_plan = form.save(commit=False)
            monthly_plan.基地 = base_instance  # 分配BaseInfoBase实例
            monthly_plan.save()  # 保存对象
            return redirect('/monthly_plan')
        else:
            print('表单验证失败：', form.errors)
            print('POST 数据：', form_data)  # 输出 POST 数据，调试查看提交内容

    else:
        form = MonthlyPlanForm(initial={'日期': date.today().strftime('%Y-%m')})

    # 获取所有的二级分类和基地信息
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    bases = BaseInfoBase.objects.all()

    context = {
        'form': form,
        'job_categories': job_categories,
        'bases': bases,
    }
    return render(request, 'monthly_plan_form.html', context)
def monthly_plan_edit(request, pk):
    plan = get_object_or_404(MonthlyPlan, pk=pk)

    if request.method == "POST":
        form = MonthlyPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('monthly_plan_list')
    else:
        # 在编辑时使用已有的日期数据
        form = MonthlyPlanForm(instance=plan)

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
    plan = get_object_or_404(MonthlyPlan, pk=pk)
    if request.method == "POST":
        plan.delete()
        return redirect('monthly_plan_list')
    return render(request, 'monthly_plan_confirm_delete.html', {'plan': plan})