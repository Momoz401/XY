import re
from datetime import datetime

from app01 import models

from django.core.exceptions import ValidationError


from app01.models import BaseInfoWorkType, BaseInfoWorkHour, ProductionWage, ExpenseAllocation, DepreciationAllocation, \
    LossReport, Salesperson, Vehicle, Market, Customer, OutboundRecord, SalesRecord, DailyPriceReport, MonthlyPlan, \
    BaseInfoBase, DailyPlan, Plant_batch, ProcessAlert, UserInfo, Channel
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from django import forms
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=2,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        label="手机号码",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            # 校验手机号是否为11位数字
            RegexValidator(r'^\d{11}$', '手机号必须是11位数字')
        ]
    )

    id_card = forms.CharField(
        label="身份证号码",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        validators=[
            # 校验身份证号码的格式
            RegexValidator(r'^\d{15}|\d{18}$', '身份证号码必须是15或18位数字')
        ]
    )

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "salary", "create_time", "gender", "depart", "phone", "bank_account", "id_card","bank_name"]



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
        fields = ['基地', '代号', '基地经理', '面积']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['代号']
        exists = models.BaseInfoBase.objects.filter(代号=txt_mobile).exists()
        if exists:
            raise ValidationError("代号")

        # 验证通过，用户输入的值返回
        return txt_mobile


class workHourModelForm(BootStrapModelForm):
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
                self.add_error('一级工种', '选择的二级分类无效')

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
        fields = ['工种ID', '一级工种', '二级工种', '单价', '单位', '备注', '一级分类', '一级工种', '默认计入成本']


class production_wage_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.ProductionWage
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工人', '批次', '一级分类', '一级工种', '二级工种', '工价', '合计工资', '工时', '地块']

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
        self.fields['一级工种'].choices = []

        self.fields['一级工种'].widget = forms.Select(attrs={'class': 'form-control'})
        # 设置日期字段为日期控件
        self.fields['日期'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['二级工种'].choices = []
        self.fields['二级工种'].widget = forms.Select(attrs={'class': 'form-control'})
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
                cleaned_data['工种'] = corresponding_object.二级工种
                cleaned_data['一级分类'] = corresponding_object.一级分类
                cleaned_data['二级分类'] = corresponding_object.一级工种
                # print(cleaned_data)
        return cleaned_data


class production_wage_Edit_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.ProductionWage
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期', '工人', '批次', '一级分类', '一级工种', '二级工种', '工价', '数量','合计工资', '工时', '地块', ]


class agriculture_cost_ModelForm(BootStrapModelForm):
    class Meta:
        model = models.Agriculture_cost
        # fields = "__all__"
        # exclude = ['level']
        fields = ['日期',  '农资种类', '名称', '单价', '数量', '金额', '批次', '地块']

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
        fields = ['日期',  '数量', '农资种类', '名称', '单价', '金额', '批次', '地块']


# 新增时只显示部分字段
class PlantBatchCreateForm(BootStrapModelForm):
    class Meta:
        model = Plant_batch
        fields = [
            '批次ID', '种植日期', '基地', '基地经理', '地块', '面积', '二级分类', '栽种方式',
            '移栽板量', '移栽数量', '点籽日期', '用籽量', '生长周期', '采收期',
            '备注', '采收初期', '采收末期', '正常产量', '正常亩产'
        ]


# 编辑时显示所有字段
class PlantBatchEditForm(BootStrapModelForm):
    class Meta:
        model = Plant_batch
        fields = '__all__'  # 显示所有字段


from django import forms
from django.forms import modelformset_factory


class WorkHourModelForm(BootStrapModelForm):
    class Meta:
        model = BaseInfoWorkHour
        fields = ['工种ID', '一级工种', '二级工种', '单价', '单位', '备注', '一级分类', '一级工种', '默认计入成本']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        level_one_choices = BaseInfoWorkType.objects.filter(工种级别=1).values_list('分类名称', '分类名称')
        choices = list(level_one_choices)
        self.fields['一级分类'].choices = choices
        self.fields['一级分类'] = forms.ChoiceField(
            choices=choices, required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['一级工种'].choices = []
        self.fields['一级工种'].widget = forms.Select(attrs={'class': 'form-control'})


WorkHourFormSet = modelformset_factory(BaseInfoWorkHour, form=WorkHourModelForm, extra=1)


class FixedFieldsForm(BootStrapModelForm):  # 静态字段
    try:
        from app01.models import BaseInfoBase
        choices = [('', '请选择基地经理')] + [(manager, manager) for manager in
                                              BaseInfoBase.objects.values_list('基地经理', flat=True).distinct()]
       # print("选择项 (choices):", choices)  # 打印生成的选择项列表

    except Exception:
        choices = [('', '请选择基地经理')]

    负责人 = forms.ChoiceField(
        choices=choices,
        required=True,
        label="基地经理"
    )

    class Meta:
        model = ProductionWage
        fields = ['日期', '工人', '负责人']


class DynamicFieldsForm(BootStrapModelForm):
    class Meta:
        model = ProductionWage
        fields = ['基地', '批次', '二级分类', '一级工种', '二级工种', '工价', '数量', '合计工资', '工时', '地块',
                  '备注']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 配置其他字段
        level_one_choices = BaseInfoWorkType.objects.filter(分类级别=1).values_list('工种ID', '分类名称')
        choices = list(level_one_choices)

        self.fields['一级工种'].choices = []
        self.fields['一级工种'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['二级工种'].choices = []
        self.fields['二级工种'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['数量'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['工时'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['合计工资'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['基地'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['批次'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'onchange': 'updateSecondCategory(this)'})
        self.fields['地块'].choices = []
        self.fields['地块'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['备注'].widget = forms.TextInput(attrs={'class': 'form-control'})

        # 将二级分类字段设为只读，因为它会自动填充
        self.fields['二级分类'].widget.attrs['readonly'] = True
        self.fields['工价'].widget = forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        selected_batch = cleaned_data.get('批次')

        # 自动从批次填充二级分类
        if selected_batch:
            try:
                # 假设批次以 "-" 分隔并且最后一个部分为二级分类
                second_category = selected_batch.split('-')[-1]
                cleaned_data['二级分类'] = second_category
            except IndexError:
                self.add_error('批次', '批次格式不正确，无法提取二级分类')

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

    def clean_身份证号码(self):
        """
        自定义身份证号码验证，检查是否为18位数字。
        """
        身份证号码 = self.cleaned_data.get('身份证号码')

        # 如果提供了身份证号码，进行格式验证
        if 身份证号码:
            if len(身份证号码) != 18 or not 身份证号码.isdigit():
                raise forms.ValidationError("身份证号码必须是18位数字。")

        return 身份证号码

    def clean_电话(self):
        """
        自定义手机号码验证，检查是否为11位数字。
        """
        电话 = self.cleaned_data.get('电话')

        # 如果提供了手机号码，进行格式验证
        if 电话:
            if not re.match(r'^\d{11}$', 电话):
                raise forms.ValidationError("请输入有效的11位手机号码。")

        return 电话


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
        fields = [
            '日期',
            '车牌',
            '公司',
            '市场',
            '规格',
            '单位',
            '数量_筐',
            '重量_kg',
            '批次',
            '地块',
            '盖布_块',
            '挑菜',
            '备注',

        ]
        widgets = {
            '地块': forms.Select(attrs={'class': 'form-control plot-select'}),
            '车牌': forms.Select(attrs={'class': 'form-control vehicle-select'}),
            '市场': forms.Select(attrs={'class': 'form-control market-select'}),
            '单位': forms.Select(attrs={'class': 'form-control unit-select'}),
            '批次': forms.TextInput(attrs={'class': 'form-control batch-autocomplete'}),

        }


class OutboundRecordEditForm(BootStrapModelForm):
    class Meta:
        model = OutboundRecord
        fields = [
            '日期',
            '车牌',
            '公司',
            '市场',
            '规格',
            '单位',
            '数量_筐',
            '重量_kg',
            '批次',
            '地块',
            '盖布_块',
            '挑菜',
            '备注',

        ]




class SalesRecordForm(BootStrapModelForm):
    # 在模型中 “销售人员” 只是 CharField
    # 在表单中，用 ChoiceField 并在 __init__ 中动态填充
    销售人员 = forms.ChoiceField(label="销售人员", choices=[], required=False)

    class Meta:
        model = SalesRecord  # 你的销售记录模型
        fields = [
            '客户',
            '数量',
            '单价',
            '金额',
            '应收金额',
            '实收金额',
            '收款日期',
            '销售人员',   # <-- 这里与模型字段名一致
            '单位',
            '规格',
            '收款方式',
            '备注'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1) 从 Salesperson 表中获取所有销售人员姓名
        salesperson_list = Salesperson.objects.values_list('姓名', flat=True)

        # 2) 构造 choices => [("", "请选择销售人员"), ("张三","张三"), ...]
        choices = [("", "请选择销售人员")] + [(name, name) for name in salesperson_list]
        self.fields['销售人员'].choices = choices

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
        fields = ['日期', '品种', '市场', '价格','价格上限']


class MonthlyPlanForm(BootStrapModelForm):
    class Meta:
        model = MonthlyPlan
        fields = [
            '日期', '二级分类', '面积', '周期', '每天种植单位亩', '每天产量单位吨',
            '五天种植单位亩', '盘数', '每天数量单位框', '备注'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置必填字段
        self.fields['日期'].required = True
        self.fields['二级分类'].required = True
        self.fields['面积'].required = True
        self.fields['周期'].required = True
        self.fields['每天种植单位亩'].required = True
        self.fields['每天产量单位吨'].required = True
        self.fields['五天种植单位亩'].required = True
        self.fields['盘数'].required = True
        self.fields['每天数量单位框'].required = True

        # 你可以为某些字段添加自定义标签或帮助文本
        self.fields['备注'].widget.attrs['placeholder'] = '请输入备注...'

    def clean(self):
        cleaned_data = super().clean()


class DailyPlanForm(BootStrapModelForm):
    """
    日计划表单，用于创建和编辑日计划信息，并包含自定义的验证逻辑。
    """

    class Meta:
        model = DailyPlan
        fields = ['业主', '地块', '面积', '上批批次', '下批种植日期', '播种方式', '备注']
        widgets = {
            '种植日期': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            '下批种植日期': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # 确保下批种植日期使用日期选择器
        }

    # 添加非空验证
    def clean_业主(self):
        业主 = self.cleaned_data.get('业主')
        if not 业主:
            raise forms.ValidationError("业主不能为空")
        return 业主

    def clean_地块(self):
        地块 = self.cleaned_data.get('地块')
        if not 地块:
            raise forms.ValidationError("地块不能为空")
        return 地块

    def clean_面积(self):
        面积 = self.cleaned_data.get('面积')
        if not 面积:
            raise forms.ValidationError("面积不能为空")
        return 面积

    def clean_种植日期(self):
        种植日期 = self.cleaned_data.get('种植日期')
        if not 种植日期:
            raise forms.ValidationError("种植日期不能为空")
        return 种植日期

    def clean_上批批次(self):
        上批批次 = self.cleaned_data.get('上批批次')
        if not 上批批次:
            raise forms.ValidationError("上批批次不能为空")
        return 上批批次

    def clean_下批种植日期(self):
        下批种植日期 = self.cleaned_data.get('下批种植日期')
        if not 下批种植日期:
            raise forms.ValidationError("下批种植日期不能为空")
        return 下批种植日期

    def clean_播种方式(self):
        播种方式 = self.cleaned_data.get('播种方式')
        if not 播种方式:
            raise forms.ValidationError("播种方式不能为空")
        return 播种方式



    def clean_批次ID(self):
        """
        自定义批次ID验证，确保其唯一性和正确格式。
        """
        批次ID = self.cleaned_data.get('批次ID')
        if 批次ID:
            # 这里可以添加更多的格式验证规则
            if not re.match(r'^[A-Za-z0-9\-]+$', 批次ID):
                raise forms.ValidationError("批次ID只能包含字母、数字和连字符。")
        return 批次ID

class ProcessAlertForm(BootStrapModelForm):
    class Meta:
        model = ProcessAlert
        fields = ['一级分类', '二级分类', '一级工种', '二级工种', '最小时间', '最大时间']

class UpUserForm(forms.Form):
    excel_file = forms.FileField(label="上传 Excel 文件")


class ChannelForm(BootStrapModelForm):
    class Meta:
        model = Channel
        fields = ["渠道名称", "地区", "联系人"]