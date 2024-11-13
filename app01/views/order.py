import json
from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.models import ProductionWage
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    """
    对照模型表单，支持对照管理的表单输入
    """
    class Meta:
        model = models.Order
        exclude = ["oid", 'admin']  # 排除自动生成的字段


def order_list(request):
    """
    对照列表展示，支持搜索和分页功能
    """
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["title__icontains"] = search_data  # 模糊匹配对照标题
    queryset = models.Order.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)

    form = OrderModelForm()  # 创建空表单实例，用于添加新对照

    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分页后的对照数据
        "page_string": page_object.html()  # 页码显示
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """
    添加新对照，支持Ajax请求，生成对照号并关联管理员
    """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 自动生成对照号，格式为当前日期
        form.instance.oid = datetime.now().strftime("%Y%m%d")

        # 固定关联管理员ID，从session中获取
        form.instance.admin_id = request.session["info"]["id"]

        form.save()  # 保存对照
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """
    删除对照，根据对照ID执行删除操作
    """
    uid = request.GET.get('uid')
    if not models.Order.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """
    获取对照详情信息，返回对照的具体数据
    """
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    return JsonResponse({
        "status": True,
        "data": row_dict
    })


@csrf_exempt
def order_edit(request):
    """
    编辑对照信息，通过Ajax请求更新数据
    """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()  # 保存更新后的对照数据
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})