from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Plant_batch, BaseInfoBase, JobCategoryInfo
from app01.utils.form import PlantBatchEditForm, PlantBatchCreateForm

from app01.utils.pagination import Pagination

def Plant_batch_list(request):
    """ 批次列表 """
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["批次ID__contains"] = search_data

    queryset = Plant_batch.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'Plant_batch.html', context)

# 新增视图
def Plant_batch_add(request):
    if request.method == "GET":
        form = PlantBatchCreateForm()
        bases = BaseInfoBase.objects.all()
        job_categories = JobCategoryInfo.objects.filter(category_level=2)
        return render(request, 'Plant_batch_add.html', {
            "form": form,
            "bases": bases,
            "job_categories": job_categories
        })

    form = PlantBatchCreateForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/Plant_batch/list/')

    bases = BaseInfoBase.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    return render(request, 'Plant_batch_add.html', {
        "form": form,
        "bases": bases,
        "job_categories": job_categories
    })

# 编辑视图
def Plant_batch_edit(request, nid):
    # 获取对应的批次对象，如果不存在则返回 404
    row_object = get_object_or_404(Plant_batch, ID=nid)

    if request.method == "GET":
        # 创建编辑表单实例并预填充当前数据
        form = PlantBatchEditForm(instance=row_object)

        # 获取所有基地和二级分类数据
        bases = BaseInfoBase.objects.all()
        job_categories = JobCategoryInfo.objects.filter(category_level=2)

        return render(request, 'Plant_batch_edit.html', {
            "form": form,
            "bases": bases,
            "job_categories": job_categories
        })

    # 提交后的表单处理
    form = PlantBatchEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/Plant_batch/list/')

    # 如果表单验证失败，重新加载编辑页面
    bases = BaseInfoBase.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)

    return render(request, 'Plant_batch_edit.html', {
        "form": form,
        "bases": bases,
        "job_categories": job_categories
    })

def Plant_batch_delete(request, nid):
    """ 删除批次 """
    Plant_batch.objects.filter(ID=nid).delete()
    return redirect('/Plant_batch/list/')