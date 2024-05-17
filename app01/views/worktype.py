from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm, worktypeModelForm


def BaseInfoWorkType_list(request):
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


def BaseInfoWorkType_add(request):
    """ 添加工种 """
    if request.method == "GET":
        form = worktypeModelForm()
        return render(request, 'work_type_add.html', {"form": form})
    form = worktypeModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/BaseInfoWorkType/list/')
    return render(request, 'work_type_add.html', {"form": form})


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
