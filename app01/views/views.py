
from django.http import JsonResponse
from django.template.loader import render_to_string

from app01.models import Plant_batch, BaseInfoWorkHour, BaseInfoBase, ExpenseAllocation, DepreciationAllocation, \
    LossReport, Salesperson, Vehicle, Market, Customer, OutboundRecord, BaseInfoWorkType, SalesRecord
from app01.utils.form import WorkHourFormSet, ExpenseAllocationForm, DepreciationAllocationForm, LossReportForm, \
    SalespersonForm, VehicleForm, MarketForm, CustomerForm, OutboundRecordForm, SalesRecordForm
from django.db.models.functions import Substr

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
    search_data = request.GET.get('q', "")
    if search_data:
        queryset = OutboundRecord.objects.filter(公司__contains=search_data)
    else:
        queryset = OutboundRecord.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
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
    OutboundRecord.objects.filter(id=nid).delete()
    return redirect('/outbound/list/')


def add_sales_record(request, outbound_id):
    outbound_record = get_object_or_404(OutboundRecord, id=outbound_id)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sales_record = form.save(commit=False)
            sales_record.出库记录 = outbound_record
            if sales_record.数量 <= outbound_record.数量 - sum([sr.数量 for sr in outbound_record.sales_records.all()]):
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
            if total_sales_quantity > outbound_record.数量:
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