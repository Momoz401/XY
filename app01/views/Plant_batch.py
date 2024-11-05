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

    queryset = Plant_batch.objects.filter(**data_dict).order_by('-种植日期')
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
        instance = form.save(commit=False)
        # 使用批次号处理函数获取所需数据
        batch_id, second_category, primary_category, base_name = process_batch_id(instance.批次ID)

        # 更新实例字段
        instance.批次ID = batch_id
        instance.二级分类 = second_category
        instance.一级分类 = primary_category
        instance.基地 = base_name

        instance.save()
        return redirect('/Plant_batch/list/')

    bases = BaseInfoBase.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    return render(request, 'Plant_batch_add.html', {
        "form": form,
        "bases": bases,
        "job_categories": job_categories
    })
def process_batch_id(batch_id):
    # 假设批次号格式为 "TXA-20241105-夏黄白"
    parts = batch_id.split("-")
    if len(parts) < 3:
        return None, None, None, None  # 批次号格式不正确

    base_code = parts[0]  # 基地代号
    date_part = parts[1]   # 日期部分
    second_category = parts[2]  # 二级分类

    # 日期部分处理为简短格式，比如 "20241105" 转换为 "241105"
    short_date = date_part[2:] if len(date_part) == 8 else date_part

    # 获取一级分类
    primary_category = None
    try:
        second_category_instance = JobCategoryInfo.objects.get(category_name=second_category, category_level=2)
        primary_category = second_category_instance.parent_category.category_name if second_category_instance.parent_category else None
    except JobCategoryInfo.DoesNotExist:
        print(f"二级分类 '{second_category}' 不存在")

    # 获取基地名称
    base_name = None
    try:
        base_instance = BaseInfoBase.objects.get(代号=base_code)
        base_name = base_instance.基地
    except BaseInfoBase.DoesNotExist:
        print(f"基地代号 '{base_code}' 不存在")

    return f"{base_code}-{short_date}-{second_category}", second_category, primary_category, base_name
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