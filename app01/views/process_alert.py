from django.core.paginator import Paginator
from django.db import connection

from django.shortcuts import render, redirect, get_object_or_404

from app01.models import ProcessAlert
from app01.utils.form import ProcessAlertForm
from app01.utils.pagination import Pagination

def process_alert_list(request):
    # 获取去重的二级分类
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT 二级分类名称
            FROM view_baseinfoworkhour_with_names
        """)
        secondary_categories = [row[0] for row in cursor.fetchall()]

    # 获取搜索查询或默认值
    search_query = request.GET.get('q', '夏黄白')

    # 获取基础数据，按二级分类筛选
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                一级分类名称,
                二级分类名称,
                一级工种名称,
                二级工种名称
            FROM view_baseinfoworkhour_with_names
            WHERE 二级分类名称 = %s
        """, [search_query])
        base_data = cursor.fetchall()

    # 获取已有的流程预警数据
    existing_alerts = {(
        alert.一级分类,
        alert.二级分类,
        alert.一级工种,
        alert.二级工种
    ): alert for alert in ProcessAlert.objects.all()}

    alerts = []
    for row in base_data:
        key = (row[0], row[1], row[2], row[3])
        alert = existing_alerts.get(key)
        alerts.append({
            '一级分类': row[0],
            '二级分类': row[1],
            '一级工种': row[2],
            '二级工种': row[3],
            '最小时间': alert.最小时间 if alert else None,
            '最大时间': alert.最大时间 if alert else None,
            'alert_id': alert.id if alert else None,
        })

    context = {
        'alerts': alerts,
        'secondary_categories': secondary_categories,  # 传递去重的二级分类
        'search_query': search_query  # 保持原搜索功能一致，并将默认值传递
    }

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('save_'):
                index = key.split('_')[1]
                category_data = request.POST.get(f'category_data_{index}').split('|')
                min_time = request.POST.get(f'min_time_{index}')
                max_time = request.POST.get(f'max_time_{index}')

                # 创建或更新 ProcessAlert 记录
                ProcessAlert.objects.update_or_create(
                    一级分类=category_data[0],
                    二级分类=category_data[1],
                    一级工种=category_data[2],
                    二级工种=category_data[3],
                    defaults={'最小时间': min_time, '最大时间': max_time}
                )

        return redirect('process_alert_list')  # 重定向到列表页面

    return render(request, 'process_alert_list.html', context)
def process_alert_create(request):
    if request.method == 'POST':
        form = ProcessAlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('process_alert_list')
    else:
        form = ProcessAlertForm()
    return render(request, 'process_alert_form.html', {'form': form})

def process_alert_update(request, pk):
    alert = get_object_or_404(ProcessAlert, pk=pk)
    if request.method == 'POST':
        form = ProcessAlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('process_alert_list')
    else:
        form = ProcessAlertForm(instance=alert)
    return render(request, 'process_alert_form.html', {'form': form})

def process_alert_delete(request, pk):
    alert = get_object_or_404(ProcessAlert, pk=pk)
    if request.method == 'POST':
        alert.delete()
        return redirect('process_alert_list')
    return render(request, 'process_alert_confirm_delete.html', {'alert': alert})
def process_alert_create(request):
    if request.method == 'POST':
        form = ProcessAlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('process_alert_list')
    else:
        form = ProcessAlertForm()
    return render(request, 'process_alert_form.html', {'form': form})

def process_alert_update(request, pk):
    alert = get_object_or_404(ProcessAlert, pk=pk)
    if request.method == 'POST':
        form = ProcessAlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('process_alert_list')
    else:
        form = ProcessAlertForm(instance=alert)
    return render(request, 'process_alert_form.html', {'form': form})

def process_alert_delete(request, pk):
    alert = get_object_or_404(ProcessAlert, pk=pk)
    if request.method == 'POST':
        alert.delete()
        return redirect('process_alert_list')
    return render(request, 'process_alert_confirm_delete.html', {'alert': alert})


