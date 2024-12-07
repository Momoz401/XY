from django.shortcuts import render, redirect
from app01.models import DailyPriceReport, Market, JobCategoryInfo
from datetime import date

def daily_price_report(request):
    markets = Market.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    today = date.today().isoformat()  # 获取今天的日期

    # 获取最新的价格数据并组织为嵌套字典
    latest_prices = {}
    for category in job_categories:
        latest_prices[category.id] = {}
        for market in markets:
            latest_entry = DailyPriceReport.objects.filter(品种=category, 市场=market).order_by('-日期').first()
            latest_prices[category.id][market.id] = {
                '价格': latest_entry.价格 if latest_entry else '',
                '价格上限': latest_entry.价格上限 if latest_entry else '',
            }

    if request.method == 'POST':
        formset_data = request.POST
        report_date = formset_data.get('date', today)  # 如果没有选择日期，使用今天的日期

        for category in job_categories:
            for market in markets:
                price_key = f'price_{category.id}_{market.id}'
                max_price_key = f'max_price_{category.id}_{market.id}'
                price = formset_data.get(price_key)
                max_price = formset_data.get(max_price_key)

                if price and max_price:  # 只有在两个价格都不为空时才提交
                    DailyPriceReport.objects.update_or_create(
                        日期=report_date,
                        品种=category,
                        市场=market,
                        defaults={'价格': price, '价格上限': max_price}
                    )
        return redirect('/daily_price_report/list/')

    return render(request, 'daily_price_report.html', {
        'markets': markets,
        'job_categories': job_categories,
        'today': today,
        'latest_prices': latest_prices,
    })