from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Vehicle
from app01.utils.form import VehicleForm
from app01.utils.pagination import Pagination


def vehicle_list(request):
    """车辆管理信息列表

    该视图函数负责显示所有车辆信息，支持根据车牌号进行搜索，并返回分页后的车辆数据。
    """
    data_dict = {}
    # 获取搜索关键词，默认为空
    search_data = request.GET.get('q', "")
    if search_data:
        # 根据车牌号模糊查询车辆信息
        data_dict["车牌__icontains"] = search_data

    # 查询车辆数据，并按照ID倒序排列
    queryset = Vehicle.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'vehicle_list.html', context)


def vehicle_add(request):
    """添加车辆信息

    该视图函数负责处理新建车辆信息的表单提交。当请求为GET时，显示空表单；当请求为POST时，验证并保存新车辆数据。
    """
    if request.method == "GET":
        # 显示空的车辆表单
        form = VehicleForm()
        return render(request, 'vehicle_form.html', {"form": form, "title": "新建车辆信息"})

    # 处理POST请求，保存车辆数据
    form = VehicleForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/vehicle/list/')
    return render(request, 'vehicle_form.html', {"form": form, "title": "新建车辆信息"})


def vehicle_edit(request, nid):
    """编辑车辆信息

    该视图函数处理编辑已存在车辆信息的表单提交，首先根据车辆ID获取对应的车辆数据，然后根据表单提交的内容更新车辆信息。
    """
    # 获取要编辑的车辆对象，如果找不到则返回404错误
    row_object = get_object_or_404(Vehicle, id=nid)

    if request.method == "GET":
        # 显示编辑车辆的表单，预填充当前车辆信息
        form = VehicleForm(instance=row_object)
        return render(request, 'vehicle_form.html', {"form": form, "title": "编辑车辆信息"})

    # 处理POST请求，更新车辆信息
    form = VehicleForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/vehicle/list/')
    return render(request, 'vehicle_form.html', {"form": form, "title": "编辑车辆信息"})


def vehicle_delete(request, nid):
    """删除车辆信息

    该视图函数用于删除指定ID的车辆信息。
    """
    Vehicle.objects.filter(id=nid).delete()
    return redirect('/vehicle/list/')