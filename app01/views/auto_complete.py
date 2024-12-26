from django.http import JsonResponse

from app01.models import Vehicle, Plant_batch, Customer


def vehicle_autocomplete(request):
    term = request.GET.get('term','')
    qs = Vehicle.objects.filter(车牌__icontains=term)[:10]
    data = [{"label": v.车牌, "value": v.车牌} for v in qs]
    return JsonResponse(data, safe=False)

def batch_autocomplete(request):
    """批次自动完成视图"""
    if 'q' in request.GET:
        q = request.GET.get('q')
        batches = Plant_batch.objects.filter(批次ID__icontains=q)[:10]
        results = [{'id': batch.id, 'text': batch.批次ID} for batch in batches]
    else:
        results = []
    return JsonResponse({'results': results})
