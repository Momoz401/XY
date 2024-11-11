from django.shortcuts import render, redirect, get_object_or_404
from app01 import models
from django.contrib import messages

from app01.models import DailyPriceReport, Market, JobCategoryInfo
from datetime import date

def daily_price_report(request):
    markets = Market.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)
    today = date.today().isoformat()  # 获取今天的日期

    if request.method == 'POST':
        formset_data = request.POST
        report_date = formset_data.get('date', today)  # 如果没有选择日期，使用今天的日期

        for category in job_categories:
            for market in markets:
                price_key = f'price_{category.id}_{market.id}'
                price = formset_data.get(price_key)

                if price:  # 只有在价格不为空时才提交
                    DailyPriceReport.objects.update_or_create(
                        日期=report_date,
                        品种=category,
                        市场=market,
                        defaults={'价格': price}
                    )
        return redirect('/daily_price_report/list/')

    return render(request, 'daily_price_report.html', {
        'markets': markets,
        'job_categories': job_categories,
        'today': today,  # 将今天的日期传递给模板
    })


