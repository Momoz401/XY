from django.http import JsonResponse
from django.shortcuts import render
from numpy.random import random

from app01.models import DailyPriceReport, JobCategoryInfo, Market
from datetime import timedelta, date, datetime
from django.db.models import Avg
import json


def get_price_trends(request):
    """价格走势页面"""
    # 获取查询参数
    category_id = request.GET.get('category_id')
    date_filter = request.GET.get('date_filter', 'week')

    # 时间范围过滤逻辑
    start_date = date.today() - timedelta(days=7)  # 默认最近一周
    title = "最近一周价格走势"
    if date_filter == 'month':
        start_date = date.today() - timedelta(days=30)
        title = "最近一个月价格走势"
    elif date_filter == 'year':
        start_date = date.today() - timedelta(days=365)
        title = "最近一年价格走势"

    # 验证品种 ID 是否有效
    if category_id and not JobCategoryInfo.objects.filter(id=category_id).exists():
        category_id = None

    # 查询数据
    price_data = DailyPriceReport.objects.filter(日期__gte=start_date)
    if category_id:
        price_data = price_data.filter(品种_id=category_id)

    # 聚合市场数据
    available_markets = Market.objects.all()
    market_data = {}
    for market in available_markets:
        market_name = market.市场名称
        market_id = market.id  # 获取市场 ID

        # 查询市场的价格数据
        market_prices = (
            price_data.filter(市场_id=market_id)
            .values('日期')
            .annotate(avg_price=Avg('价格'))  # 确保 '价格' 字段名称正确
            .order_by('日期')
        )

        # 打印调试信息
        print(f"Market: {market_name} (ID: {market_id}), Prices: {list(market_prices)}")

        # 获取日期和价格列表
        dates = [entry['日期'].strftime("%Y-%m-%d") for entry in market_prices]
        prices = [float(entry['avg_price']) for entry in market_prices]

        # 检查是否有数据
        if dates and prices:
            market_data[market_name] = {'dates': dates, 'prices': prices}
        else:
            print(f"Skipping market: {market_name} (ID: {market_id}) due to no data")

    # 打印最终 market_data 调试
    print("Final Market Data:", json.dumps(market_data, ensure_ascii=False, indent=2))

    # 构造上下文数据
    context = {
        'title': title,
        'available_categories': JobCategoryInfo.objects.all(),
        'selected_category': int(category_id) if category_id else None,
        'date_filter': date_filter,
        'market_data': json.dumps(market_data),  # 将数据传递到前端
    }

    return render(request, 'price_trends.html', context)



def get_available_categories(request):
    """ 获取所有可用的品种列表 """
    categories = list(JobCategoryInfo.objects.values('id', 'category_name'))
    return JsonResponse(categories, safe=False)