from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType,ProductionWage

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm, production_wage_ModelForm, \
    production_wage_Edit_ModelForm, FixedFieldsForm, DynamicFieldsFormSet


def production_wage_list(request):
    """ 工时列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["工种__contains"] = search_data

    queryset = models.ProductionWage.objects.filter(**data_dict).order_by("-日期")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'productionwage.html', context)


def production_wage_add(request):
    if request.method == 'POST':
        fixed_form = FixedFieldsForm(request.POST)
        print(request.POST)
        formset = DynamicFieldsFormSet(request.POST, queryset=ProductionWage.objects.none())
        if fixed_form.is_valid() and formset.is_valid():
            fixed_instance = fixed_form.save(commit=False)
            instances = formset.save(commit=False)  # 获取所有实例，但不保存到数据库中

            for instance in instances:
                instance.日期 = fixed_instance.日期
                instance.工人 = fixed_instance.工人
                instance.批次 = fixed_instance.批次
                instance.save()  # 保存每个实例

            formset.save_m2m()  # 保存多对多关系，如果有的话
            return redirect('/production_wage_list/list')
    else:
        fixed_form = FixedFieldsForm()
        formset = DynamicFieldsFormSet(queryset=ProductionWage.objects.none())
    return render(request, 'productionwate_add.html', {'fixed_form': fixed_form, 'formset': formset})


def get_productionwate(request):
    if request.method == 'GET' :
        # 解码参数
        level_one_id = request.GET.get('one', None)
        level_tow_id = request.GET.get('tow', None)

        # 根据一级分类和二级分类活动工种和价格
        if level_tow_id is not None:
            work_type = BaseInfoWorkHour.objects.filter(一级分类=level_one_id ,二级分类=level_tow_id).values_list('工种ID', '工种')
            # print(work_type)
            return JsonResponse(dict(work_type))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)
#获得公价
def get_productionwate_price(request):
    if request.method == 'GET' :
        # 解码参数
        level_one_id = request.GET.get('one', None)
        level_tow_id = request.GET.get('tow', None)
        level_three_id = request.GET.get('three', None)

        # 根据一级分类和二级分类活动工种和价格
        if level_tow_id is not None:
            work_type = BaseInfoWorkHour.objects.filter(一级分类=level_one_id ,二级分类=level_tow_id,工种=level_three_id).values_list('工种ID', '单价')
            # print(work_type)
            return JsonResponse(dict(work_type))
        else:
            return JsonResponse({'error': '一级分类_id 参数缺失'}, status=400)
    else:
        return JsonResponse({'error': '无效请求'}, status=400)






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
