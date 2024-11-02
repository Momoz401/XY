from datetime import datetime

from django.forms import CharField
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

from app01.models import BaseInfoWorkType, BaseInfoWorkHour, ProductionWage, ExpenseAllocation, DepreciationAllocation, \
    LossReport, Salesperson, Vehicle, Market, Customer, OutboundRecord, SalesRecord, DailyPriceReport, MonthlyPlan, \
    BaseInfoBase, DailyPlan
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=2,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "salary", "create_time", "gender", "depart", "phone", "bank_account"]


from django import forms
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5

class MobileLoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class PrettyModelForm(BootStrapModelForm):
    # 验证：方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["mobile", 'price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class work_type_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.BaseInfoWorkType
        fields = ['分类名称', '父分类', '分类级别']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有工种级别为1的工种，构建成选择框的选项
        level_one_choices = BaseInfoWorkType.objects.filter(分类级别=1).values_list('分类名称', '分类名称')
        # 添加一个空的选项，表示可以为空
        choices = [('', '')] + list(level_one_choices)
        self.fields['父分类'].choices = choices
        # 重新设置字段
        self.fields['父分类'] = forms.ChoiceField(choices=choices, required=False,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('工种级别')
        parent = cleaned_data.get('父工种')
        name = cleaned_data.get('工种名称')
        # 如果工种级别为1，但父工种字段不为空，则引发验证错误
        if level == 1 and parent != '':
            # print(parent+'111')
            raise forms.ValidationError("一级分类的父工种必须为空")
            # 如果工种级别为2，但父工种字段为空，则引发验证错误
        if level == 2 and not parent:
            raise forms.ValidationError("二级分类必须选择父工种")
        if BaseInfoWorkType.objects.filter(工种名称=name, 父工种=parent).exists():  # 存在父工种下面，同名的情况。
            raise forms.ValidationError("该工种名称在相同工种级别下已经存在，请使用其他名称")

        return cleaned_data


class baseInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.BaseInfoBase
        # fields = "__all__"
        # exclude = ['level']
        # exclude = ['level']
        fields = ['基地', '代号', '基地经理', '面积' ]

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['代号']
        exists = models.BaseInfoBase.objects.filter(代号=txt_mobile).exists()
        if exists:
            raise ValidationError("代号")

        # 验证通过，用户输入的值返回
        return txt_mobile


class workHourModelForm(forms.ModelForm):
    class Meta:
        model = BaseInfoWorkHour
        fields = ['工种ID', '一级分类', '二级分类', '一级工种', '二级工种', '单价', '单位', '备注', '默认计入成本']

    def clean(self):
        cleaned_data = super().clean()

        # 获取一级分类、二级分类、一级工种、二级工种的ID或实例
        一级分类 = cleaned_data.get('一级分类')
        二级分类 = cleaned_data.get('二级分类')
        一级工种 = cleaned_data.get('一级工种')
        二级工种 = cleaned_data.get('二级工种')

        # 如果一级分类不是实例，则将其转换为 JobCategoryInfo 实例
        if isinstance(一级分类, str) or isinstance(一级分类, int):
            try:
                cleaned_data['一级分类'] = JobCategoryInfo.objects.get(id=int(一级分类))
            except JobCategoryInfo.DoesNotExist:
                self.add_error('一级分类', '选择的一级分类无效')

        # 如果二级分类不是实例，则将其转换为 JobCategoryInfo 实例
        if isinstance(二级分类, str) or isinstance(二级分类, int):
            try:
                cleaned_data['二级分类'] = JobCategoryInfo.objects.get(id=int(二级分类))
            except JobCategoryInfo.DoesNotExist:
                self.add_error('二级分类', '选择的二级分类无效')

        # 如果一级工种不是实例，则将其转换为 JobTypeDetailInfo 实例
        if isinstance(一级工种, str) or isinstance(一级工种, int):
            try:
                cleaned_data['一级工种'] = JobTypeDetailInfo.objects.get(id=int(一级工种))
            except JobTypeDetailInfo.DoesNotExist:
                self.add_error('一级工种', '选择的一级工种无效')

        # 如果二级工种不是实例，则将其转换为 JobTypeDetailInfo 实例
        if isinstance(二级工种, str) or isinstance(二级工种, int):
            try:
                cleaned_data['二级工种'] = JobTypeDetailInfo.objects.get(id=int(二级工种))
            except JobTypeDetailInfo.DoesNotExist:
                self.add_error('二级工种', '选择的二级工种无效')

        return cleaned_data

class workHour_Edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.BaseInfoWorkHour
        # fields = "__all__"
        # exclude = ['level']
        fields =['工种ID', '一级工种', '二级工种', '单价', '单位', '备注', '一级分类', '二级分类', '默认计入成本']


class production_wage_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.ProductionWage
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工人', '批次', '一级分类', '二级分类', '工种', '工价', '合计工资', '工时', '地块']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有工种级别为1的工种，构建成选择框的选项
        level_one_choices = BaseInfoWorkType.objects.filter(工种级别=1).values_list('工种ID', '分类名称')

        # 添加一个空的选项，表示可以为空
        choices = list(level_one_choices)
        self.fields['一级分类'].choices = choices
        # 重新设置字段
        self.fields['一级分类'] = forms.ChoiceField(choices=choices, required=True,
                                                    widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['二级分类'].choices = []

        self.fields['二级分类'].widget = forms.Select(attrs={'class': 'form-control'})
        # 设置日期字段为日期控件
        self.fields['日期'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['工种'].choices = []
        self.fields['工种'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['工价'].widget = forms.Select(attrs={'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        selected_work_type = cleaned_data.get('工种')
        selected_base_id = cleaned_data.get('地块')
        # print(selected_work_type)
        # 获取工种选项的文本值
        if selected_work_type:
            corresponding_object = BaseInfoWorkHour.objects.filter(工种ID=selected_work_type).first()
            # print(corresponding_object.工种)

            if corresponding_object:
                # 保存选项的文本值
                cleaned_data['工种'] = corresponding_object.工种
                cleaned_data['一级分类'] = corresponding_object.一级分类
                cleaned_data['二级分类'] = corresponding_object.二级分类
                # print(cleaned_data)
        return cleaned_data


class production_wage_Edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.ProductionWage
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工人', '批次', '一级分类', '二级分类', '工种', '工价', '合计工资', '工时', '地块']


class agriculture_cost_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Agriculture_cost
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工种', '数量', '农资种类', '名称', '单价', '金额', '批次', '地块']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.now().date()
        self.fields['日期'].initial = today
        self.fields['日期'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })


class agriculture_cost_Edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Agriculture_cost
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工种', '数量', '农资种类', '名称', '单价', '金额', '批次', '地块']


class Plant_batch_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Plant_batch
        # fields = "__all__"
        # exclude = ['level']
        fields = ['批次ID', '二级分类', '一级分类', '地块', '面积', '基地经理', '移栽日期', '移栽板量', '移栽数量', '点籽日期',
                  '用籽量', '备注']


class Plant_batch_Edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Plant_batch
        # fields = "__all__"
        # exclude = ['level']
        fields = ['批次ID', '二级分类', '一级分类', '地块', '面积', '基地经理', '移栽日期', '移栽板量', '移栽数量', '点籽日期',
                  '用籽量', '备注']


from django import forms
from django.forms import modelformset_factory


class WorkHourModelForm(forms.ModelForm):
    class Meta:
        model = BaseInfoWorkHour
        fields = ['工种ID', '一级工种', '二级工种', '单价', '单位', '备注', '一级分类', '二级分类', '默认计入成本']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        level_one_choices = BaseInfoWorkType.objects.filter(工种级别=1).values_list('分类名称', '分类名称')
        choices = list(level_one_choices)
        self.fields['一级分类'].choices = choices
        self.fields['一级分类'] = forms.ChoiceField(
            choices=choices, required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['二级分类'].choices = []
        self.fields['二级分类'].widget = forms.Select(attrs={'class': 'form-control'})


WorkHourFormSet = modelformset_factory(BaseInfoWorkHour, form=WorkHourModelForm, extra=1)


class FixedFieldsForm(BootStrapModelForm):  # 静态字段
    class Meta:
        model = ProductionWage
        fields = ['日期', '工人', '负责人']


class DynamicFieldsForm(forms.ModelForm):
    class Meta:
        model = ProductionWage
        fields = ['基地', '批次', '一级分类', '二级分类', '工种', '工价', '数量', '合计工资', '工时', '地块','备注']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        level_one_choices = BaseInfoWorkType.objects.filter(分类级别=1).values_list('工种ID', '分类名称')
        choices = list(level_one_choices)
        self.fields['一级分类'].choices = choices
        self.fields['一级分类'] = forms.ChoiceField(
            choices=choices, required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['二级分类'].choices = []
        self.fields['二级分类'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['工种'].choices = []
        self.fields['工种'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['工价'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['数量'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['工时'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['合计工资'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['基地'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['批次'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['地块'].choices = []
        self.fields['地块'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['备注'].widget = forms.TextInput(attrs={'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        selected_work_type = cleaned_data.get('工价')
        print(selected_work_type)
        # 获取工种选项的文本值 ,这里非常重要
        if selected_work_type:
            corresponding_object = BaseInfoWorkHour.objects.filter(工种ID=selected_work_type).first()
            # print(corresponding_object.工种)

            if corresponding_object:
                # 保存选项的文本值
                cleaned_data['工种'] = corresponding_object.工种
                cleaned_data['一级分类'] = corresponding_object.一级分类
                cleaned_data['二级分类'] = corresponding_object.二级分类
                cleaned_data['工价'] = corresponding_object.单价
                # print(cleaned_data)
        return cleaned_data


from django.forms import modelformset_factory

DynamicFieldsFormSet = modelformset_factory(ProductionWage, form=DynamicFieldsForm, extra=1)

class ExpenseAllocationForm(BootStrapModelForm):
    月份 = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m'],
        label="月份"
    )

    class Meta:
        model = ExpenseAllocation
        fields = "__all__"



class DepreciationAllocationForm(BootStrapModelForm):
    月份 = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m'],
        label="月份"
    )

    class Meta:
        model = DepreciationAllocation
        fields = "__all__"


class LossReportForm(BootStrapModelForm):
    报损时间 = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="报损时间"
    )

    class Meta:
        model = LossReport
        fields = "__all__"



class SalespersonForm(BootStrapModelForm):
    class Meta:
        model = Salesperson
        fields = "__all__"


class VehicleForm(BootStrapModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"


class MarketForm(BootStrapModelForm):
    class Meta:
        model = Market
        fields = "__all__"

class CustomerForm(BootStrapModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class OutboundRecordForm(BootStrapModelForm):
    class Meta:
        model = OutboundRecord
        fields = "__all__"


class SalesRecordForm(BootStrapModelForm):
    class Meta:
        model = SalesRecord
        fields = [
            '客户',
            '数量',
            '单价',
            '金额',
            '应收金额',
            '实收金额',
            '收款日期',  # 新增字段
            '销售人员',  # 新增字段
            '单位',      # 新增字段
            '规格',      # 新增字段
            '收款方式',  # 新增字段
            '备注'
        ]
class ExpenseAllocationModelForm(forms.ModelForm):
    class Meta:
        model = ExpenseAllocation
        fields = "__all__"


class OutboundUploadForm(forms.Form):
    excel_file = forms.FileField(label="上传Excel文件")


class SalesRecordUploadForm(forms.Form):
    excel_file = forms.FileField(label="上传销售记录")


from app01.models import JobCategoryInfo, JobTypeDetailInfo

class JobCategoryInfoModelForm(BootStrapModelForm):
    class Meta:
        model = JobCategoryInfo
        fields = "__all__"

class JobTypeDetailInfoModelForm(BootStrapModelForm):
    class Meta:
        model = JobTypeDetailInfo
        fields = "__all__"


# forms.py

class DailyPriceReportForm(BootStrapModelForm):
    class Meta:
        model = DailyPriceReport
        fields = ['日期', '品种', '市场', '价格']

class MonthlyPlanForm(BootStrapModelForm):
    class Meta:
        model = MonthlyPlan
        fields = ['日期', '二级分类', '面积', '周期', '基地', '地块']


class DailyPlanForm(BootStrapModelForm):
    class Meta:
        model = DailyPlan
        fields = ['基地经理', '地块', '面积', '生长周期', '采收期', '备注']