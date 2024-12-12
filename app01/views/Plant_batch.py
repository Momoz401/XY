from datetime import datetime, timedelta

import pandas as pd
from django.http import HttpResponse
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

    context = {
        "queryset": queryset,      # 传递所有过滤后的数据
        "search_data": search_data # 保留搜索数据
    }
    return render(request, 'Plant_batch.html', context)

# 新增视图

def export_plant_batches(request):
    # 获取批次数据
    queryset = Plant_batch.objects.all()

    # 将查询结果转换为DataFrame
    data = list(queryset.values())
    df = pd.DataFrame(data)

    # 设置HTTP响应头
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="批次表.csv"'

    # 将DataFrame导出为CSV格式并写入HttpResponse
    df.to_csv(response, index=False, encoding='utf-8-sig')

    return response


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

        # 获取前端传来的批次ID
        batch_id = instance.批次ID

        # 使用批次号处理函数获取所需数据
        batch_id, second_category, primary_category, base_name = process_batch_id(batch_id)

        # 更新实例字段
        instance.批次ID = batch_id
        instance.二级分类 = second_category
        instance.一级分类 = primary_category
        instance.基地 = base_name

        # 处理栽种方式，计算采收日期
        if instance.栽种方式 == '移栽':
            instance.移栽日期 = request.POST.get('移栽日期')
            instance.移栽板量 = request.POST.get('移栽板量')
            instance.移栽数量 = request.POST.get('移栽数量')
        elif instance.栽种方式 == '点籽':
            instance.点籽日期 = request.POST.get('点籽日期')
            instance.用籽量 = request.POST.get('用籽量')

        # 计算采收初期和采收末期
        if instance.种植日期 and instance.生长周期 and instance.采收期:
            try:
                planting_date = instance.种植日期
                growth_cycle = float(instance.生长周期)  # 将 decimal.Decimal 转为 float
                harvest_period = float(instance.采收期)  # 将 decimal.Decimal 转为 float

                # 计算采收初期和采收末期
                harvest_start_date = planting_date + timedelta(days=growth_cycle)
                harvest_end_date = harvest_start_date + timedelta(days=harvest_period)

                instance.采收初期 = harvest_start_date
                instance.采收末期 = harvest_end_date
            except ValueError:
                print("生长周期或采收期无效，请检查输入")

        # 保存批次数据
        instance.save()
        return redirect('/Plant_batch/list/')

    # 如果表单无效，重新加载页面并显示错误
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




def Plant_batch_query(request):
    """ 批次信息查询 """
    data_dict = {}
    search_data = request.GET.get('q', "")  # 获取查询条件（批次ID）
    if search_data:
        data_dict["批次ID__contains"] = search_data  # 过滤批次ID

    # 查询匹配的批次
    queryset = Plant_batch.objects.filter(**data_dict).order_by('-种植日期')

    # 处理查询结果：将每个批次的工种相关数据提取出来
    result = []
    for batch in queryset:
        job_data = {
            '批次ID': batch.批次ID,
            '地块': batch.地块,
            '工种数据': []
        }

        # 遍历每个工种的开始时间、结束时间和数量（如果有）
        job_fields = [
            ('收苗', batch.收苗开始时间, batch.收苗结束时间, batch.收苗数量),
            ('打地', batch.打地开始时间, batch.打地结束时间, batch.打地数量),
            ('移栽', batch.移栽开始时间, batch.移栽结束时间, batch.移栽数量),
            ('除草', batch.除草开始时间, batch.除草结束时间, batch.除草数量),
            ('采收', batch.采收开始时间, batch.采收结束时间, batch.采收数量),
            ('清棚', batch.清棚开始时间, batch.清棚结束时间, batch.清棚数量),
            ('点籽', batch.点籽开始时间, batch.点籽结束时间, batch.点籽数量),
            ('间菜', batch.间菜开始时间, batch.间菜结束时间, batch.间菜数量),
            ('吹生菜', batch.吹生菜开始时间, batch.吹生菜结束时间, batch.吹生菜数量),
            ('施肥', batch.施肥开始时间, batch.施肥结束时间, batch.施肥数量),
        ]

        # 将工种数据添加到批次中
        for job in job_fields:
            job_data['工种数据'].append({
                '工种': job[0],
                '开始时间': job[1] if job[1] else '未设定',
                '结束时间': job[2] if job[2] else '未设定',
                '数量': job[3] if job[3] else '未设定'
            })

        result.append(job_data)

    context = {
        'result': result,  # 将结果传递到模板
        'search_data': search_data  # 保留搜索的批次ID
    }

    return render(request, 'plant_batch_query.html', context)