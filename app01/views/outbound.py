from pyexpat.errors import messages

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from app01.models import OutboundRecord, Market, Plant_batch, Vehicle, JobCategoryInfo
from app01.utils.form import OutboundRecordForm, OutboundRecordEditForm
from app01.utils.pagination import Pagination


def outbound_list(request):
    """出库记录列表"""
    search_data = request.GET.get('q', "")
    queryset = OutboundRecord.objects.exclude(日期__isnull=True).annotate(
        sales_count=Count('sales_records')  # related_name='sales_records'
    ).order_by('-日期')

    if search_data:
        queryset = queryset.filter(
            Q(批次__icontains=search_data) |
            Q(车牌__icontains=search_data) |
            Q(挑菜__icontains=search_data) |
            Q(地块__icontains=search_data) |
            Q(公司__icontains=search_data) |
            Q(日期__icontains=search_data) |
            Q(市场__icontains=search_data)
        ).order_by('-日期')

    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 分页HTML
    }
    return render(request, 'outbound_list.html', context)

def outbound_add(request):
    """添加出库记录（桌面端）"""
    if request.method == "GET":
        form = OutboundRecordForm()
        vehicles = Vehicle.objects.all()
        markets = Market.objects.all()
        return render(request, 'outbound_form.html', {
            "form": form,
            "title": "添加出库记录",
            "vehicles": vehicles,
            "markets": markets,
        })

    form = OutboundRecordForm(data=request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        # 获取批次ID
        batch_id = form.cleaned_data.get('批次')
        if batch_id:
            try:
                # 根据批次ID获取 Plant_batch 对象
                batch_obj = Plant_batch.objects.get(批次ID=batch_id)
                instance.地块 = batch_obj.地块

                # 解析批次ID以获取二级分类
                # 假设批次ID格式为 "XQA-240106-冬娃娃菜"
                try:
                    secondary_category = batch_id.split('-')[-1]
                except IndexError:
                    secondary_category = ""

                # 根据二级分类查询一级分类
                try:
                    classification_obj = JobCategoryInfo.objects.get(
                        category_level=2,
                        category_name=secondary_category
                    )
                    primary_category = classification_obj.parent_category.category_name if classification_obj.parent_category else ""
                except JobCategoryInfo.DoesNotExist:
                    primary_category = ""
                    # 添加错误消息或其他逻辑
                    messages.error(request, f"未找到二级分类 '{secondary_category}' 对应的一级分类。")

                # 赋值分类信息
                instance.品种 = secondary_category
                instance.品类 = primary_category

            except Plant_batch.DoesNotExist:
                instance.地块 = ""
                messages.error(request, f"批次ID '{batch_id}' 不存在。")
                # 根据需要，您可以选择不保存实例或进行其他处理
        # 处理批次获取地块
        batch = form.cleaned_data.get('批次')
        if batch:
            try:
                batch_obj = Plant_batch.objects.get(批次ID=batch)
                instance.地块 = batch_obj.地块
            except Plant_batch.DoesNotExist:
                instance.地块 = ""
                # 可以根据需要添加错误信息或其他逻辑

        instance.save()
        return redirect('/outbound/list/')  # 根据您的 URL 配置调整

    vehicles = Vehicle.objects.all()
    markets = Market.objects.all()
    return render(request, 'outbound_form.html', {
        "form": form,
        "title": "添加出库记录",
        "vehicles": vehicles,
        "markets": markets,
    })
def outbound_edit(request, nid):
    """编辑出库记录"""
    row_object = get_object_or_404(OutboundRecord, id=nid)
    if request.method == "GET":
        form = OutboundRecordEditForm(instance=row_object)
        # print(form)
        return render(request, 'outbound_edit_form.html', {"form": form, "title": "编辑出库记录"})

    form = OutboundRecordEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/outbound/list/')
    return render(request, 'outbound_edit_form.html', {"form": form, "title": "编辑出库记录"})

def outbound_delete(request, nid):
    """删除出库记录"""
    OutboundRecord.objects.filter(id=nid).delete()
    return redirect('/outbound/list/')

def plot_autocomplete(request):
    term = request.GET.get('term','')
    qs = Plant_batch.objects.filter(地块__icontains=term).values_list('地块', flat=True).distinct()[:10]
    data = [{"label": x, "value": x} for x in qs]
    return JsonResponse(data, safe=False)


def get_batch_by_plot(request):
    plot_val = request.GET.get('plot','')
    qs = Plant_batch.objects.filter(地块=plot_val).values_list('批次ID', flat=True)
    data = list(qs)  # ["TXA-123xx","xxxx"]
    return JsonResponse(data, safe=False)