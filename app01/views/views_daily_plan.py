from datetime import timedelta, datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from app01.models import DailyPlan, BaseInfoBase, JobCategoryInfo
from app01.utils.form import DailyPlanForm
from app01.utils.pagination import Pagination

# List View
def daily_plan_list(request):
    # 获取用户输入的日期，默认为当前月份
    search_date = request.GET.get('date', datetime.now().strftime('%Y-%m'))

    # 如果用户输入了日期，按种植日期进行过滤
    if search_date:
        try:
            # 将字符串转换为日期格式（默认当前月）
            search_date = datetime.strptime(search_date, '%Y-%m').date()
            plans = DailyPlan.objects.filter(种植日期__year=search_date.year, 种植日期__month=search_date.month).order_by('-种植日期')
        except ValueError:
            plans = DailyPlan.objects.none()
    else:
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

            # 获取播种方式、上批批次和下批种植日期
            播种方式 = form.cleaned_data['播种方式']
            上批批次 = form.cleaned_data['上批批次']
            下批种植日期 = form.cleaned_data['下批种植日期']

            # 将种植日期转换为 yymmdd 格式
            formatted_date = plant_date.strftime('%y%m%d')

            # 更新批次ID，确保批次ID中包含格式化的日期
            batch_id_parts = batch_id.split('-')
            if len(batch_id_parts) >= 2:
                # 替换日期部分
                batch_id_parts[1] = formatted_date
                batch_id = '-'.join(batch_id_parts)
            else:
                print("批次ID格式不正确")
                return render(request, 'daily_plan_form.html', {'form': form})

            # 保存日计划，确保批次ID不被覆盖
            daily_plan = form.save(commit=False)
            daily_plan.批次ID = batch_id  # 使用更新后的批次ID
            daily_plan.种植日期 = plant_date
            daily_plan.上批批次 = 上批批次
            daily_plan.下批种植日期 = 下批种植日期
            daily_plan.播种方式 = 播种方式

            daily_plan.save()

            return redirect('daily_plan_list')
        else:
            # 表单校验失败，返回错误信息
            print("表单验证失败：", form.errors)
            return render(request, 'daily_plan_form.html', {'form': form})
    else:
        # GET 请求时渲染空表单，带入已有的基地和二级分类数据
        form = DailyPlanForm()
        today = date.today()  # 获取当前日期

        # 获取所有的基地和二级分类信息（用于前端选择）
        bases = BaseInfoBase.objects.all()  # 获取完整的基地对象
        job_categories = JobCategoryInfo.objects.filter(category_level=2)  # 获取完整的二级分类对象

        context = {
            'today': today,
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