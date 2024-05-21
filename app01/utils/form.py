from django.forms import CharField
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

from app01.models import BaseInfoWorkType
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]


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


class worktypeModelForm(BootStrapModelForm):
    class Meta:
        model = models.BaseInfoWorkType
        fields = ['工种名称', '父工种', '工种级别']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有工种级别为1的工种，构建成选择框的选项
        level_one_choices = BaseInfoWorkType.objects.filter(工种级别=1).values_list('工种ID', '工种名称')
        # 添加一个空的选项，表示可以为空
        choices = [('', '------------------------------------------------------')] + list(level_one_choices)
        self.fields['父工种'].choices = choices
        # 重新设置字段
        self.fields['父工种'] = forms.ChoiceField(choices=choices, required=False)

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
        fields = ['基地ID', '基地位置', '基地名称', '基地经理']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['基地名称']
        exists = models.BaseInfo.objects.filter(工种名称=txt_mobile).exists()
        if exists:
            raise ValidationError("基地已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class workHourModelForm(BootStrapModelForm):
    class Meta:
        model = models.BaseInfoWorkHour
        # fields = "__all__"
        # exclude = ['level']
        fields = ['工种ID', '工种', '分类', '单价', '单位', '备注']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['分类']

        exists = models.BaseInfoWorkHour.objects.filter(工种名称=txt_mobile).exists()
        if exists:
            raise ValidationError("分类已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile
