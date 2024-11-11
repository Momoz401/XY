from django.shortcuts import render
from app01.models import DailyPriceReport, JobCategoryInfo, Market
from datetime import timedelta, date
from django.db.models import Avg
import json
from django.http import JsonResponse

from django.shortcuts import render
from app01.models import DailyPriceReport, JobCategoryInfo, Market
from datetime import timedelta, date
from django.db.models import Avg
import json

def get_price_trends(request):
    """ 价格走势页面 """
    category_id = request.GET.get('category_id', None)
    date_filter = request.GET.get('date_filter', 'week')

    # 获取所有市场和品种
    available_categories = JobCategoryInfo.objects.all()
    available_markets = Market.objects.all()

    # 过滤时间范围
    today = date.today()
    if date_filter == 'week':
        start_date = today - timedelta(days=7)
        title = "最近一周价格走势"
    elif date_filter == 'month':
        start_date = today - timedelta(days=30)
        title = "最近一个月价格走势"
    elif date_filter == 'year':
        start_date = today - timedelta(days=365)
        title = "最近一年价格走势"
    else:
        start_date = today - timedelta(days=7)
        title = "最近一周价格走势"

    # 价格数据过滤和聚合
    price_data = DailyPriceReport.objects.filter(日期__gte=start_date)
    if category_id:
        price_data = price_data.filter(品种_id=category_id)

    market_data = {}
    for market in available_markets:
        market_name = market.市场名称
        market_prices = price_data.filter(市场_id=market.id).values('日期').annotate(avg_price=Avg('价格')).order_by('日期')
        dates = [entry['日期'].strftime("%Y-%m-%d") for entry in market_prices]
        prices = [float(entry['avg_price']) for entry in market_prices]
        market_data[market_name] = {'dates': dates, 'prices': prices}

    context = {
        'title': title,
        'available_categories': available_categories,
        'available_markets': available_markets,
        'selected_category': int(category_id) if category_id else None,
        'date_filter': date_filter,
        'market_data': json.dumps(market_data),
    }

    return render(request, 'price_trends.html', context)
def get_available_categories(request):
    """ 获取所有可用的品种列表 """
    categories = list(JobCategoryInfo.objects.values('id', 'category_name'))
    return JsonResponse(categories, safe=False)