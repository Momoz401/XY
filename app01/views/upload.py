import os
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import pandas as pd
import openpyxl

from app01.utils.database import data_to_db


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # # 'username': ['big666']
    # print(request.POST)  # 请求体中数据
    # # {'avatar': [<InMemoryUploadedFile: 图片 1.png (image/png)>]}>
    # print(request.FILES)  # 请求发过来的文件 {}

    file_object = request.FILES.get("avatar")
    # print(file_object.name)  # 文件名：WX20211117-222041@2x.png

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("...")


from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01.models import BaseInfoWorkHour, ProductionWage


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # {'name': '武沛齐', 'age': 123, 'img': <InMemoryUploadedFile: 图片 1.png (image/png)>}
        # 1.读取图片内容，写入到文件夹中并获取文件的路径。
        image_object = form.cleaned_data.get("img")

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("...")
    return render(request, 'upload_form.html', {"form": form, "title": title})


from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.uploader
        fields = "__all__"


def upload_workhour_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "批量上传价格文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        # print(form.cleaned_data)
        df = pd.read_excel(form.cleaned_data['excel_file'])
        print(df)
        #data_to_db(df, 'tpx_hxb_province')
        records = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表
        for record in records:
            obj, created = BaseInfoWorkHour.objects.update_or_create(
                工人=record['工人'],
                一级分类=record['一级分类'],
                二级分类=record['二级分类'],
                单位=record['单位'],
                单价=record['单价'],
                备注=record['备注'],
                # 假设 'name' 是唯一标识相同记录的字段

            )
        return redirect('/WorkHour/list/')
    return render(request, 'upload_form.html', {"form": form, 'title': title})

def upload_productionwate_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "批量上传工价文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        # print(form.cleaned_data)
        df = pd.read_excel(form.cleaned_data['excel_file'])
        # print(df)
        #data_to_db(df, 'tpx_hxb_province')
        records = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表
        for record in records:
            obj, created = ProductionWage.objects.update_or_create(
                工人=record['工人'],
                一级分类=record['一级分类'],
                二级分类=record['二级分类'],
                工种=record['工种'],
                工价=record['工价'],
                工时=record['工时'],
                日期=record['日期'],
                批次=record['批次'],
                地块=record['地块'],

            )
        return redirect('/production_wage_list/list/')
    return render(request, 'upload_form.html', {"form": form, 'title': title})
