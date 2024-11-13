from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Salesperson
from app01.utils.form import SalespersonForm
from app01.utils.pagination import Pagination

def salesperson_list(request):
    """
    显示销售人员信息列表
    """
    # 初始化数据字典，用于存储查询条件
    data_dict = {}
    # 获取查询参数
    search_data = request.GET.get('q', "")
    if search_data:
        # 如果存在查询数据，将其加入过滤条件
        data_dict["姓名__icontains"] = search_data

    # 查询数据库，按ID倒序排列
    queryset = Salesperson.objects.filter(**data_dict).order_by("-id")
    # 分页处理
    page_object = Pagination(request, queryset)

    # 上下文数据
    context = {
        "search_data": search_data,  # 查询关键字
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 分页HTML
    }
    return render(request, 'salesperson_list.html', context)

def salesperson_add(request):
    """
    添加销售人员信息
    """
    if request.method == "GET":
        # 生成空表单
        form = SalespersonForm()
        return render(request, 'salesperson_form.html', {"form": form, "title": "新建销售人员信息"})

    # 处理POST请求的数据
    form = SalespersonForm(data=request.POST)
    if form.is_valid():
        # 数据有效，保存表单
        form.save()
        return redirect('/salesperson/list/')
    # 数据无效，重新渲染表单并显示错误信息
    return render(request, 'salesperson_form.html', {"form": form, "title": "新建销售人员信息"})

def salesperson_edit(request, nid):
    """
    编辑销售人员信息
    """
    # 获取要编辑的销售人员对象，如果不存在返回404错误
    row_object = get_object_or_404(Salesperson, id=nid)

    if request.method == "GET":
        # 将对象填充到表单中
        form = SalespersonForm(instance=row_object)
        return render(request, 'salesperson_form.html', {"form": form, "title": "编辑销售人员信息"})

    # 处理POST请求的数据
    form = SalespersonForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 数据有效，保存表单
        form.save()
        return redirect('/salesperson/list/')
    # 数据无效，重新渲染表单并显示错误信息
    return render(request, 'salesperson_form.html', {"form": form, "title": "编辑销售人员信息"})

def salesperson_delete(request, nid):
    """
    删除销售人员信息
    """
    # 根据ID删除对应的销售人员
    Salesperson.objects.filter(id=nid).delete()
    # 重定向回销售人员列表
    return redirect('/salesperson/list/')