import os

from babel.dates import parse_date
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
import pandas as pd
import openpyxl
from app01.utils.database import data_to_db
from app01.utils.form import OutboundUploadForm, SalesRecordUploadForm
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01.models import BaseInfoWorkHour, ProductionWage, Agriculture_cost, Plant_batch, ExpenseAllocation, \
    OutboundRecord, Vehicle, Market, SalesRecord, JobCategoryInfo, JobTypeDetailInfo
from app01.utils.bootstrap import BootStrapModelForm
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
class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")
def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title,'uploader_name': request.session["info"]['name']})

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
    return render(request, 'upload_form.html', {"form": form, "title": title,'uploader_name': request.session["info"]['name']})


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
        # 获取上传人信息
        uploader_name = form.cleaned_data.get('update_user', '')
        # 保存上传文件到服务器
        uploaded_file = form.cleaned_data['excel_file']
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)  # 如果目录不存在，则创建
        file_path = os.path.join(upload_dir, uploaded_file.name)

        with open(file_path, mode='wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # 保存上传日志到数据库
        uploader_obj = models.uploader.objects.create(
            update_user=uploader_name,
            excel_file=file_path.replace(settings.MEDIA_ROOT, ''),  # 存储相对路径
        )

        # 读取上传的 Excel 文件
        df = pd.read_excel(file_path)
        records = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表

        for record in records:
            # 获取或创建相关的一级分类和二级分类对象
            一级分类_obj = JobCategoryInfo.objects.filter(category_name=record['一级分类'], category_level=1).first()
            if not 一级分类_obj:
                continue  # 如果没有找到对应的一级分类，跳过该记录

            二级分类_obj = None
            if '二级分类' in record and record['二级分类']:
                二级分类_obj = JobCategoryInfo.objects.filter(category_name=record['二级分类'], category_level=2).first()
                if not 二级分类_obj:
                    continue  # 如果没有找到对应的二级分类，跳过该记录

            # 获取或创建相关的一级工种和二级工种对象
            一级工种_obj = JobTypeDetailInfo.objects.filter(job_name=record['一级工种'], job_level=1).first()
            if not 一级工种_obj:
                continue  # 如果没有找到对应的一级工种，跳过该记录

            二级工种_obj = None
            if '二级工种' in record and record['二级工种']:
                二级工种_obj = JobTypeDetailInfo.objects.filter(job_name=record['二级工种'], job_level=2).first()
                if not 二级工种_obj:
                    continue  # 如果没有找到对应的二级工种，跳过该记录

            # 更新或创建 BaseInfoWorkHour 对象
            obj, created = BaseInfoWorkHour.objects.update_or_create(
                二级分类=二级分类_obj,
                一级工种=一级工种_obj,
                二级工种=二级工种_obj,
                defaults={
                    '一级分类': 一级分类_obj,
                    '单位': record['单位'],
                    '单价': record['单价'],
                    '备注': record['备注'],
                    '默认计入成本': record['默认计入成本'],
                    '最后更新时间': uploader_obj.update_date,
                    '上传人': uploader_name,
                }
            )

        return redirect('/WorkHour/list/')

    return render(request, 'upload_form.html', {"form": form, 'title': title})
def upload_productionwate_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "批量上传工价文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html',
                      {"form": form, 'title': title, 'uploader_name': request.session["info"]['name']})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        df = pd.read_excel(form.cleaned_data['excel_file'])

        # 对于 DecimalField 类型字段进行清洗
        decimal_fields = ['工价', '数量', '工时', '累计工时', '合计工资']  # 你需要确保这些字段名正确
        for field in decimal_fields:
            df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0)  # 将无法转换为数字的值转换为NaN，然后用0填充

        records = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表
        for record in records:
            obj, created = ProductionWage.objects.update_or_create(
                基地=record['基地'],
                工人=record['工人'],
                日期=record['日期'],
                负责人=record['基地经理'],
                一级分类=record['一级分类'],
                二级分类=record['二级分类'],
                工种=record['工种'],
                defaults={  # 使用 defaults 来简化 update_or_create 的使用
                    '工价': record['工价'],
                    '数量': record['数量'],
                    '工时': record['工时'],
                    '累计工时': record['累计工时'],
                    '合计工资': record['合计工资'],
                    '批次': record['批次'],
                    '地块': record['地块'],
                    '备注': record['备注'],
                }
            )
        return redirect('/production_wage_list/list/')
    return render(request, 'upload_form.html',
                  {"form": form, 'title': title, 'uploader_name': request.session["info"]['name']})


def upload_depreciation_excel(request):
    """ 上传折旧摊销表 """
    title = "折旧摊销表文件上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {
            "form": form,
            'title': title,
            'uploader_name': request.session["info"]['name']
        })

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        file = form.cleaned_data['excel_file']
        file_name = file.name

        # 保存文件到指定目录
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # 读取并处理Excel文件 (这里你可以根据需求进一步处理文件)
        try:
            df = pd.read_excel(file_path)
            # 此处可以根据df进行进一步的数据处理或存入数据库操作
            # 例如：处理 df 数据，将其写入到数据库中的其他表中
        except Exception as e:
            return HttpResponse(f"文件处理失败: {e}")

        return HttpResponse(f"文件 {file_name} 上传成功，并保存在 {file_path}")

    return render(request, 'upload_form.html', {
        "form": form,
        'title': title,
        'uploader_name': request.session["info"]['name']
    })


def upload_agriculturecost_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "批量农资成本文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title,'uploader_name': request.session["info"]['name']})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        # print(form.cleaned_data)
        df = pd.read_excel(form.cleaned_data['excel_file'])
        # print(df)
        # data_to_db(df, 'tpx_hxb_province')
        records = df.to_dict(orient='records')  # 将 DataFrame 转换为字典列表
        for record in records:
            obj, created = Agriculture_cost.objects.update_or_create(
                日期=record['日期'],
                工种=record['工种'],
                数量=record['数量'],
                农资种类=record['农资种类'],
                名称=record['名称'],
                单价=record['单价'],
                金额=record['金额'],
                批次=record['批次'],
                地块=record['地块'],

            )
        return redirect('/Agricureture/list/')
    return render(request, 'upload_form.html', {"form": form, 'title': title,'uploader_name': request.session["info"]['name']})

def upload_Plant_batch_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "批次表文件上传"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title, 'uploader_name': request.session["info"]['name']})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        try:
            # 读取 Excel 文件
            df = pd.read_excel(form.cleaned_data['excel_file'])

            # 检查必要的列是否存在
            required_columns = ['批次ID', '移栽日期', '点籽日期', '面积', '移栽板量', '移栽数量']
            for column in required_columns:
                if column not in df.columns:
                    raise ValueError(f"缺少必要的列：{column}")

            # 转换日期列为字符串格式
            date_columns = ['移栽日期', '点籽日期', '采收初期', '采收末期', '下批前一天时间']
            for column in date_columns:
                df[column] = df[column].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else None)

            # 处理 NaN 值的列，比如面积
            df['面积'] = df['面积'].fillna(0)

            # 将 DataFrame 转换为字典列表
            records = df.to_dict(orient='records')

            for record in records:
                try:
                    data = {
                        '一级分类': record.get('一级分类'),
                        '二级分类': record.get('二级分类'),
                        '地块': record.get('地块'),
                        '面积': record.get('面积', 0),
                        '基地经理': record.get('基地经理'),
                        '移栽日期': record.get('移栽日期'),
                        '移栽板量': record.get('移栽板量', 0),
                        '移栽数量': record.get('移栽数量', 0),
                        '点籽日期': record.get('点籽日期'),
                        '用籽量': record.get('用籽量', 0),
                        '备注': record.get('备注'),
                        '生长周期': record.get('生长周期'),
                        '采收初期': record.get('采收初期'),
                        '采收末期': record.get('采收末期'),
                        '采收期': record.get('采收期'),
                        '周期批次': record.get('周期批次'),
                        '总周期天数': record.get('总周期天数'),
                        '销毁面积': record.get('销毁面积', 0),
                        '销毁备注': record.get('销毁备注'),
                        '总产量': record.get('总产量', 0),
                        '总亩产': record.get('总亩产', 0),
                        '正常产量': record.get('正常产量', 0),
                        '正常亩产': record.get('正常亩产', 0),
                        '栽种方式': record.get('栽种方式'),
                        '下批前一天时间': record.get('下批前一天时间'),
                        '周期': record.get('周期'),
                        'uploader': request.session["info"]['name'],
                    }

                    # 单独尝试每一个字段，捕捉并记录出错的字段
                    for key, value in data.items():
                        try:
                            if key in ['移栽日期', '点籽日期', '采收初期', '采收末期', '下批前一天时间'] and value:
                                # 尝试将日期字符串转换为日期对象以确保格式正确
                                value = pd.to_datetime(value).strftime('%Y-%m-%d')
                            obj, created = Plant_batch.objects.update_or_create(
                                批次ID=record['批次ID'],
                                defaults={key: value}
                            )
                        except Exception as field_error:
                            print(f"处理字段 '{key}' 的值 '{value}' 时出错: {field_error}")
                            raise  # 重新抛出异常以便在外层捕获

                except Exception as e:
                    print(f"在处理记录时发生错误，字段 {record} 报错: {e}")
            return redirect('/Plant_batch/list/')
        except Exception as e:
            print(f"处理过程中出现错误：{e}")
            form.add_error(None, "上传过程中出现问题，请检查数据格式并重试。")
    return render(request, 'Plant_batch.html', {"form": form, 'title': title, 'uploader_name': request.session["info"]['name']})


def upload_expense_allocation(request):
    """ 上传费用摊销数据 """
    if request.method == "GET":
        return render(request, 'upload_expense_allocation.html')

    file_object = request.FILES.get("excel_file")
    df = pd.read_excel(file_object)
    df = df.fillna(0)  # 填充空值
    records = df.to_dict(orient='records')

    for record in records:
        ExpenseAllocation.objects.update_or_create(
            批次=record['批次'],  # 假设批次是唯一标识
            defaults={
                '生活费': record['生活费'],
                '水电费': record['水电费'],
                '服务费': record['服务费'],
                '其他费用': record['其他费用'],
                '燃油费': record['燃油费'],
                '维修费': record['维修费'],
                '销售费': record['销售费'],
                '基地经理': record['基地经理'],
                '散工工时': record['散工工时'],
                '浇水打杂费用': record['浇水打杂费用'],
                '材料费': record['材料费'],
                '管理费1': record['管理费1'],
                '报销费用': record['报销费用'],
                '地租': record['地租'],
                '大棚折旧': record['大棚折旧'],
                '其他资产': record['其他资产'],
                '农家肥': record['农家肥'],
                '有机肥': record['有机肥'],
                '草莓土': record['草莓土'],
                '出勤奖': record['出勤奖'],
                '服务费': record['服务费'],
                '地租大棚摊销': record['地租大棚摊销'],
            }
        )

    return redirect('/expense_allocation/list/')

def outbound_upload(request):
    """上传出库记录"""
    if request.method == "GET":
        form = OutboundUploadForm()
        return render(request, 'upload_outbound_from.html', {"form": form, "title": "上传出库记录"})

    form = OutboundUploadForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        df = pd.read_excel(form.cleaned_data['excel_file'])

        # 处理NaN值，将其替换为0或其他合适的默认值
        df = df.fillna({
            '运送数量': 0,
            '数量_筐': 0,
            '重量_kg': 0,
            '盖布_块': 0,
            '备注': '',
            '挑菜': '',
            '客户': ''
        })

        records = df.to_dict(orient='records')

        for record in records:
            OutboundRecord.objects.update_or_create(
                批次=record['批次'],
                defaults={
                    '日期': record['日期'],
                    '运送数量': record['运送数量'],
                    '车牌': record['车牌'],  # 直接保存车牌号
                    '公司': record['公司'],
                    '市场': record['市场'],  # 直接保存市场名称
                    '品类': record['品类'],
                    '品种': record['品种'],
                    '规格': record['规格'],
                    '单位': record['单位'],
                    '数量_筐': record['数量_筐'],
                    '重量_kg': record['重量_kg'],
                    '地块': record['地块'],
                    '盖布_块': record['盖布_块'],
                    '备注': record['备注'],
                    '挑菜': record['挑菜'],
                    '客户': record['客户'],
                }
            )

        # 成功上传后跳转到列表页
        return redirect('/outbound/list/')
    return render(request, 'upload_outbound_from.html', {"form": form, "title": "上传出库记录"})


def upload_sales_record(request):
    if request.method == "POST":
        form = SalesRecordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 读取上传的Excel文件
            excel_file = form.cleaned_data['excel_file']
            df = pd.read_excel(excel_file)

            # 遍历每一行数据并创建或更新 SalesRecord 对象
            for _, row in df.iterrows():
                # 根据批次号查找出库记录
                outbound_record = OutboundRecord.objects.filter(批次=row['批次']).first()
                if outbound_record:
                    # 处理日期字段
                    sales_date = None
                    payment_date = None

                    try:
                        if pd.notna(row['销售日期']):
                            sales_date = parse_date(str(row['销售日期']))
                    except Exception as e:
                        print(f"销售日期解析错误: {e}")

                    try:
                        if pd.notna(row['收款日期']):
                            payment_date = parse_date(str(row['收款日期']))
                    except Exception as e:
                        print(f"收款日期解析错误: {e}")

                    # 创建或更新销售记录
                    SalesRecord.objects.update_or_create(
                        出库记录=outbound_record,
                        批次=row['批次'],  # 根据批次号查找
                        defaults={
                            '销售日期': sales_date,
                            '客户': row['客户'],
                            '数量': row['数量'],
                            '单价': row['单价'],
                            '金额': row['金额'],
                            '应收金额': row['应收金额'],
                            '实收金额': row['实收金额'],
                            '备注': row['备注'],
                            '收款日期': payment_date,
                            '销售人员': row['销售人员'],
                            '单位': row['单位'],
                            '规格': row['规格'],
                            '收款方式': row['收款方式'],
                        }
                    )
                else:
                    # 处理找不到对应出库记录的情况，可以记录错误或跳过
                    print(f"找不到批次号为 {row['批次']} 的出库记录")

                    # 成功后重定向到出库记录列表页面
                return redirect('outbound_list')
    else:
        form = SalesRecordUploadForm()

    return render(request, 'upload_sales_record.html', {'form': form})