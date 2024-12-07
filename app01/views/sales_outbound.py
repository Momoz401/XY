from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from app01.models import OutboundRecord, SalesRecord
from app01.utils.form import SalesRecordForm


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
            if total_sales_quantity > outbound_record.实销筐数:
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
