from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm


def Hour_list(request):
    """ 工时列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["工种__contains"] = search_data

    queryset = models.BaseInfoWorkHour.objects.filter(**data_dict).order_by("-工种ID")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'workhour.html', context)


def WorkHour_add(request):
    """ 添加工种 """
    if request.method == "GET":
        form = workHourModelForm()
        return render(request, 'workhour_add.html', {"form": form})
    form = workHourModelForm(data=request.POST)
    # 限制一级工种只能从规定的类别列选择
    if form.is_valid():
        form.save()
        return redirect('/WorkHour/list/')
    return render(request, 'workhour_add.html', {"form": form})


def get_second_level_categories(request):
    if request.method == 'GET' :
        # 解码参数
        level_one_id = request.GET.get('id', None)
        # 根据一级分类 ID 获取相应的二级分类数据
        if level_one_id is not None:
            second_level_categories = BaseInfoWorkType.objects.filter(父工种=level_one_id).values_list('工种ID', '工种名称')
            print(JsonResponse(dict(second_level_categories)))
            return JsonResponse(dict(second_level_categories))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)


def work_hour_edit(request, nid):
    """ 编辑工时 """
    row_object = models.BaseInfoWorkHour.objects.filter(工种ID=nid).first()

    if request.method == "GET":
        form = workHour_Edit_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = workHour_Edit_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/WorkHour/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def work_hour_delete(request, nid):
    models.BaseInfoWorkHour.objects.filter(工种ID=nid).delete()
    return redirect('/WorkHour/list/')
