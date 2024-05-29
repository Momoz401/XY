from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import BaseInfoWorkHour, BaseInfoWorkType,ProductionWage

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyEditModelForm, workHourModelForm, workHour_Edit_ModelForm, production_wage_ModelForm


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
    """ 添加工价 """
    if request.method == "GET":
        form = production_wage_ModelForm()
        return render(request, 'productionwate_add.html', {"form": form})
    form = production_wage_ModelForm(data=request.POST)
    # 限制一级工种只能从规定的类别列选择
    if form.is_valid():
        form.save()
        return redirect('/production_wage_list/list/')
    return render(request, 'productionwage.html', {"form": form})



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






def work_hour_edit(request, nid):
    """ 编辑工时 """
    row_object = models.BaseInfoWorkHour.objects.filter(工种ID=nid).first()

    if request.method == "GET":
        form = workHour_Edit_ModelForm(instance=row_object)
        return render(request, 'work_type_edit.html', {"form": form})

    form = workHour_Edit_ModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/WorkHour/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def production_wage_delete(request, nid):
    models.Production_Wage.objects.filter(ID=nid).delete()
    return redirect('/production_wage_list/list')
