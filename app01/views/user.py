
from django.db.models import Q
from django.shortcuts import render, redirect
from app01 import models
from app01.models import UserInfo
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    """
    用户管理列表视图
    处理用户查询和分页显示
    """
    query = request.GET.get('q', '')  # 获取查询字符串
    queryset = UserInfo.objects.all()

    if query:
        # 根据姓名或手机号码进行过滤查询
        queryset = queryset.filter(Q(name__icontains=query) | Q(phone__icontains=query))

    # 使用自定义的Pagination工具类进行分页
    page_object = Pagination(request, queryset, page_size=20)

    context = {
        "search_data": page_object,
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 页码HTML字符串
    }
    return render(request, 'user_list.html', context)



def user_model_form_add(request):
    """
    添加用户视图（使用ModelForm）
    通过ModelForm实现数据验证和保存
    """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 处理POST请求的表单验证和保存
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()  # 如果验证成功，保存数据
        return redirect('/user/list/')

    # 如果验证失败，重新返回表单页面并显示错误信息
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """
    编辑用户视图
    通过ModelForm实现数据回填和保存
    """
    row_object = models.UserInfo.objects.filter(id=nid).first()  # 获取用户实例

    if request.method == "GET":
        form = UserModelForm(instance=row_object)  # 将实例传递给ModelForm用于回填
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)  # 绑定提交的数据
    if form.is_valid():
        form.save()  # 保存更新后的数据
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """
    删除用户视图
    根据用户ID删除对应的记录
    """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')