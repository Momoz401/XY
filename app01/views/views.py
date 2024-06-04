
from django.http import JsonResponse
from app01.models import Plant_batch, BaseInfoWorkHour, BaseInfoBase
from app01.utils.form import WorkHourFormSet
from django.db.models.functions import Substr

from django.http import JsonResponse
from django.db.models.functions import Substr


def autocomplete(request):
    print(request.GET)
    if 'term' in request.GET:
        term = request.GET.get('term')
        baseId = request.GET.get('baseId')

        # 过滤批次ID包含term且批次ID的前三位等于baseId
        qs = Plant_batch.objects.annotate(
            prefix=Substr('批次ID', 1, 3)
        ).filter(
            批次ID__icontains=term,
            prefix=str(baseId)
        )

        # 构建返回的数据格式
        titles = [{'label': plant.批次ID, 'value': plant.批次ID} for plant in qs]

        return JsonResponse(titles, safe=False)

    return JsonResponse([], safe=False)


from django.shortcuts import render, redirect

def autocomplete_baseinfo(request):
    # 自动补全基地
    if 'term' in request.GET:
        qs = BaseInfoBase.objects.filter(代号__icontains=request.GET.get('term'))
        titles = list()
        for plant in qs:
            titles.append(plant.代号)
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)


from django.shortcuts import render, redirect








def add_multiple_work_hours(request):
    if request.method == 'POST':
        formset = WorkHourFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/production_wage_list/list')
    else:
        formset = WorkHourFormSet(queryset=BaseInfoWorkHour.objects.none())

    return render(request, 'add_multiple_work_hours.html', {'formset': formset})
