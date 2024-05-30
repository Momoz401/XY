from django.http import JsonResponse
from app01.models import Plant_batch


def autocomplete(request):
    print('11111')
    if 'term' in request.GET:
        qs = Plant_batch.objects.filter(批次ID__icontains=request.GET.get('term'))
        titles = list()
        for plant in qs:
            titles.append(plant.批次ID)
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)