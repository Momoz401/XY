from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType,ProductionWage,Agriculture_cost

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm, production_wage_ModelForm, \
    production_wage_Edit_ModelForm, agriculture_cost_ModelForm, agriculture_cost_Edit_ModelForm


def agriculture_cost_list(request):
    """农资成本列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["名称__icontains"] = search_data

    # 查询过滤并按日期降序排列
    queryset = Agriculture_cost.objects.filter(**data_dict).order_by("-日期")

    context = {
        "queryset": queryset,       # 传递所有过滤后的数据
        "search_data": search_data  # 保留搜索数据
    }
    return render(request, 'agriculturecost.html', context)


def agriculture_cost_add(request):
    """ 添加工价 """
    if request.method == "GET":
        form =agriculture_cost_ModelForm()
        return render(request, 'agriculturecost_add.html', {"form": form})
    form = agriculture_cost_ModelForm(data=request.POST)
    # 限制一级工种只能从规定的类别列选择
    if form.is_valid():
        form.save()
        return redirect('/Agricureture/list/')
    return render(request, 'agriculturecost.html', {"form": form})





def agriculture_cost_edit(request, nid):
    """ 编辑工时 """
    row_object = models.Agriculture_cost.objects.filter(ID=nid).first()

    if request.method == "GET":
        form = agriculture_cost_Edit_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = agriculture_cost_Edit_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/Agricureture/list/')

    return render(request, 'agriculturecost.html', {"form": form})


def agriculture_cost_delete(request, nid):
    models.Agriculture_cost.objects.filter(ID=nid).delete()
    return redirect('/Agricureture/list/')
