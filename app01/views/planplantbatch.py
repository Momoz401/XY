from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm

def planplantbatch_list(request):
    """ 月度计划列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["品种"] = search_data

    queryset = models.PlanPlantBatch.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'planplantbatch.html', context)


def WorkHour_add(request):
    """ 添加工种 """
    if request.method == "GET":
        form = workHourModelForm()
        return render(request, 'workhour_add.html', {"form": form})
    form = workHourModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/WorkHour/list/')
    return render(request, 'workhour_add.html', {"form": form})


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
