from django.shortcuts import render

from app01.models import Plant_batch

# 这里要设计一个日历的生产情况
def plant_batch_calendar_view(request):
    # 获取所有批次的记录
    plant_batches = Plant_batch.objects.all().values('批次ID', '移栽日期', '点籽日期', '采收初期', '采收末期')

    # 创建一个事件列表
    events = []
    for batch in plant_batches:
        if batch['移栽日期']:
            events.append({
                'title': f"移栽: {batch['批次ID']}",
                'start': batch['移栽日期'].strftime('%Y-%m-%d'),
                'color': 'green',
            })
        if batch['点籽日期']:
            events.append({
                'title': f"点籽: {batch['批次ID']}",
                'start': batch['点籽日期'].strftime('%Y-%m-%d'),
                'color': 'blue',
            })
        if batch['采收初期']:
            events.append({
                'title': f"采收初期: {batch['批次ID']}",
                'start': batch['采收初期'].strftime('%Y-%m-%d'),
                'color': 'orange',
            })
        if batch['采收末期']:
            events.append({
                'title': f"采收末期: {batch['批次ID']}",
                'start': batch['采收末期'].strftime('%Y-%m-%d'),
                'color': 'red',
            })

    context = {
        'events': events
    }

    return render(request, 'plant_batch_calendar.html', context)
