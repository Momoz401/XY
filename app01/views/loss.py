from django.shortcuts import render, redirect, get_object_or_404

from app01.models import LossReport ,Plant_batch
from app01.utils.form import LossReportForm
from app01.utils.pagination import Pagination


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
        # 保存报损记录
        instance = form.save()

        # 获取报损信息
        batch_id = instance.批次
        loss_area = instance.报损面积
        loss_reason = instance.备注

        # 更新批次表中的报损信息
        try:
            plant_batch = Plant_batch.objects.get(批次ID=batch_id)

            # 汇总报损面积，添加到批次表
            plant_batch.销毁面积 = (plant_batch.销毁面积 or 0) + loss_area

            # 汇总报损原因（可以连接多个原因）
            if plant_batch.销毁备注:
                plant_batch.销毁备注 += " " + loss_reason
            else:
                plant_batch.销毁备注 = loss_reason

            # 保存批次表
            plant_batch.save()

        except Plant_batch.DoesNotExist:
            print(f"未找到批次 {batch_id}，请检查批次ID是否正确")



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
