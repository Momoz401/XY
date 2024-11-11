from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.models import ProductionWage, JobCategoryInfo, JobTypeDetailInfo, BaseInfoBase, Vehicle, Customer, UserInfo, \
    PlanPlantBatch, Market, Plant_batch
from app01.utils.encrypt import md5
from app01.utils.form import MobileLoginForm, FixedFieldsForm, DynamicFieldsFormSet, OutboundRecordForm


def mobile_login(request):
    """ 手机端登录 """
    if request.method == "GET":
        form = MobileLoginForm()
        return render(request, 'mobile/mobile_login.html', {'form': form})

    form = MobileLoginForm(data=request.POST)
    # print(form)
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

                # 查询并转换基地的中文名称
                base_code = instance.基地
                if base_code:
                    try:
                        base_info = BaseInfoBase.objects.get(代号=base_code)
                        instance.基地 = base_info.基地  # 保存基地的中文名称
                    except BaseInfoBase.DoesNotExist:
                        print(f"基地代号 '{base_code}' 不存在")

                # 获取二级分类名称，并根据它查找对应的一级分类
                second_category_name = instance.二级分类
                try:
                    second_category_instance = JobCategoryInfo.objects.get(category_name=second_category_name,
                                                                           category_level=2)
                    if second_category_instance.parent_category:
                        instance.一级分类 = second_category_instance.parent_category.category_name
                    else:
                        print(f"二级分类 '{second_category_name}' 没有对应的一级分类")
                except JobCategoryInfo.DoesNotExist:
                    print(f"二级分类 '{second_category_name}' 不存在")

                # 查询并转换一级工种的中文名称
                primary_work_id = instance.一级工种
                if primary_work_id:
                    try:
                        primary_work_info = JobTypeDetailInfo.objects.get(id=primary_work_id)
                        instance.一级工种 = primary_work_info.job_name  # 保存一级工种的中文名称
                    except JobTypeDetailInfo.DoesNotExist:
                        print(f"一级工种 ID '{primary_work_id}' 不存在")

                # 查询并转换二级工种的中文名称
                secondary_work_id = instance.二级工种
                if secondary_work_id:
                    try:
                        secondary_work_info = JobTypeDetailInfo.objects.get(id=secondary_work_id)
                        instance.二级工种 = secondary_work_info.job_name  # 保存二级工种的中文名称
                    except JobTypeDetailInfo.DoesNotExist:
                        print(f"二级工种 ID '{secondary_work_id}' 不存在")

                instance.save()
            formset.save_m2m()
            return JsonResponse({'success': True, 'message': '录入成功，正在跳转到主页...'})

    else:
        fixed_form = FixedFieldsForm()
        formset = DynamicFieldsFormSet(queryset=ProductionWage.objects.none())

    return render(request, 'mobile/mobile_gongshiluru.html', {'fixed_form': fixed_form, 'formset': formset})


def mobile_outbound_add(request):
    if request.method == "POST":
        form = OutboundRecordForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            # 处理批次获取品类和品种
            batch = form.cleaned_data.get('批次')
            if batch:
                try:
                    batch_obj = Plant_batch.objects.get(批次ID=batch)
                    instance.品类 = batch_obj.一级分类  # 从批次对象获取一级分类并存储为品类
                    instance.品种 = batch_obj.二级分类  # 从批次对象获取二级分类并存储为品种
                    # print(f"批次 {batch} 的一级分类为: {batch_obj.一级分类}, 二级分类为: {batch_obj.二级分类}")
                except Plant_batch.DoesNotExist:
                    print(f"批次 {batch} 在 PlanPlantBatch 中不存在")

            # 打印实例信息用于调试
            print(f"即将保存的实例数据: {instance.__dict__}")

            try:
                instance.save()
                return JsonResponse({'success': True, 'message': '出库记录添加成功！'})
            except Exception as e:
                print(f"保存实例时出现错误: {e}")
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            print(f"表单验证失败: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = OutboundRecordForm()
        vehicles = Vehicle.objects.all()
        markets = Market.objects.all()
        categories = JobCategoryInfo.objects.all()
        return render(request, 'mobile/mobile_outbound_form.html', {
            'form': form,
            'title': '添加出库记录',
            'vehicles': vehicles,
            'markets': markets,
            'categories': categories
        })

def customer_autocomplete(request):
    term = request.GET.get('term', '')
    customers = Customer.objects.filter(客户名称__icontains=term)  # 替换为实际字段名
    customer_list = [{'label': customer.客户名称, 'value': customer.客户名称} for customer in customers]
    return JsonResponse(customer_list, safe=False)

def worker_autocomplete(request):
    term = request.GET.get('term', '')
    workers = UserInfo.objects.filter(name__icontains=term)  # 替换为实际字段名
    worker_list = [{'label': worker.name, 'value': worker.name} for worker in workers]
    return JsonResponse(worker_list, safe=False)

def batch_autocomplete(request):
    term = request.GET.get('term', '')
    batches = Plant_batch.objects.filter(批次ID__icontains=term)  # 替换为实际字段名
    batch_list = [{'label': batch.批次ID, 'value': batch.批次ID} for batch in batches]
    return JsonResponse(batch_list, safe=False)