from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType, JobCategoryInfo, JobTypeDetailInfo
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm

def Hour_list(request):
    """
    显示工时列表并支持一级分类搜索过滤。
    如果存在查询参数，将根据一级分类的名称搜索对应的ID并筛选数据。
    """
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        # 查询一级分类的中文名称对应的ID
        matching_category_ids = models.JobCategoryInfo.objects.filter(category_name__contains=search_data).values_list('id', flat=True)
        # 将匹配的ID加入到过滤条件中
        data_dict["一级分类__in"] = matching_category_ids

    queryset = models.BaseInfoWorkHour.objects.filter(**data_dict).order_by("-工种ID")
    page_object = Pagination(request, queryset, page_size=15)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'workhour.html', context)

def work_hour_edit(request, nid):
    """
    编辑工时信息。
    通过工种ID获取要编辑的记录并加载表单进行编辑。
    """
    row_object = models.BaseInfoWorkHour.objects.filter(工种ID=nid).first()

    if request.method == "GET":
        form = workHour_Edit_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = workHour_Edit_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/WorkHour/list/')

    return render(request, 'workhour.html', {"form": form})

def work_hour_delete(request, nid):
    """
    删除工时记录。
    根据指定的工种ID删除相应的记录。
    """
    models.BaseInfoWorkHour.objects.filter(工种ID=nid).delete()
    return redirect('/WorkHour/list/')

def WorkHour_add(request):
    """
    添加工时信息。
    如果是GET请求，加载空表单。如果是POST请求，验证并保存数据。
    """
    if request.method == "GET":
        form = workHourModelForm()
        return render(request, 'workhour_add.html', {"form": form})

    form = workHourModelForm(data=request.POST)

    # 打印调试信息
    print("POST 数据: ", request.POST)

    # 验证表单是否有效
    if form.is_valid():
        # 打印清理后的数据
        print("清理后的数据: ", form.cleaned_data)

        form.save()
        return redirect('/WorkHour/list/')
    else:
        # 如果表单无效，打印表单错误
        print("表单错误: ", form.errors)

    return render(request, 'workhour_add.html', {"form": form})

def get_second_level_categories(request):
    """
    根据一级分类动态加载二级分类。
    通过AJAX请求接收一级分类ID并返回匹配的二级分类列表。
    """
    if request.method == 'GET':
        level_one_id = request.GET.get('id', None)
        if level_one_id:
            second_level_categories = JobCategoryInfo.objects.filter(
                parent_category_id=level_one_id, category_level=2).values('id', 'category_name')

            if second_level_categories.exists():
                return JsonResponse(list(second_level_categories), safe=False)
            else:
                return JsonResponse({'error': '没有找到对应的二级分类'}, status=404)
        else:
            return JsonResponse({'error': '一级分类 ID 缺失'}, status=400)
    return JsonResponse({'error': '无效请求'}, status=400)

def get_second_level_jobs(request):
    """
    根据一级工种动态加载二级工种。
    通过AJAX请求接收一级工种ID并返回匹配的二级工种列表。
    """
    if request.method == 'GET':
        level_one_job_id = request.GET.get('id', None)
        if level_one_job_id:
            second_level_jobs = JobTypeDetailInfo.objects.filter(
                parent_job_id=level_one_job_id, job_level=2).values('id', 'job_name')

            if second_level_jobs.exists():
                return JsonResponse(list(second_level_jobs), safe=False)
            else:
                return JsonResponse({'error': '没有找到对应的二级工种'}, status=404)
        else:
            return JsonResponse({'error': '一级工种 ID 缺失'}, status=400)
    return JsonResponse({'error': '无效请求'}, status=400)