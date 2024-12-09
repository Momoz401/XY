import json
import random
from datetime import datetime

from django.db.models import Count
from django.db.models.functions.datetime import TruncMonth
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.models import ProductionWage, Salary_by_plople, Salary_by_daily, Workhour_by_daily
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = [""]
        exclude = ["oid", 'admin']


def report_list(request):
    months = ProductionWage.objects.annotate(month=TruncMonth('日期')).values('month').annotate(
        count=Count('id')).order_by('month')
    month_options = [{"value": month['month'].strftime('%Y%m'), "label": month['month'].strftime('%Y年%m月')} for month
                     in months]
    context = {
        'months': month_options  # 月份选项
    }

    return render(request, 'report_list.html', context)


def report_salary_temp_by_daily(request):
    months = ProductionWage.objects.annotate(month=TruncMonth('日期')).values('month').annotate(count=Count('id')).order_by('month')
    month_options = [{"value": month['month'].strftime('%Y%m'), "label": month['month'].strftime('%Y年%m月')} for month
                     in months]
    context = {
        'months': month_options  # 月份选项
    }

    return render(request, 'report_salary_temp_by_daily.html', context)







def report_salary_by_plople(request):
    # 按月份进行分组和计数
    months = Salary_by_plople.objects.values('日期').annotate(count=Count('id')).order_by('日期')

    # 生成月份选项
    month_options = [
        {"value": month['日期'], "label": f"{str(month['日期'])[:4]}年{str(month['日期'])[4:]}月"}
        for month in months
    ]
    print(month_options)
    # 将月份选项传递给模板
    context = {
        'months': month_options
    }

    return render(request, 'report_salary_by_plople.html', context)

def report_salary_by_daily(request):
    # 按月份进行分组和计数
    months = Salary_by_daily.objects.values('月份').annotate(count=Count('id')).order_by('月份')

    # 生成月份选项
    month_options = [
        { "value": month['月份'],
            "label": f"{str(month['月份'])[:4]}年{str(month['月份'])[4:]}月"}
        for month in months
    ]
    print(month_options)
    # 将月份选项传递给模板
    context = {
        'months': month_options
    }

    return render(request, 'report_salary_by_daily.html', context)

def report_workhour_by_daily(request):
    # 按月份进行分组和计数
    months = Workhour_by_daily.objects.values('月份').annotate(count=Count('id')).order_by('月份')

    # 生成月份选项
    month_options = [
        {"value": month['月份'], "label": f"{str(month['月份'])[:4]}年{str(month['月份'])[4:]}月"}
        for month in months
    ]
    # print(month_options)
    # 将月份选项传递给模板
    context = {
        'months': month_options
    }

    return render(request, 'report_salary_by_hour.html', context)


# 工资明细表
def data_table_view(request):
    query = request.GET.get('q', '')
    month_str = request.GET.get('month', '')

    queryset = ProductionWage.objects.all()

    if month_str:
        try:
            year = int(month_str[:4])
            month = int(month_str[4:])
            queryset = queryset.filter(日期__year=year, 日期__month=month)  # 假设日期字段为 `日期`
        except ValueError:
            pass  # 处理错误的月份格
    data = [{
        "id": obj.id,
        "base": obj.基地,
        "manager": obj.负责人,
        "date": obj.日期,
        "worker": obj.工人,
        "category1": obj.一级分类,
        "category2": obj.一级工种,
        "job": obj.二级工种,
        "wage": obj.工价,
        "quantity": obj.数量,
        "total_wage": obj.合计工资,
        "hours": obj.工时,
        "batch": obj.批次,
        "plot": obj.地块
    } for obj in queryset]

    return JsonResponse({"data": data})





# 散工明细表
def report_salary_temp_by_daily_data_table_view(request):
    query = request.GET.get('q', '')
    month_str = request.GET.get('month', '')

    queryset = ProductionWage.objects.filter(一级分类='散工')

    if month_str:
        try:
            year = int(month_str[:4])
            month = int(month_str[4:])
            queryset = queryset.filter(日期__year=year, 日期__month=month)  # 假设日期字段为 `日期`
        except ValueError:
            pass  # 处理错误的月份格
    data = [{
        "id": obj.id,
        "base": obj.基地,
        "manager": obj.负责人,
        "date": obj.日期,
        "worker": obj.工人,
        "category1": obj.一级分类,
        "category2": obj.一级工种,
        "job": obj.二级工种,
        "wage": obj.工价,
        "quantity": obj.数量,
        "total_wage": obj.合计工资,
        "hours": obj.工时,
        "batch": obj.批次,
        "plot": obj.地块
    } for obj in queryset]

    return JsonResponse({"data": data})



# 工资花名册
def report_salary_by_plople_data_table_view(request):
    month_str = request.GET.get('month', '')
    queryset = Salary_by_plople.objects.all()  # 全部数据
    if month_str:
        try:
            queryset = queryset.filter(日期=month_str)  # 假设日期字段为 `日期`
        except ValueError:
            pass  # 处理错误的月份格
    data = [{
        "company": obj.公司,
        "owner": obj.归属业主,
        "name": obj.姓名,
        "ri_qi": obj.日期,
        "clean_shed": obj.清棚,
        "seed_sowing": obj.点籽,
        "transplant": obj.移栽,
        "weeding": obj.锄草,
        "inter_vegetable": obj.间菜,
        "pull_weeds": obj.拔草,
        "pesticide": obj.打药,
        "fertilize": obj.施肥,
        "blow_lettuce": obj.吹生菜,
        "tie_bamboo": obj.插竹竿绑线,
        "harvest": obj.收菜,
        "clean_waste": obj.清废菜,
        "tie_line": obj.绑线,
        "scattered_work": obj.散工,
        "prune": obj.修枝,
        "tie_branch": obj.绑枝,
        "insert_bamboo": obj.插竹竿,
        "other": obj.其它,
        "ditch_grass": obj.铲沟草,
        "weed_removal": obj.锄拔草,
        "total_hours": obj.合计工时,
        "total_wage": obj.合计工资,
        "average_wage": obj.平均工资
    } for obj in queryset]

    return JsonResponse({"data": data})

def report_salary_by_daily_data_table_view(request):
    month_str = request.GET.get('month', '')
    queryset = Salary_by_daily.objects.all()  # 全部数据
    if month_str:
        try:
            queryset = queryset.filter(月份=month_str)  # 假设月份字段为 `month`
        except ValueError:
            pass  # 处理错误的月份格式

    data = [{
        "worker": obj.工人,
        "base": obj.基地,
        "supervisor": obj.负责人,
        "month": obj.月份,
        "day_1": obj.day_1,
        "day_2": obj.day_2,
        "day_3": obj.day_3,
        "day_4": obj.day_4,
        "day_5": obj.day_5,
        "day_6": obj.day_6,
        "day_7": obj.day_7,
        "day_8": obj.day_8,
        "day_9": obj.day_9,
        "day_10": obj.day_10,
        "day_11": obj.day_11,
        "day_12": obj.day_12,
        "day_13": obj.day_13,
        "day_14": obj.day_14,
        "day_15": obj.day_15,
        "day_16": obj.day_16,
        "day_17": obj.day_17,
        "day_18": obj.day_18,
        "day_19": obj.day_19,
        "day_20": obj.day_20,
        "day_21": obj.day_21,
        "day_22": obj.day_22,
        "day_23": obj.day_23,
        "day_24": obj.day_24,
        "day_25": obj.day_25,
        "day_26": obj.day_26,
        "day_27": obj.day_27,
        "day_28": obj.day_28,
        "day_29": obj.day_29,
        "day_30": obj.day_30,
        "day_31": obj.day_31,
        "total": obj.合计
    } for obj in queryset]

    return JsonResponse({"data": data})

def report_workhour_by_daily_data_table_view(request):
    month_str = request.GET.get('month', '')
    queryset = Workhour_by_daily.objects.all()  # 全部数据
    if month_str:
        try:
            queryset = queryset.filter(月份=month_str)  # 假设月份字段为 `month`
        except ValueError:
            pass  # 处理错误的月份格式

    data = [{
        "worker": obj.工人,
        "base": obj.基地,
        "supervisor": obj.负责人,
        "month": obj.月份,
        "day_1": obj.day_1,
        "day_2": obj.day_2,
        "day_3": obj.day_3,
        "day_4": obj.day_4,
        "day_5": obj.day_5,
        "day_6": obj.day_6,
        "day_7": obj.day_7,
        "day_8": obj.day_8,
        "day_9": obj.day_9,
        "day_10": obj.day_10,
        "day_11": obj.day_11,
        "day_12": obj.day_12,
        "day_13": obj.day_13,
        "day_14": obj.day_14,
        "day_15": obj.day_15,
        "day_16": obj.day_16,
        "day_17": obj.day_17,
        "day_18": obj.day_18,
        "day_19": obj.day_19,
        "day_20": obj.day_20,
        "day_21": obj.day_21,
        "day_22": obj.day_22,
        "day_23": obj.day_23,
        "day_24": obj.day_24,
        "day_25": obj.day_25,
        "day_26": obj.day_26,
        "day_27": obj.day_27,
        "day_28": obj.day_28,
        "day_29": obj.day_29,
        "day_30": obj.day_30,
        "day_31": obj.day_31,
        "total": obj.合计工时,
        "total_1": obj.累积工时
    } for obj in queryset]

    return JsonResponse({"data": data})



@csrf_exempt
def order_add(request):
    """ 新建订单（Ajax请求）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：额外增加一些不是用户输入的值（自己计算出来）
        form.instance.oid = datetime.now().strftime("%Y%m%d")

        # 固定设置管理员ID，去哪里获取？
        form.instance.admin_id = request.session["info"]["id"]

        # 保存到数据库中
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    # 方式1
    """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)
    """

    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
