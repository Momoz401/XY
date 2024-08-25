from django.shortcuts import render, redirect
from app01 import models
from app01.models import ProductionWage
from app01.utils.encrypt import md5
from app01.utils.form import MobileLoginForm, FixedFieldsForm, DynamicFieldsFormSet


def mobile_login(request):
    """ 手机端登录 """
    if request.method == "GET":
        form = MobileLoginForm()
        return render(request, 'mobile/mobile_login.html', {'form': form})

    form = MobileLoginForm(data=request.POST)
    print(form)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = request.POST.get('password')  # 直接获取POST提交的明文密码




        # 使用加密后的密码进行数据库查询
        admin_object = models.UserInfo.objects.filter(
            name=username,
            password=password
        ).first()

        # 调试信息：查看查询到的对象
        print(f"查询到的用户对象: {admin_object}")

        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'mobile/mobile_login.html', {'form': form})

        # 登录成功后，保存 session 信息
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.name}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录

        # 成功登录后跳转到手机端的主页或其他页面
        """ 手机端主页，根据部门加载不同模板 """
        user_info = request.session.get('info')
        if not user_info:
            return redirect('/mobile/login/')  # 如果未登录，重定向到登录页面

        # 获取用户的详细信息
        user = models.UserInfo.objects.get(id=user_info['id'])
        department = user.depart.title  # 获取部门名称

        # 根据部门加载不同的模板
        if department == "统计部":
            return render(request, 'mobile/statistics_template.html', {'user': user})
        elif department == "市场部":
            return render(request, 'mobile/market_template.html', {'user': user})
        else:
            # 如果部门不属于已定义的部门，则加载一个默认的模板
            return render(request, 'mobile/default_template.html', {'user': user})

    return render(request, 'mobile/mobile_login.html', {'form': form})
def mobile_home(request):
    """ 手机端主页 """
    if not request.session.get('info'):
        return redirect('/mobile_login/')  # 如果用户未登录，则重定向到登录页面

    return render(request, 'mobile/statistics_template.html')


def mobile_logout(request):
    """ 手机端退出登录 """
    request.session.clear()
    return redirect('/mobile/login/')  # 退出后跳转回手机登录页面


def mobile_gongshiluru(request):
    if request.method == 'POST':
        fixed_form = FixedFieldsForm(request.POST)
        formset = DynamicFieldsFormSet(request.POST)

        if fixed_form.is_valid() and formset.is_valid():
            fixed_instance = fixed_form.save(commit=False)
            instances = formset.save(commit=False)
            for instance in instances:
                instance.日期 = fixed_instance.日期
                instance.工人 = fixed_instance.工人
                instance.负责人 = fixed_instance.负责人
                instance.save()
            formset.save_m2m()
            return redirect('/mobile/home/')  # 手机端重定向到手机主页

    else:
        fixed_form = FixedFieldsForm()
        formset = DynamicFieldsFormSet(queryset=ProductionWage.objects.none())

    return render(request, 'mobile/mobile_gongshiluru.html', {'fixed_form': fixed_form, 'formset': formset})