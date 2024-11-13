from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import baseInfoModelForm


def BaseInfo_list(request):
    """
    基地信息列表视图
    获取并显示所有基地信息，并提供搜索和分页功能。
    """
    data_dict = {}
    search_data = request.GET.get('q', "")  # 获取搜索查询
    if search_data:
        data_dict["基地__icontains"] = search_data  # 搜索基地名称包含输入内容

    queryset = models.BaseInfoBase.objects.filter(**data_dict).order_by("-基地ID")  # 查询和排序

    page_object = Pagination(request, queryset)  # 分页处理

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 分页导航HTML
    }
    return render(request, 'baseinfo.html', context)


def BaseInfo_add(request):
    """
    添加基地信息视图
    处理GET和POST请求以添加新的基地信息。
    """
    if request.method == "GET":
        form = baseInfoModelForm()  # 初始化空表单
        return render(request, 'baseinfo_add.html', {"form": form})

    form = baseInfoModelForm(data=request.POST)  # 处理用户提交的数据
    if form.is_valid():
        form.save()  # 保存数据到数据库
        return redirect('/BaseInfo/list/')
    return render(request, 'baseinfo_add.html', {"form": form})  # 返回带有错误的表单


def BaseInfo_edit(request, nid):
    """
    编辑基地信息视图
    处理GET和POST请求以编辑指定的基地信息。
    """
    row_object = models.BaseInfoBase.objects.filter(ID=nid).first()  # 获取要编辑的对象

    if request.method == "GET":
        form = baseInfoModelForm(instance=row_object)  # 初始化表单并填充现有数据
        return render(request, 'pretty_edit.html', {"form": form})

    form = baseInfoModelForm(data=request.POST, instance=row_object)  # 处理用户提交的数据
    if form.is_valid():
        form.save()  # 保存更新后的数据
        return redirect('/BaseInfo/list/')
    return render(request, 'pretty_edit.html', {"form": form})  # 返回带有错误的表单


def BaseInfo_delete(request, nid):
    """
    删除基地信息视图
    删除指定的基地信息。
    """
    models.BaseInfoBase.objects.filter(基地ID=nid).delete()  # 删除指定ID的对象
    return redirect('/BaseInfo/list/')