from django.http import JsonResponse
from app01.models import Plant_batch, BaseInfoWorkHour
from app01.utils.form import WorkHourFormSet


def autocomplete(request):
    # print('11111')
    if 'term' in request.GET:
        qs = Plant_batch.objects.filter(批次ID__icontains=request.GET.get('term'))
        titles = list()
        for plant in qs:
            titles.append(plant.批次ID)
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
