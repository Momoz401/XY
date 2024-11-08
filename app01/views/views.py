import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import JsonResponse
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from app01 import models
from app01.models import Plant_batch, BaseInfoWorkHour, BaseInfoBase, ExpenseAllocation, DepreciationAllocation, \
    LossReport, Salesperson, Vehicle, Market, Customer, OutboundRecord, BaseInfoWorkType, SalesRecord, ProductionWage, \
    V_Profit_Summary, JobCategoryInfo, DailyPriceReport, UserInfo, CostAlertFeedback, BatchCost
from app01.utils.form import WorkHourFormSet, ExpenseAllocationForm, DepreciationAllocationForm, LossReportForm, \
    SalespersonForm, VehicleForm, MarketForm, CustomerForm, OutboundRecordForm, SalesRecordForm, \
    ExpenseAllocationModelForm, OutboundUploadForm, JobCategoryInfoModelForm, JobTypeDetailInfoModelForm, \
    DailyPriceReportForm
from django.db.models.functions import Substr, TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Q, F

from django.http import JsonResponse
from django.db.models.functions import Substr

from app01.utils.pagination import Pagination

def autocomplete(request):
    print(request.GET)
    if 'term' in request.GET:
        term = request.GET.get('term')
        baseId = request.GET.get('baseId')

        # 过滤批次ID包含term且批次ID的前三位等于baseId
        qs = Plant_batch.objects.annotate(
            prefix=Substr('批次ID', 1, 3)
        ).filter(
            批次ID__icontains=term,
            prefix=str(baseId)
        )

        # 构建返回的数据格式
        titles = [{'label': plant.批次ID, 'value': plant.批次ID} for plant in qs]

        return JsonResponse(titles, safe=False)

    return JsonResponse([], safe=False)


from django.shortcuts import render, redirect, get_object_or_404


def autocomplete_baseinfo(request):
    # 自动补全基地
    if 'term' in request.GET:
        qs = BaseInfoBase.objects.filter(代号__icontains=request.GET.get('term'))
        titles = list()
        for plant in qs:
            titles.append(plant.代号)
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)


from django.shortcuts import render, redirect








def add_multiple_work_hours(request):
    if request.method == 'POST':
        formset = WorkHourFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/production_wage_list/list')
    else:
        formset = WorkHourFormSet(queryset=BaseInfoWorkHour.objects.none())

    return render(request, 'add_multiple_work_hours.html', {'formset': formset})

def create_expense_allocation(request):
    title = "新建费用摊销"
    if request.method == "GET":
        form = ExpenseAllocationForm()
        return render(request, 'expense_allocation_form.html', {"form": form, "title": title})

    form = ExpenseAllocationForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/expense_allocation/list/')  # 替换为实际的成功页面或列表视图
    return render(request, 'expense_allocation_form.html', {"form": form, "title": title})

def expense_allocation_list(request):
    """费用摊销列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["基地经理__基地经理__icontains"] = search_data

    queryset = ExpenseAllocation.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'expense_allocation_list.html', context)

def expense_allocation_add(request):
    """添加费用摊销"""
    if request.method == "GET":
        form = ExpenseAllocationForm()
        return render(request, 'expense_allocation_form.html', {"form": form})

    form = ExpenseAllocationForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/expense_allocation/list/')
    return render(request, 'expense_allocation_form.html', {"form": form})

def expense_allocation_edit(request, nid):
    """编辑费用摊销"""
    row_object = get_object_or_404(ExpenseAllocation, id=nid)

    if request.method == "GET":
        form = ExpenseAllocationForm(instance=row_object)
        return render(request, 'expense_allocation_form.html', {"form": form})

    form = ExpenseAllocationForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/expense_allocation/list/')
    return render(request, 'expense_allocation_form.html', {"form": form})

def expense_allocation_delete(request, nid):
    ExpenseAllocation.objects.filter(id=nid).delete()
    return redirect('/expense_allocation/list/')




def depreciation_allocation_list(request):
    """折旧摊销列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["基地经理__基地经理__icontains"] = search_data

    queryset = DepreciationAllocation.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'depreciation_allocation_list.html', context)

def depreciation_allocation_add(request):
    """添加折旧摊销"""
    if request.method == "GET":
        form = DepreciationAllocationForm()
        return render(request, 'depreciation_allocation_form.html', {"form": form})

    form = DepreciationAllocationForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/depreciation_allocation/list/')
    return render(request, 'depreciation_allocation_form.html', {"form": form})

def depreciation_allocation_edit(request, nid):
    """编辑折旧摊销"""
    row_object = get_object_or_404(DepreciationAllocation, id=nid)

    if request.method == "GET":
        form = DepreciationAllocationForm(instance=row_object)
        return render(request, 'depreciation_allocation_form.html', {"form": form})

    form = DepreciationAllocationForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/depreciation_allocation/list/')
    return render(request, 'depreciation_allocation_form.html', {"form": form})

def depreciation_allocation_delete(request, nid):
    DepreciationAllocation.objects.filter(id=nid).delete()
    return redirect('/depreciation_allocation/list/')


def loss_report_list(request):
    """报损列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["报损人__icontains"] = search_data

    queryset = LossReport.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'loss_report_list.html', context)

def loss_report_add(request):
    """添加报损"""
    if request.method == "GET":
        form = LossReportForm()
        return render(request, 'loss_report_form.html', {"form": form})

    form = LossReportForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/loss_report/list/')
    return render(request, 'loss_report_form.html', {"form": form})

def loss_report_edit(request, nid):
    """编辑报损"""
    row_object = get_object_or_404(LossReport, id=nid)

    if request.method == "GET":
        form = LossReportForm(instance=row_object)
        return render(request, 'loss_report_form.html', {"form": form})

    form = LossReportForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/loss_report/list/')
    return render(request, 'loss_report_form.html', {"form": form})

def loss_report_delete(request, nid):
    LossReport.objects.filter(id=nid).delete()
    return redirect('/loss_report/list/')


def get_plant_batch_dk(request):
    batch_id = request.GET.get('one')
    plant_batch = Plant_batch.objects.filter(批次ID=batch_id).first()
    if plant_batch:
        data = {
            '地块': plant_batch.地块
        }
    else:
        data = {}
    return JsonResponse(data)

def loss_report_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs = Plant_batch.objects.filter(批次ID__icontains=term)
        titles = [{'label': plant.批次ID, 'value': plant.批次ID} for plant in qs]
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)


def salesperson_list(request):
    """销售人员信息列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["姓名__icontains"] = search_data

    queryset = Salesperson.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'salesperson_list.html', context)

def salesperson_add(request):
    """添加销售人员信息"""
    if request.method == "GET":
        form = SalespersonForm()
        return render(request, 'salesperson_form.html', {"form": form, "title": "新建销售人员信息"})

    form = SalespersonForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/salesperson/list/')
    return render(request, 'salesperson_form.html', {"form": form, "title": "新建销售人员信息"})

def salesperson_edit(request, nid):
    """编辑销售人员信息"""
    row_object = get_object_or_404(Salesperson, id=nid)

    if request.method == "GET":
        form = SalespersonForm(instance=row_object)
        return render(request, 'salesperson_form.html', {"form": form, "title": "编辑销售人员信息"})

    form = SalespersonForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/salesperson/list/')
    return render(request, 'salesperson_form.html', {"form": form, "title": "编辑销售人员信息"})

def salesperson_delete(request, nid):
    Salesperson.objects.filter(id=nid).delete()
    return redirect('/salesperson/list/')


def vehicle_list(request):
    """车辆管理信息列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["车牌__icontains"] = search_data

    queryset = Vehicle.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'vehicle_list.html', context)

def vehicle_add(request):
    """添加车辆信息"""
    if request.method == "GET":
        form = VehicleForm()
        return render(request, 'vehicle_form.html', {"form": form, "title": "新建车辆信息"})

    form = VehicleForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/vehicle/list/')
    return render(request, 'vehicle_form.html', {"form": form, "title": "新建车辆信息"})

def vehicle_edit(request, nid):
    """编辑车辆信息"""
    row_object = get_object_or_404(Vehicle, id=nid)

    if request.method == "GET":
        form = VehicleForm(instance=row_object)
        return render(request, 'vehicle_form.html', {"form": form, "title": "编辑车辆信息"})

    form = VehicleForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/vehicle/list/')
    return render(request, 'vehicle_form.html', {"form": form, "title": "编辑车辆信息"})

def vehicle_delete(request, nid):
    Vehicle.objects.filter(id=nid).delete()
    return redirect('/vehicle/list/')

def market_list(request):
    """市场信息列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["市场名称__icontains"] = search_data

    queryset = Market.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'market_list.html', context)

def market_add(request):
    """添加市场信息"""
    if request.method == "GET":
        form = MarketForm()
        return render(request, 'market_form.html', {"form": form, "title": "新建市场信息"})

    form = MarketForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/market/list/')
    return render(request, 'market_form.html', {"form": form, "title": "新建市场信息"})

def market_edit(request, nid):
    """编辑市场信息"""
    row_object = get_object_or_404(Market, id=nid)

    if request.method == "GET":
        form = MarketForm(instance=row_object)
        return render(request, 'market_form.html', {"form": form, "title": "编辑市场信息"})

    form = MarketForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/market/list/')
    return render(request, 'market_form.html', {"form": form, "title": "编辑市场信息"})

def market_delete(request, nid):
    Market.objects.filter(id=nid).delete()
    return redirect('/market/list/')

def customer_list(request):
    """客户信息列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["客户名称__icontains"] = search_data

    queryset = Customer.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'customer_list.html', context)

def customer_add(request):
    """添加客户信息"""
    if request.method == "GET":
        form = CustomerForm()
        return render(request, 'customer_form.html', {"form": form, "title": "新建客户信息"})

    form = CustomerForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_form.html', {"form": form, "title": "新建客户信息"})

def customer_edit(request, nid):
    """编辑客户信息"""
    row_object = get_object_or_404(Customer, id=nid)

    if request.method == "GET":
        form = CustomerForm(instance=row_object)
        return render(request, 'customer_form.html', {"form": form, "title": "编辑客户信息"})

    form = CustomerForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_form.html', {"form": form, "title": "编辑客户信息"})

def customer_delete(request, nid):
    Customer.objects.filter(id=nid).delete()
    return redirect('/customer/list/')

def outbound_list(request):
    """出库记录列表"""
    search_data = request.GET.get('q', "")
    queryset = OutboundRecord.objects.all()
    if search_data:
        queryset = queryset.filter(公司__contains=search_data)

    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 分页HTML
    }
    return render(request, 'outbound_list.html', context)

def outbound_add(request):
    """添加出库记录"""
    if request.method == "GET":
        form = OutboundRecordForm()
        return render(request, 'outbound_form.html', {"form": form, "title": "添加出库记录"})

    form = OutboundRecordForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/outbound/list/')
    return render(request, 'outbound_form.html', {"form": form, "title": "添加出库记录"})

def outbound_edit(request, nid):
    """编辑出库记录"""
    row_object = get_object_or_404(OutboundRecord, id=nid)
    if request.method == "GET":
        form = OutboundRecordForm(instance=row_object)
        return render(request, 'outbound_form.html', {"form": form, "title": "编辑出库记录"})

    form = OutboundRecordForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/outbound/list/')
    return render(request, 'outbound_form.html', {"form": form, "title": "编辑出库记录"})

def outbound_delete(request, nid):
    """删除出库记录"""
    OutboundRecord.objects.filter(id=nid).delete()
    return redirect('/outbound/list/')


def add_sales_record(request, outbound_id):
    outbound_record = get_object_or_404(OutboundRecord, id=outbound_id)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sales_record = form.save(commit=False)
            sales_record.出库记录 = outbound_record
            if sales_record.数量 <= outbound_record.数量_筐 - sum([sr.数量 for sr in outbound_record.sales_records.all()]):
                sales_record.save()
                return redirect('outbound_list')
            else:
                form.add_error('数量', '销售数量不能超过出库数量')
    else:
        form = SalesRecordForm()
    return render(request, 'add_sales_record.html', {'form': form, 'outbound_record': outbound_record})

def fetch_unique_second_level_categories(request):
    first_level_category_name = request.GET.get('name')
    second_level_categories = BaseInfoWorkType.objects.filter(父分类=first_level_category_name, 分类级别=2).distinct('分类名称').values_list('分类名称', flat=True)
    return JsonResponse({'second_level_categories': list(second_level_categories)})


def get_sales_records(request):
    outbound_id = request.GET.get('outbound_id')
    outbound_record = get_object_or_404(OutboundRecord, id=outbound_id)
    sales_records = outbound_record.sales_records.all()
    html = render_to_string('sales_records.html', {'sales_records': sales_records})
    return JsonResponse({'html': html})

def add_sale_form(request):
    outbound_id = request.GET.get('outbound_id')
    outbound_record = get_object_or_404(OutboundRecord, id=outbound_id)
    form = SalesRecordForm()
    html = render_to_string('add_sale_form.html', {'form': form, 'outbound_record': outbound_record}, request=request)
    return JsonResponse({'html': html})

def sales_record_add(request, outbound_id):
    outbound_record = get_object_or_404(OutboundRecord, id=outbound_id)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sales_record = form.save(commit=False)
            sales_record.出库记录 = outbound_record
            sales_record.批次 = outbound_record.批次
            sales_record.销售日期 = outbound_record.日期

            # 检查销售数量是否超过出库数量
            total_sales_quantity = sum(record.数量 for record in outbound_record.sales_records.all()) + sales_record.数量
            if total_sales_quantity > outbound_record.数量_筐:
                form.add_error('数量', '销售数量不能超过出库数量')
            else:
                sales_record.save()
                return redirect('outbound_list')
    else:
        form = SalesRecordForm()

    return render(request, 'sales_record_add.html', {'form': form, 'outbound_record': outbound_record})

def sales_record_edit(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('outbound_list')  # 重定向到出库记录列表或其他页面
    else:
        form = SalesRecordForm(instance=record)
    return render(request, 'sales_record_edit.html', {'form': form})

def sales_record_delete(request, pk):
    record = get_object_or_404(SalesRecord, pk=pk)
    record.delete()
    return redirect('outbound_list')  # 重定向到出库记录列表或其他页面


# 单独管理销售记录的视图函数
def sales_record_management_list(request):
    """销售记录列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["客户__icontains"] = search_data

    queryset = SalesRecord.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset)  # 使用分页功能

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'sales_record_management_list.html', context)


def sales_record_management_add(request):
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_record_management_list')
    else:
        form = SalesRecordForm()
    return render(request, 'sales_record_management_add.html', {'form': form})

def sales_record_management_edit(request, pk):
    sales_record = get_object_or_404(SalesRecord, pk=pk)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST, instance=sales_record)
        if form.is_valid():
            form.save()
            return redirect('sales_record_management_list')
    else:
        form = SalesRecordForm(instance=sales_record)
    return render(request, 'sales_record_management_edit.html', {'form': form})

def sales_record_management_delete(request, pk):
    sales_record = get_object_or_404(SalesRecord, pk=pk)
    sales_record.delete()
    return redirect('sales_record_management_list')


from django.shortcuts import render
from app01.models import Plant_batch

# 这里要设计一个日历的生产情况
def plant_batch_calendar_view(request):
    # 获取所有批次的记录
    plant_batches = Plant_batch.objects.all().values('批次ID', '移栽日期', '点籽日期', '采收初期', '采收末期')

    # 创建一个事件列表
    events = []
    for batch in plant_batches:
        if batch['移栽日期']:
            events.append({
                'title': f"移栽: {batch['批次ID']}",
                'start': batch['移栽日期'].strftime('%Y-%m-%d'),
                'color': 'green',
            })
        if batch['点籽日期']:
            events.append({
                'title': f"点籽: {batch['批次ID']}",
                'start': batch['点籽日期'].strftime('%Y-%m-%d'),
                'color': 'blue',
            })
        if batch['采收初期']:
            events.append({
                'title': f"采收初期: {batch['批次ID']}",
                'start': batch['采收初期'].strftime('%Y-%m-%d'),
                'color': 'orange',
            })
        if batch['采收末期']:
            events.append({
                'title': f"采收末期: {batch['批次ID']}",
                'start': batch['采收末期'].strftime('%Y-%m-%d'),
                'color': 'red',
            })

    context = {
        'events': events
    }

    return render(request, 'plant_batch_calendar.html', context)
# 这里设计一个批次成本汇总数据



def plant_batch_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    now = datetime.now()

    if not start_date:
        first_day_of_month = now.replace(day=1)
        start_date = first_day_of_month.strftime('%Y-%m-%d')
    else:
        first_day_of_month = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        end_date = last_day_of_month.strftime('%Y-%m-%d')
    else:
        last_day_of_month = datetime.strptime(end_date, '%Y-%m-%d')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                批次ID,
                种植日期,
                批次一级分类,
                批次二级分类,
                面积,
                总计划内成本
            FROM
                views_批次计划内成本汇总
            WHERE
                种植日期 BETWEEN %s AND %s
            GROUP BY
                批次ID, 种植日期, 批次一级分类, 批次二级分类, 面积
        """, [start_date, end_date])
        rows = cursor.fetchall()

    summary_data = [
        {
            '批次ID': row[0],
            '种植日期': row[1],
            '批次一级分类': row[2],
            '批次二级分类': row[3],
            '地块': row[4],
            '总计划内成本': row[5]
        }
        for row in rows
    ]

    context = {
        'summary_data': summary_data,
        'start_date': start_date,
        'end_date': end_date,
        'default_start_date': first_day_of_month.strftime('%Y-%m-%d'),
        'default_end_date': last_day_of_month.strftime('%Y-%m-%d')
    }

    return render(request, 'plant_batch_summary.html', context)
def get_batch_details(request):
    batch_id = request.GET.get('batch_id')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                批次ID,
                种植日期,
                二级工种名称,
                单价,
                计量系数,
                计划内成本
            FROM
                views_批次计划内成本
            WHERE
                批次ID = %s
        """, [batch_id])
        details_data = cursor.fetchall()

    # 生成 HTML 内容
    html = '<table class="table table-striped">'
    html += '<tr><th>批次ID</th><th>种植日期</th><th>二级工种</th><th>单价</th><th>计量系数</th><th>计划内成本</th></tr>'
    for row in details_data:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>'
    html += '</table>'

    return JsonResponse({'html': html})

from django.shortcuts import render
from django.db import connection


def production_wage_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    now = datetime.now()

    if not start_date:
        start_date = now.strftime("%Y-%m-01")

    if not end_date:
        end_date = now.strftime("%Y-%m-%d")

    # 查询第一层汇总数据，按批次进行汇总
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 批次, SUM(合计工资) AS total_wage
            FROM app01_productionwage
            WHERE 日期 >= %s AND 日期 <= %s
            GROUP BY 批次
        """, [start_date, end_date])
        summary_data = cursor.fetchall()

    return render(request, 'production_wage_summary.html', {
        'summary_data': summary_data,
        'start_date': start_date,
        'end_date': end_date
    })


def production_wage_second_level(request):
    batch = request.GET.get('batch')

    # 查询第二层数据，按工人进行汇总
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 工人, SUM(合计工资) AS total_wage
            FROM app01_productionwage
            WHERE 批次 = %s
            GROUP BY 工人
        """, [batch])
        second_level_data = cursor.fetchall()

    # 生成 HTML 内容
    html = '<table class="table table-striped">'
    html += '<tr><th>工人</th><th>合计工资</th></tr>'
    for row in second_level_data:
        html += f'<tr data-worker="{row[0]}"><td>{row[0]}</td><td>{row[1]:.2f}</td></tr>'
    html += '</table>'

    return JsonResponse({'html': html})


def production_wage_details(request):
    worker = request.GET.get('worker')
    batch = request.GET.get('batch')

    # 查询第三层数据，显示详细信息
    details = ProductionWage.objects.filter(工人=worker, 批次=batch).values()

    # 生成 HTML 内容
    html = '<table class="table table-striped">'
    html += '<tr><th>日期</th><th>二级工种</th><th>一级分类</th><th>二级分类</th><th>工时</th><th>数量</th><th>工价</th><th>累计工时</th><th>合计工资</th></tr>'
    for row in details:
        html += f"<tr>"
        html += f"<td>{row.get('日期', '')}</td>"
        html += f"<td>{row.get('二级工种', '')}</td>"
        html += f"<td>{row.get('一级分类', '')}</td>"
        html += f"<td>{row.get('二级分类', '')}</td>"
        html += f"<td>{row.get('工时', 0) if row.get('工时') is not None else 0:.2f}</td>"
        html += f"<td>{row.get('数量', 0) if row.get('数量') is not None else 0:.2f}</td>"
        html += f"<td>{row.get('工价', 0) if row.get('工价') is not None else 0:.2f}</td>"
        html += f"<td>{row.get('累计工时', 0) if row.get('累计工时') is not None else 0:.2f}</td>"
        html += f"<td>{row.get('合计工资', 0) if row.get('合计工资') is not None else 0:.2f}</td>"
        html += f"</tr>"
    html += '</table>'

    return JsonResponse({'html': html})


# 费用分摊设计

def expense_allocation_add(request):
    """ 添加费用摊销 """
    if request.method == "GET":
        form = ExpenseAllocationModelForm()
        return render(request, 'expense_allocation_form.html', {"form": form})

    form = ExpenseAllocationModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/expense_allocation/list/')
    return render(request, 'expense_allocation_form.html', {"form": form})

def expense_allocation_edit(request, nid):
    """ 编辑费用摊销 """
    row_object = ExpenseAllocation.objects.filter(id=nid).first()

    if request.method == "GET":
        form = ExpenseAllocationModelForm(instance=row_object)
        return render(request, 'expense_allocation_form.html', {"form": form})

    form = ExpenseAllocationModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/expense_allocation/list/')
    return render(request, 'expense_allocation_form.html', {"form": form})

def expense_allocation_delete(request, nid):
    ExpenseAllocation.objects.filter(id=nid).delete()
    return redirect('/expense_allocation/list/')

# 利润
def profit_summary(request):
    # 获取查询参数
    search_data = request.GET.get('q', "")

    # 获取时间区间参数
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # 基于时间区间筛选数据
    queryset = V_Profit_Summary.objects.all()
    if start_date and end_date:
        queryset = queryset.filter(批次__range=[start_date, end_date])

    # 分页处理
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'profit_summary.html', context)



# 分类列表
def job_category_list(request):
    categories = models.JobCategoryInfo.objects.all()
    return render(request, 'job_category_list.html', {"categories": categories})

# 添加分类
def job_category_add(request):
    if request.method == "POST":
        form = JobCategoryInfoModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/job_category/list/')
    else:
        form = JobCategoryInfoModelForm()

    parent_categories = JobCategoryInfo.objects.filter(category_level=1)
    return render(request, 'job_category_add.html', {'form': form, 'parent_categories': parent_categories})

# 编辑分类
def job_category_edit(request, pk):
    category = get_object_or_404(models.JobCategoryInfo, pk=pk)
    # 获取所有一级分类，用于二级分类选择父分类
    parent_categories = models.JobCategoryInfo.objects.filter(category_level=1)  # 获取所有一级分类

    if request.method == "GET":
        form = JobCategoryInfoModelForm(instance=category)
        return render(request, 'job_category_edit.html', {
            "form": form,
            "parent_categories": parent_categories,
        })

    form = JobCategoryInfoModelForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        return redirect('/job_category/list/')

    return render(request, 'job_category_edit.html', {
        "form": form,
        "parent_categories": parent_categories,
    })


# 每日价格上报列表


# 每日价格上报列表
def daily_price_report_list(request):
    """每日价格上报列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["品种__category_name__icontains"] = search_data

    # 根据查询条件过滤数据并排序
    queryset = DailyPriceReport.objects.filter(**data_dict).order_by("-id")

    # 使用自定义分页类
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'daily_price_report_list.html', context)


def daily_price_report_edit(request, pk):
    """编辑每日价格上报"""
    report = get_object_or_404(DailyPriceReport, pk=pk)

    if request.method == 'POST':
        form = DailyPriceReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('daily_price_report_list')  # 假设您的列表页面路径名称为 daily_price_report_list
    else:
        form = DailyPriceReportForm(instance=report)

    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'daily_price_report_edit.html', context)


def daily_price_report_delete(request, pk):
    """删除每日价格上报"""
    report = get_object_or_404(DailyPriceReport, pk=pk)
    report.delete()
    return redirect('daily_price_report_list')

def employee_autocomplete(request):
    if request.method == 'GET':
        query = request.GET.get('term', '').strip()
        if query:
            employees = UserInfo.objects.filter(name__startswith=query).values_list('id', 'name', 'create_time')
            employee_list = [{'id': emp[0], 'name': emp[1], 'birthdate': emp[2].strftime('%Y-%m-%d') if emp[2] else 'N/A'} for emp in employees]
            return JsonResponse(employee_list, safe=False)
        else:
            return JsonResponse([], safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 费用预警的汇总视图
def cost_alert_summary(request):
    """第一层: 显示批次的总计划内成本和实际成本的比较，包含反馈内容"""
    # 获取当前月的起始和结束日期
    from datetime import date, timedelta
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # 获取用户输入或设置默认值
    start_date = request.GET.get('start_date', first_day_of_month)
    end_date = request.GET.get('end_date', last_day_of_month)
    queryset = Plant_batch.objects.all()

    if start_date and end_date:
        queryset = queryset.filter(种植日期__range=[start_date, end_date])

    # 手动关联 BatchCost 数据
    batch_ids = queryset.values_list('批次ID', flat=True)
    cost_data = BatchCost.objects.filter(批次ID__in=batch_ids).values('批次ID').annotate(
        total_planned_cost=Sum('计划内成本')
    )

    cost_dict = {item['批次ID']: item['total_planned_cost'] for item in cost_data}

    summary_data = []
    for item in queryset:
        total_planned_cost = cost_dict.get(item.批次ID, 0)
        total_actual_cost = ProductionWage.objects.filter(批次=item.批次ID).aggregate(total=Sum('合计工资'))[
                                'total'] or 0

        # 查询反馈内容
        feedback = CostAlertFeedback.objects.filter(批次ID=item.批次ID).first()
        feedback_content = feedback.反馈内容 if feedback else ""

        summary_data.append({
            '批次ID': item.批次ID,
            '种植日期': item.种植日期,
            'total_planned_cost': total_planned_cost,
            'total_actual_cost': total_actual_cost,
            'cost_exceeded': total_actual_cost > total_planned_cost,
            'feedback_content': feedback_content  # 添加反馈内容
        })

    return render(request, 'cost_alert_summary.html', {
        'summary_data': summary_data,
        'start_date': start_date,
        'end_date': end_date
    })


def cost_alert_details(request):
    """第二层: 显示每个批次内的具体工种成本详情"""
    batch_id = request.GET.get('batch_id')
    details_data = ProductionWage.objects.filter(批次=batch_id).annotate(
        planned_cost=F('batchcost__计划内成本')
    ).values('工种', 'planned_cost', '合计工资')

    html = '<table class="table table-striped">'
    html += '<tr><th>工种</th><th>计划成本</th><th>实际成本</th><th>超出反馈</th></tr>'
    for row in details_data:
        exceeded = row['合计工资'] > row['planned_cost']
        feedback_button = '<button class="btn btn-warning">反馈</button>' if exceeded else ''
        html += f"<tr><td>{row['工种']}</td><td>{row['planned_cost']:.2f}</td><td>{row['合计工资']:.2f}</td><td>{feedback_button}</td></tr>"
    html += '</table>'

    return JsonResponse({'html': html})


def cost_alert_feedback(request):
    """处理超支反馈的视图方法"""
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        work_type = request.POST.get('work_type')
        feedback_content = request.POST.get('feedback_content', '')

        try:
            # 使用 update_or_create 方法查找或更新记录
            feedback, created = CostAlertFeedback.objects.update_or_create(
                批次ID=batch_id,
                defaults={'工种': work_type, '反馈内容': feedback_content}
            )

            if created:
                message = "反馈已成功提交。"
            else:
                message = "反馈已更新。"

            return JsonResponse({"success": True, "message": message})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"提交反馈时发生错误: {str(e)}"})

    return JsonResponse({"success": False, "message": "仅支持POST请求。"})


def fetch_cost_details(request):
    batch_id = request.GET.get('batch_id')

    with connection.cursor() as cursor:
        # 查询计划内成本数据
        cursor.execute("""
            SELECT
                批次ID,
                种植日期,
                二级工种名称,
                计划内成本
            FROM
                views_批次计划内成本
            WHERE
                批次ID = %s
        """, [batch_id])
        details_data = cursor.fetchall()

        # 查询实际成本数据，按批次和二级工种关联
        cursor.execute("""
            SELECT
                二级工种,
                SUM(合计工资) AS total_actual_cost
            FROM
                main.app01_productionwage
            WHERE
                批次 = %s
            GROUP BY 二级工种
        """, [batch_id])
        actual_cost_data = cursor.fetchall()

    # 将实际成本数据转换为字典，便于快速查找
    actual_cost_dict = {row[0]: row[1] for row in actual_cost_data}

    # 生成 HTML 内容
    html = '<table class="table table-striped">'
    html += '<tr><th>批次ID</th><th>种植日期</th><th>二级工种</th><th>计划内成本</th><th>实际成本</th><th>差额</th></tr>'
    for row in details_data:
        planned_cost = row[3]
        actual_cost = actual_cost_dict.get(row[2], 0)  # 根据二级工种名称匹配实际成本
        difference = actual_cost - planned_cost
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{planned_cost:.2f}</td><td>{actual_cost:.2f}</td><td>{difference:.2f}</td></tr>'
    html += '</table>'

    return JsonResponse({'html': html})