from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Market
from app01.utils.form import MarketForm
from app01.utils.pagination import Pagination


def market_list(request):
    """
    获取市场信息列表，并进行分页显示
    功能：根据市场名称进行搜索，支持模糊查询
    """
    data_dict = {}  # 存储过滤条件
    search_data = request.GET.get('q', "")  # 获取查询参数
    if search_data:
        data_dict["市场名称__icontains"] = search_data  # 根据市场名称模糊查询

    # 获取所有符合条件的市场数据，并按ID降序排列
    queryset = Market.objects.filter(**data_dict).order_by("-id")

    # 分页处理
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,  # 搜索框中显示的查询值
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码
    }

    # 渲染并返回市场列表页面
    return render(request, 'market_list.html', context)


def market_add(request):
    """
    添加新的市场信息
    功能：处理新建市场信息的表单提交和数据保存
    """
    if request.method == "GET":
        # 如果是GET请求，返回一个空的表单
        form = MarketForm()
        return render(request, 'market_form.html', {"form": form, "title": "新建市场信息"})

    # 如果是POST请求，处理表单数据
    form = MarketForm(data=request.POST)
    if form.is_valid():
        # 表单数据验证通过，保存数据
        form.save()
        # 保存成功后重定向到市场列表页面
        return redirect('/market/list/')

    # 如果表单无效，重新渲染表单并显示错误信息
    return render(request, 'market_form.html', {"form": form, "title": "新建市场信息"})


def market_edit(request, nid):
    """
    编辑已有的市场信息
    功能：根据市场ID查找市场信息，并提供表单编辑
    """
    row_object = get_object_or_404(Market, id=nid)  # 根据ID获取市场对象，如果不存在则返回404

    if request.method == "GET":
        # GET请求，返回该市场的表单，供用户编辑
        form = MarketForm(instance=row_object)
        return render(request, 'market_form.html', {"form": form, "title": "编辑市场信息"})

    # 如果是POST请求，处理编辑后的表单数据
    form = MarketForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 表单数据验证通过，保存编辑后的数据
        form.save()
        # 保存成功后重定向到市场列表页面
        return redirect('/market/list/')

    # 如果表单无效，重新渲染表单并显示错误信息
    return render(request, 'market_form.html', {"form": form, "title": "编辑市场信息"})


def market_delete(request, nid):
    """
    删除市场信息
    功能：根据市场ID删除市场数据
    """
    # 根据ID查找并删除市场信息
    Market.objects.filter(id=nid).delete()
    # 删除后重定向到市场列表页面
    return redirect('/market/list/')