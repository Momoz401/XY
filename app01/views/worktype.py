from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm, work_type_ModelForm


def work_type_list(request):
    """ 工种列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["工种名称"] = search_data

    queryset = models.BaseInfoWorkType.objects.filter(**data_dict).order_by("-工种ID")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'work_type.html', context)


def work_type_add(request):
    """ 添加工种 """
    if request.method == "GET":
        form = work_type_ModelForm()
        return render(request, 'work_type_add.html', {"form": form})
    form = work_type_ModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/BaseInfoWorkType/list/')
    return render(request, 'work_type_add.html', {"form": form})


def work_type_edit(request, nid):
    """ 编辑工种 """
    row_object = models.BaseInfoWorkType.objects.filter(工种ID=nid).first()

    if request.method == "GET":
        form = work_type_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = work_type_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/BaseInfoWorkType/list/')

    return render(request, 'work_type.html', {"form": form})


def work_type_delete(request, nid):
    models.BaseInfoWorkType.objects.filter(工种ID=nid).delete()
    return redirect('/BaseInfoWorkType/list/')
