from django.shortcuts import render, redirect, get_object_or_404
from app01 import models
from django.contrib import messages

from app01.models import DailyPriceReport, Market, JobCategoryInfo


def daily_price_report(request):
    markets = Market.objects.all()
    job_categories = JobCategoryInfo.objects.filter(category_level=2)

    if request.method == 'POST':
        formset_data = request.POST
        date = formset_data.get('date')

        for category in job_categories:
            for market in markets:
                price_key = f'price_{category.id}_{market.id}'
                price = formset_data.get(price_key)

                if price:
                    DailyPriceReport.objects.update_or_create(
                        日期=date,
                        品种=category,
                        市场=market,
                        defaults={'价格': price}
                    )
        return redirect('/daily_price_report/')

    return render(request, 'daily_price_report.html', {
        'markets': markets,
        'job_categories': job_categories,
    })


