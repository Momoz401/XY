from django.shortcuts import render, redirect, get_object_or_404

from app01.models import OutboundRecord
from app01.utils.form import OutboundRecordForm
from app01.utils.pagination import Pagination


def outbound_list(request):
    """出库记录列表"""
    search_data = request.GET.get('q', "")
    queryset = OutboundRecord.objects.exclude(日期__isnull=True)
    if search_data:
        queryset = queryset.filter(公司__contains=search_data).order_by('-日期')

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
