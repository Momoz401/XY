import pandas as pd
from django.db.models import Q
from django.shortcuts import render, redirect
from app01 import models
from app01.models import UserInfo, Department
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, UpUserForm


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

    # 不再手动分页，因为 DataTables 会处理分页
    context = {
        "queryset": queryset,  # 原始数据会传递给 DataTables
        "query": query,
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


def upload_userinfo_modal_form(request):
    """ 上传员工信息并批量汇总数据 """
    title = "批量上传员工信息"

    if request.method == "GET":
        form = UpUserForm()
        download_text = f"点击下载 {title} 模板"
        template_path = 'files/员工信息导入模板.xlsx'  # 指定 Excel 文件路径
        return render(request, 'upload_form.html', {
            "form": form,
            'title': title,
            "download_text": download_text,
            "template_path": template_path
        })

    form = UpUserForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取上传的 Excel 文件
        uploaded_file = form.cleaned_data['excel_file']
        try:
            df = pd.read_excel(uploaded_file)
            print(f"读取的 Excel 数据:\n{df}")
        except Exception as e:
            print(f"读取 Excel 文件失败: {e}")
            return render(request, 'upload_form.html',
                          {"form": form, 'title': title, 'error': f"读取 Excel 文件失败: {e}"})

        # 将 DataFrame 转换为字典列表
        records = df.to_dict(orient='records')
        print(f"转换后的记录: {records}")
        gender_map = {
            '男': 1,
            '女': 2,
        }
        for record in records:
            try:

                # 转换性别字符串为数字
                gender_value = record.get('性别')
                gender_number = gender_map.get(gender_value)

                if gender_number is None:
                    print(f"性别字段值错误: {gender_value}, 跳过记录: {record}")
                    continue
                # 获取部门对象
                depart_name = record.get('所属部门')
                depart_obj = Department.objects.filter(title=depart_name).first()
                if not depart_obj:
                    print(f"未找到部门ID为 {depart_name} 的部门，跳过记录: {record}")
                    continue

                # 通过身份证号判断是更新还是创建
                user_obj, created = UserInfo.objects.update_or_create(
                    id_card=record['身份证号码'],
                    defaults={
                        'name': record['姓名'],
                        'password': record['密码'],
                        'age': record['年龄'],
                        'salary': record['工资'],
                        'create_time': record['入职日期'],
                        'depart': depart_obj,
                        'gender': gender_number,
                        'phone': record['手机号码'],
                        'bank_account': record['银行卡号'],
                        'bank_name': record['开户行信息'],
                    }
                )
                if created:
                    print(f"创建了新用户: {user_obj}")
                else:
                    print(f"更新了用户: {user_obj}")

            except Exception as e:
                print(f"处理记录时发生错误: {e}, 记录: {record}")

        return redirect('/user/list/')

    return render(request, 'upload_form.html', {"form": form, 'title': title})