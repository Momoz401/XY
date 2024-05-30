from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType,ProductionWage,Agriculture_cost

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm, production_wage_ModelForm, \
    production_wage_Edit_ModelForm, agriculture_cost_ModelForm, agriculture_cost_Edit_ModelForm, Plant_batch_ModelForm


def Plant_batch_list(request):
    """ 工时列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["名称__contains"] = search_data

    queryset = models.Plant_batch.objects.filter(**data_dict).order_by("-ID")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'Plant_batch.html', context)


def Plant_batch_add(request):
    """ 添加工价 """
    if request.method == "GET":
        form =Plant_batch_ModelForm()
        return render(request, 'Plant_batch_add.html', {"form": form})
    form = Plant_batch_ModelForm(data=request.POST)
    # 限制一级工种只能从规定的类别列选择
    if form.is_valid():
        form.save()
        return redirect('/Plant_batch/list/')
    return render(request, 'Plant_batch.html', {"form": form})





def Plant_batch_edit(request, nid):
    """ 编辑工时 """
    row_object = models.Plant_batch.objects.filter(ID=nid).first()

    if request.method == "GET":
        form = Plant_batch_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = Plant_batch_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/Plant_batch/list/')

    return render(request, 'Plant_batch.html', {"form": form})


def Plant_batch_delete(request, nid):
    models.Plant_batch.objects.filter(ID=nid).delete()
    return redirect('/Plant_batch/list/')
