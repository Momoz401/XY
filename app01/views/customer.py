from django.shortcuts import render, redirect, get_object_or_404
from app01.models import Customer
from app01.utils.form import CustomerForm
from app01.utils.pagination import Pagination

def customer_list(request):
    """
    客户信息列表视图，用于展示客户信息，并支持通过客户名称进行模糊搜索。
    """
    data_dict = {}

    # 获取搜索数据
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["客户名称__icontains"] = search_data  # 如果有搜索关键词，则根据客户名称进行过滤

    # 获取客户数据，按照ID降序排序
    queryset = Customer.objects.filter(**data_dict).order_by("-id")

    # 使用自定义分页工具进行分页
    page_object = Pagination(request, queryset)

    # 渲染模板并传递分页后的数据
    context = {
        "search_data": search_data,  # 搜索关键词，用于回显
        "queryset": page_object.page_queryset,  # 分页后的客户数据
        "page_string": page_object.html()  # 页码HTML
    }
    return render(request, 'customer_list.html', context)

def customer_add(request):
    """
    添加客户信息视图，显示客户表单并处理表单提交。
    """
    if request.method == "GET":
        # GET请求时，返回一个空的表单用于添加客户
        form = CustomerForm()
        return render(request, 'customer_form.html', {"form": form, "title": "新建客户信息"})

    # 处理POST请求，保存表单数据
    form = CustomerForm(data=request.POST)
    if form.is_valid():
        form.save()  # 表单验证通过后保存数据
        return redirect('/customer/list/')  # 跳转到客户信息列表页面

    # 如果表单无效，重新渲染页面并显示错误信息
    return render(request, 'customer_form.html', {"form": form, "title": "新建客户信息"})

def customer_edit(request, nid):
    """
    编辑客户信息视图，根据客户ID加载客户信息并展示在表单中。
    """
    # 获取要编辑的客户对象，如果找不到则返回404页面
    row_object = get_object_or_404(Customer, id=nid)

    if request.method == "GET":
        # GET请求时，加载现有客户数据到表单
        form = CustomerForm(instance=row_object)
        return render(request, 'customer_form.html', {"form": form, "title": "编辑客户信息"})

    # 处理POST请求，更新客户数据
    form = CustomerForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()  # 表单验证通过后保存修改的数据
        return redirect('/customer/list/')  # 跳转到客户信息列表页面

    # 如果表单无效，重新渲染页面并显示错误信息
    return render(request, 'customer_form.html', {"form": form, "title": "编辑客户信息"})

def customer_delete(request, nid):
    """
    删除客户信息视图，根据客户ID删除客户记录。
    """
    # 删除指定ID的客户记录
    Customer.objects.filter(id=nid).delete()
    # 删除成功后，跳转到客户列表页面
    return redirect('/customer/list/')