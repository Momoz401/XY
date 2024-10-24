from datetime import timedelta, datetime
from django.shortcuts import render, get_object_or_404, redirect
from app01.models import DailyPlan, BaseInfoBase, JobCategoryInfo
from app01.utils.form import DailyPlanForm
from app01.utils.pagination import Pagination


# List View
def daily_plan_list(request):
    # 获取用户输入的日期
    search_date = request.GET.get('date', "")

    # 如果用户输入了日期，按种植日期进行过滤
    if search_date:
        try:
            # 将字符串转换为日期格式
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            plans = DailyPlan.objects.filter(种植日期=search_date).order_by('-种植日期')
        except ValueError:
            # 如果输入的日期格式不正确，返回空的计划列表
            plans = DailyPlan.objects.none()
    else:
        # 如果没有输入日期，显示所有的日计划
        plans = DailyPlan.objects.all().order_by('-种植日期')

    # 分页处理
    page_object = Pagination(request, plans)
    context = {
        'plans': page_object.page_queryset,  # 分页后的数据
        'page_string': page_object.html(),  # 分页控件HTML
        'search_date': search_date  # 保留搜索的日期
    }

    return render(request, 'daily_plan_list.html', context)


def daily_plan_create(request):
    if request.method == "POST":
        form = DailyPlanForm(request.POST)

        if form.is_valid():
            # 获取前端传递的批次ID
            batch_id = request.POST.get('批次ID')

            # 获取种植日期并格式化
            plant_date_str = request.POST.get('种植日期')
            try:
                plant_date = datetime.strptime(plant_date_str, '%Y-%m-%d')  # 假设日期格式为 YYYY-MM-DD
            except ValueError:
                print("日期解析错误")
                return render(request, 'daily_plan_form.html', {'form': form})

            # 获取生长周期和采收期
            growth_cycle = form.cleaned_data['生长周期']
            harvest_cycle = form.cleaned_data['采收期']

            # 计算采收初期和采收末期
            initial_harvest = plant_date + timedelta(days=growth_cycle)
            final_harvest = initial_harvest + timedelta(days=harvest_cycle)

            # 保存日计划，确保批次ID不被覆盖
            daily_plan = form.save(commit=False)
            daily_plan.批次ID = batch_id  # 使用前端传递的批次ID，不再重新生成
            daily_plan.种植日期 = plant_date
            daily_plan.采收初期 = initial_harvest
            daily_plan.采收末期 = final_harvest


            daily_plan.save()

            return redirect('daily_plan_list')
        else:
            # 表单校验失败，返回错误信息
            print("表单验证失败：", form.errors)
            return render(request, 'daily_plan_form.html', {'form': form})
    else:
        # GET 请求时渲染空表单，带入已有的基地和二级分类数据
        form = DailyPlanForm()

        # 获取所有的基地和二级分类信息（用于前端选择）
        bases = BaseInfoBase.objects.all()  # 获取完整的基地对象
        job_categories = JobCategoryInfo.objects.filter(category_level=2)  # 获取完整的二级分类对象

        context = {
            'form': form,
            'bases': bases,
            'job_categories': job_categories,
        }
        return render(request, 'daily_plan_form.html', context)
# Edit View
def daily_plan_edit(request, pk):
    plan = get_object_or_404(DailyPlan, pk=pk)
    if request.method == 'POST':
        form = DailyPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('daily_plan_list')
    else:
        form = DailyPlanForm(instance=plan)

    # 获取所有的基地和二级分类信息（用于前端选择）
    bases = BaseInfoBase.objects.all()
    job_categories = JobCategoryInfo.objects.all()

    context = {
        'form': form,
        'bases': bases,
        'job_categories': job_categories,
    }

    return render(request, 'daily_plan_form.html', context)


# Delete View
def daily_plan_delete(request, batch_id):
    # 使用批次ID删除对应的日计划
    DailyPlan.objects.filter(批次ID=batch_id).delete()
    return redirect('daily_plan_list')