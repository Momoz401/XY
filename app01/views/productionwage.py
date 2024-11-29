from django.db.models import Sum, Min, Max
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType, ProductionWage, Plant_batch, JobCategoryInfo, \
    JobTypeDetailInfo, BaseInfoBase

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm, production_wage_ModelForm, \
    production_wage_Edit_ModelForm, FixedFieldsForm, DynamicFieldsFormSet, DynamicFieldsForm


def production_wage_list(request):
    """ 工时列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["工种__contains"] = search_data

    queryset = models.ProductionWage.objects.filter(**data_dict).order_by("-id")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'productionwage.html', context)


# 获得基地信息
def get_base_options(request):
    bases = BaseInfoBase.objects.values('代号', '基地')  # 使用实际的字段名称
    base_options = {str(base['代号']): base['基地'] for base in bases}  # 将 ID 转换为字符串以符合 JSON 格式
    return JsonResponse(base_options)


def production_wage_add(request):
    if request.method == 'POST':
        # 将POST数据传递给固定表单和表单集
        fixed_form = FixedFieldsForm(request.POST)
        formset = DynamicFieldsFormSet(request.POST)
        # print(formset)
        # 如果固定表单和表单集都有效，则保存数据并重定向
        if fixed_form.is_valid() and formset.is_valid():
            fixed_instance = fixed_form.save(commit=False)
            # fixed_instance.save()  # 首先保存固定实例
            instances = formset.save(commit=False)
            for instance in instances:
                instance.日期 = fixed_instance.日期
                instance.工人 = fixed_instance.工人
                instance.负责人 = fixed_instance.负责人
                # instance.基地 = fixed_instance.基地

                # 查询基地的中文名称并保存
                base_code = instance.基地
                # print(base_code)
                if base_code:
                    try:
                        base_info = BaseInfoBase.objects.get(代号=base_code)
                        instance.基地 = base_info.基地  # 保存基地的中文名称
                    except BaseInfoBase.DoesNotExist:
                        print(f"基地代号 '{base_code}' 不存在")
                # 获取二级分类名称，并根据它查找对应的一级分类
                second_category_name = instance.二级分类
                try:
                    second_category_instance = JobCategoryInfo.objects.get(category_name=second_category_name,
                                                                           category_level=2)

                    # 获取并设置一级分类的名称
                    if second_category_instance.parent_category:
                        instance.一级分类 = second_category_instance.parent_category.category_name
                    else:
                        print(f"二级分类 '{second_category_name}' 没有对应的一级分类")

                except JobCategoryInfo.DoesNotExist:
                    print(f"二级分类 '{second_category_name}' 不存在")

                # 查询一级工种的中文名称并保存
                primary_work_id = instance.一级工种  # 假设一级工种字段当前存储的是ID
                if primary_work_id:
                    try:
                        primary_work_info = JobTypeDetailInfo.objects.get(id=primary_work_id)
                        instance.一级工种 = primary_work_info.job_name  # 保存一级工种的中文名称
                    except JobTypeDetailInfo.DoesNotExist:
                        print(f"一级工种 ID '{primary_work_id}' 不存在")

                # 查询二级工种的中文名称并保存
                secondary_work_id = instance.二级工种  # 假设二级工种字段当前存储的是ID
                if secondary_work_id:
                    try:
                        # 从 JobTypeDetailInfo 模型中查询二级工种的名称
                        secondary_work_info = JobTypeDetailInfo.objects.get(id=secondary_work_id)
                        instance.二级工种 = secondary_work_info.job_name  # 保存二级工种的中文名称
                    except JobTypeDetailInfo.DoesNotExist:
                        print(f"二级工种 ID '{secondary_work_id}' 不存在")
                instance.save()

                # 更新批次表
                batch = Plant_batch.objects.filter(批次ID=instance.批次).first()
                if batch:
                    工种名称 = instance.一级工种  # 获取工种名称（如“除草”）

                    工种字段映射 = {
                        '打地': ('打地开始时间', '打地结束时间', '打地数量', '打地周期'),
                        '移栽': ('移栽开始时间', '移栽结束时间', '移栽数量', '移栽周期'),
                        '除草': ('除草开始时间', '除草结束时间', '除草数量', '除草周期'),
                        '采收': ('采收开始时间', '采收结束时间', '采收数量', '采收周期'),
                        '清棚': ('清棚开始时间', '清棚结束时间', '清棚数量', '清棚周期'),
                        '点籽': ('点籽开始时间', '点籽结束时间', '点籽数量', '点籽周期'),
                        '间菜': ('间菜开始时间', '间菜结束时间', '间菜数量', '间菜周期'),
                        '吹生菜': ('吹生菜开始时间', '吹生菜结束时间', '吹生菜数量', '吹生菜周期'),
                        '施肥': ('施肥开始时间', '施肥结束时间', '施肥数量', '施肥周期'),
                    }

                    if 工种名称 in 工种字段映射:
                        开始时间字段, 结束时间字段, 数量字段, 周期字段 = 工种字段映射[工种名称]

                        # 汇总数量 - 计算所有相关记录的数量总和
                        total_quantity = \
                        ProductionWage.objects.filter(批次=instance.批次, 一级工种=instance.一级工种).aggregate(
                            total_quantity=Sum('数量'))['total_quantity']

                        # 计算最小的开始时间和最大的结束时间
                        start_time = \
                        ProductionWage.objects.filter(批次=instance.批次, 一级工种=instance.一级工种).aggregate(
                            min_start_time=Min('日期'))['min_start_time']
                        end_time = \
                        ProductionWage.objects.filter(批次=instance.批次, 一级工种=instance.一级工种).aggregate(
                            max_end_time=Max('日期'))['max_end_time']

                        # 计算周期（最大结束时间 - 最小开始时间，单位：天）
                        if start_time and end_time:
                            period = (end_time - start_time).days
                        else:
                            period = 0

                        # 更新批次表中的数据
                        if start_time:
                            setattr(batch, 开始时间字段, start_time)
                        if end_time:
                            setattr(batch, 结束时间字段, end_time)
                        if total_quantity:
                            setattr(batch, 数量字段, total_quantity)
                        if period:
                            setattr(batch, 周期字段, period)

                        # 计算总产量、总亩产
                        if instance.一级工种 == "采收":
                            total_yield = ProductionWage.objects.filter(批次=instance.批次, 一级工种="采收").aggregate(
                                total_yield=Sum('数量'))['total_yield']
                            batch.总产量 = total_yield if total_yield else 0
                            batch.总亩产 = batch.总产量 / (batch.面积 or 1)  # 总亩产 = 总产量 / 面积

                        # 计算总周期天数（采收末期 - 种植日期）
                        if start_time and end_time:
                            batch.总周期天数 = (end_time - start_time).days

                        # 填充批次周期（例如：240401-240525）
                        batch.周期批次 = f"{start_time.strftime('%y%m%d')}-{end_time.strftime('%y%m%d')}"

                        batch.save()

            formset.save_m2m()
            return redirect('/production_wage_list/list')
        else:
            # 如果有验证错误，打印错误信息以便调试
            #print(fixed_form.errors)  # 打印固定表单的错误
            #print(formset.errors)  # 打印表单集的错误
            # 在这里可以进一步处理验证错误
            pass

    else:
        # 如果是GET请求，创建空的固定表单和表单集
        fixed_form = FixedFieldsForm()
        formset = DynamicFieldsFormSet(queryset=ProductionWage.objects.none())
    {}
    # 渲染模板并将固定表单和表单集传递给模板
    return render(request, 'productionwate_add.html',
                  {'fixed_form': fixed_form, 'formset': formset, 'redirect': '/production_wage_list/list'})


def get_productionwate(request):
    if request.method == 'GET':
        # 解码参数
        level_one_id = request.GET.get('one', None)
        level_tow_id = request.GET.get('tow', None)
        # print(level_tow_id)
        # print(level_one_id)

        # 根据一级分类和二级分类活动工种和价格
        if level_tow_id is not None:
            work_type = BaseInfoWorkHour.objects.filter(一级分类=level_one_id, 二级分类=level_tow_id).values_list(
                '工种', '工种')
            # print(work_type)
            return JsonResponse(dict(work_type))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)


# 获得公价

def get_productionwate_price(request):
    if request.method == 'GET':
        # 解码参数
        second_category_name = request.GET.get('one', None)  # 二级分类
        primary_work_type_name = request.GET.get('tow', None)  # 一级工种
        secondary_work_type_name = request.GET.get('three', None)  # 二级工种

        # 验证输入参数是否齐全
        if second_category_name and primary_work_type_name and secondary_work_type_name:
            # 根据二级分类、一级工种和二级工种查找工价
            work_type = BaseInfoWorkHour.objects.filter(
                二级分类__category_name=second_category_name,
                一级工种__job_name=primary_work_type_name,
                二级工种__job_name=secondary_work_type_name
            ).values_list('工种ID', '单价')

            # 将查询结果转换为字典格式
            work_type_dict = {str(item[0]): item[1] for item in work_type}
            return JsonResponse(work_type_dict)
        else:
            return JsonResponse({'error': '参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)


def get_Plant_batch_dk(request):
    if request.method == 'GET':
        # 解码参数
        level_one_id = request.GET.get('one', None)

        # 根据一级分类和二级分类活动工种和价格
        if level_one_id is not None:
            dikuai = Plant_batch.objects.filter(批次ID=level_one_id).values_list('地块', '地块')
            # print(work_type)
            return JsonResponse(dict(dikuai))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)


def get_primary_work_types(request):
    try:
        # 获取一级工种的数据
        primary_work_types = JobTypeDetailInfo.objects.filter(job_level=1).values('id', 'job_name')

        # 构建包含 ID 和名称的列表
        primary_work_type_data = [
            {'id': work_type['id'], 'name': work_type['job_name']}
            for work_type in primary_work_types
        ]

        # 返回 ID 和名称组成的 JSON 响应
        return JsonResponse(primary_work_type_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': '获取一级工种失败', 'details': str(e)}, status=500)


def get_secondary_work_types(request):
    primary_work_type_name = request.GET.get('primary_work_type_name', '')

    # 打印选择的一级工种名称
    # print(f"Selected Primary Work Type Name: {primary_work_type_name}")

    # 查询父工种名称对应的工种
    secondary_work_types = JobTypeDetailInfo.objects.filter(
        parent_job__job_name=primary_work_type_name, job_level=2
    ).values('id', 'job_name')

    # 打印二级工种查询集
    # print(f"Secondary Work Types Queryset: {secondary_work_types}")

    data = list(secondary_work_types)
    # print(f"Data to return: {data}")

    return JsonResponse(data, safe=False)


def productionwate_edit(request, nid):
    """ 编辑工时 """
    row_object = models.ProductionWage.objects.filter(id=nid).first()

    if request.method == "GET":
        form = production_wage_Edit_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = production_wage_Edit_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/production_wage_list/list')

    return render(request, 'pretty_edit.html', {"form": form})


def production_wage_delete(request, nid):
    models.ProductionWage.objects.filter(id=nid).delete()
    return redirect('/production_wage_list/list')
