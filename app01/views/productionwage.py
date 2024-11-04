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
                #instance.基地 = fixed_instance.基地
                instance.save()
            formset.save_m2m()
            return redirect('/production_wage_list/list')
        else:
            # 如果有验证错误，打印错误信息以便调试
            print(fixed_form.errors)  # 打印固定表单的错误
            print(formset.errors)  # 打印表单集的错误
            # 在这里可以进一步处理验证错误

    else:
        # 如果是GET请求，创建空的固定表单和表单集
        fixed_form = FixedFieldsForm()
        formset = DynamicFieldsFormSet(queryset=ProductionWage.objects.none())
    {}
    # 渲染模板并将固定表单和表单集传递给模板
    return render(request, 'productionwate_add.html', {'fixed_form': fixed_form, 'formset': formset,'redirect': '/production_wage_list/list'})

def get_productionwate(request):
    if request.method == 'GET' :
        # 解码参数
        level_one_id = request.GET.get('one', None)
        level_tow_id = request.GET.get('tow', None)
        #print(level_tow_id)
        #print(level_one_id)

        # 根据一级分类和二级分类活动工种和价格
        if level_tow_id is not None:
            work_type = BaseInfoWorkHour.objects.filter(一级分类=level_one_id ,二级分类=level_tow_id).values_list('工种', '工种')
            print(work_type)
            return JsonResponse(dict(work_type))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)
#获得公价

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
    if request.method == 'GET' :
        # 解码参数
        level_one_id = request.GET.get('one', None)

        # 根据一级分类和二级分类活动工种和价格
        if level_one_id is not None:
            dikuai = Plant_batch.objects.filter(批次ID=level_one_id ).values_list('地块', '地块')
            # print(work_type)
            return JsonResponse(dict(dikuai))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)

def get_primary_work_types(request):
    second_category_name = request.GET.get('second_category', None)
    if second_category_name:
        try:
            # 获取二级分类ID
            second_category_id = JobCategoryInfo.objects.get(category_name=second_category_name).id

            # 查找对应的一级工种ID
            work_types = BaseInfoWorkHour.objects.filter(二级分类_id=second_category_id).values('一级工种').distinct()

            # 获取一级工种的中文名称
            primary_work_type_names = [
                JobTypeDetailInfo.objects.get(id=work_type['一级工种']).job_name
                for work_type in work_types
            ]

            # 构造 JSON 响应
            return JsonResponse(primary_work_type_names, safe=False)

        except JobCategoryInfo.DoesNotExist:
            return JsonResponse({'error': '未找到对应的二级分类'}, status=400)
    return JsonResponse({'error': '无效请求'}, status=400)

def get_secondary_work_types(request):
    primary_work_type_name = request.GET.get('primary_work_type_name', '')

    # 打印选择的一级工种名称
    print(f"Selected Primary Work Type Name: {primary_work_type_name}")

    # 查询父工种名称对应的工种
    secondary_work_types = JobTypeDetailInfo.objects.filter(
        parent_job__job_name=primary_work_type_name, job_level=2
    ).values('id', 'job_name')

    # 打印二级工种查询集
    print(f"Secondary Work Types Queryset: {secondary_work_types}")

    data = list(secondary_work_types)
    print(f"Data to return: {data}")

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
