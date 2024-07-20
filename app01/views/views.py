
from django.http import JsonResponse
from app01.models import Plant_batch, BaseInfoWorkHour, BaseInfoBase, ExpenseAllocation, DepreciationAllocation, \
    LossReport, Salesperson, Vehicle, Market, Customer, OutboundRecord
from app01.utils.form import WorkHourFormSet, ExpenseAllocationForm, DepreciationAllocationForm, LossReportForm, \
    SalespersonForm, VehicleForm, MarketForm, CustomerForm, OutboundRecordForm
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
    """出库记录列表"""
    search_data = request.GET.get('q', "")
    queryset = OutboundRecord.objects.all()
    if search_data:
        queryset = queryset.filter(公司__icontains=search_data)

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
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