from django.shortcuts import render
from app01.models import DailyPriceReport, JobCategoryInfo
from datetime import timedelta, date
from django.db.models import Avg
import json
from django.http import JsonResponse

def get_price_trends(request):
    """ 价格走势页面 """
    # 获取查询参数
    category_id = request.GET.get('category_id', 1)  # 默认品种为 ID 1
    date_filter = request.GET.get('date_filter', 'week')  # 默认时间范围

    # 获取品种名称
    category = JobCategoryInfo.objects.filter(id=category_id).first()
    category_name = category.category_name if category else '未知品种'

    # 数据查询和过滤
    today = date.today()
    if date_filter == 'week':
        start_date = today - timedelta(days=7)
        title = f"{category_name} - 最近一周价格走势"
    elif date_filter == 'month':
        start_date = today - timedelta(days=30)
        title = f"{category_name} - 最近一个月价格走势"
    elif date_filter == 'year':
        start_date = today - timedelta(days=365)
        title = f"{category_name} - 最近一年价格走势"
    else:
        start_date = today - timedelta(days=7)
        title = f"{category_name} - 最近一周价格走势"

    # 获取价格数据
    price_data = (
        DailyPriceReport.objects.filter(品种_id=category_id, 日期__gte=start_date)
        .values('日期')
        .annotate(avg_price=Avg('价格'))
        .order_by('日期')
    )

    # 转换为前端需要的格式
    dates = [entry['日期'].strftime("%Y-%m-%d") for entry in price_data]
    prices = [entry['avg_price'] for entry in price_data]

    context = {
        'title': title,
        'dates': json.dumps(dates),
        'prices': json.dumps(prices),
        'category_id': category_id,
        'date_filter': date_filter,
    }

    return render(request, 'price_trends.html', context)

def get_available_categories(request):
    """ 获取所有可用的品种列表 """
    categories = list(JobCategoryInfo.objects.values('id', 'category_name'))
    return JsonResponse(categories, safe=False)