from datetime import datetime, timedelta

from django.utils import timezone

from django.db import models


class XX(models.Model):
    title = models.CharField(verbose_name="名称", max_length=32)
    image = models.FileField(verbose_name="头像", upload_to="avatar/")


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="工资", max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    create_time = models.DateField(verbose_name="入职时间", null=True, blank=True)
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE, null=True,
                               blank=True)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)
    phone = models.CharField(verbose_name="手机号码", max_length=20, null=True, blank=True)
    bank_account = models.CharField(verbose_name="银行卡号", max_length=64, null=True, blank=True)
    id_card = models.CharField(verbose_name="身份证号码", max_length=18, null=True, blank=True)

    def __str__(self):
        return self.name

class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    # user_id
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="上传时间", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="数量")

    status_choices = (
        (1, "移栽"),
        (2, "采收"),
    )
    status = models.SmallIntegerField(verbose_name="二级分类", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class uploader(models.Model):
    """ 城市 """
    update_date = models.DateField(verbose_name="上传时间", auto_now=True)
    update_user = models.CharField(verbose_name="上传人", max_length=100, default="")
    # 本质上数据库也是CharField，自动保存数据。
    excel_file = models.FileField(verbose_name="excel_file", max_length=128, upload_to='city/', default='')


class BaseInfoBase(models.Model):
    ID = models.AutoField(primary_key=True)
    基地ID = models.IntegerField(null=True)
    基地 = models.CharField(max_length=255)
    代号 = models.CharField(max_length=255)
    基地经理 = models.CharField(max_length=255)
    面积 = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.代号

class BaseInfoProduct(models.Model):
    品类iD = models.AutoField(primary_key=True)
    品类名称 = models.CharField(max_length=255)
    品种名称 = models.CharField(max_length=255)


class BaseInfoWorkType(models.Model):
    level_choices = (
        (1, "1级分类"),
        (2, "2级分类"),
    )

    分类名称 = models.CharField(max_length=255)
    分类级别 = models.IntegerField(choices=level_choices, default=1)
    父分类 = models.CharField(max_length=255, default='', null=True, blank=True)
    工种ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.分类名称 if self.分类名称 else 'Unnamed Category'


class BaseInfoWorkHour(models.Model):
    工种ID = models.AutoField(primary_key=True)
    一级工种 = models.ForeignKey(
        'JobTypeDetailInfo',
        verbose_name="一级工种",
        on_delete=models.CASCADE,
        related_name="一级工种",
        limit_choices_to={'job_level': 1},  # 仅限一级工种
        null=True,
        blank=True
    )
    二级工种 = models.ForeignKey(
        'JobTypeDetailInfo',
        verbose_name="二级工种",
        on_delete=models.CASCADE,
        related_name="二级工种",
        limit_choices_to={'job_level': 2},  # 仅限二级工种
        null=True,
        blank=True
    )

    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=50, null=True)

    一级分类 = models.ForeignKey(
        'JobCategoryInfo',
        verbose_name="一级分类",
        on_delete=models.CASCADE,
        related_name="一级分类",
        limit_choices_to={'category_level': 1},  # 仅限一级分类
        null=True,
        blank=True
    )

    二级分类 = models.ForeignKey(
        'JobCategoryInfo',
        verbose_name="二级分类",
        on_delete=models.CASCADE,
        related_name="二级分类",
        limit_choices_to={'category_level': 2},  # 仅限二级分类
        null=True,
        blank=True
    )

    默认计入成本 = models.CharField(
        max_length=2,
        choices=[('是', '是'), ('否', '否')],
        default='是'
    )

    def __str__(self):
        return f"{self.一级工种.job_name} - {self.二级工种.job_name if self.二级工种 else ''}"

class PlanPlantBatch(models.Model):
    ID = models.AutoField(primary_key=True)
    批次ID = models.CharField(max_length=10, null=True)
    移栽日期 = models.DateField(null=True)
    品种 = models.CharField(max_length=255, null=True)
    品类 = models.CharField(max_length=255, null=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    基地ID = models.CharField(max_length=11, null=True)
    移栽数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    移栽板量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    点子数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    地块 = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=255, null=True)
    生长周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    采收期 = models.CharField(max_length=255, null=True)
    采收初期 = models.DateField(null=True)
    采收末期 = models.DateField(null=True)
    周期批次 = models.CharField(max_length=255, null=True)
    总周期天数 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    销毁面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    销毁备注 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    栽种方式 = models.CharField(max_length=255, null=True)
    正常产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    正常亩产 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    总产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    总亩产 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    下批前一天时间 = models.DateField(null=True)
    周期 = models.CharField(max_length=255, null=True)


class ProductionBatch(models.Model):
    iD = models.AutoField(primary_key=True)
    批次ID = models.CharField(max_length=255, unique=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    基地ID = models.ForeignKey(BaseInfoBase, on_delete=models.SET_NULL, null=True)
    销毁面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    产品iD = models.ForeignKey(BaseInfoProduct, on_delete=models.SET_NULL, null=True)
    地块 = models.CharField(max_length=255, null=True)
    批次 = models.IntegerField(null=True)
    生长周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    采收初期 = models.DateField(null=True)
    采收末期 = models.DateField(null=True)
    采收周期 = models.DateField(null=True)
    总周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际总产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    正常总产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    总亩产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    正常亩产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class CostTotal(models.Model):
    批次 = models.CharField(max_length=255, null=True)
    人工费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    农资费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    打药费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    打地费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    折旧费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    出库 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    销售 = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class PlanSummary(models.Model):
    移栽时间 = models.DateField(null=True)
    批次ID = models.CharField(max_length=255, null=True)
    计划种植 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际种植 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    计划达成率 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    生长周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    踩栽周期 = models.DateField(null=True)
    踩栽末期 = models.DateField(null=True)
    下一批前一天 = models.DateField(null=True)
    损耗 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际采收 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    计划实际采收率 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    预估客销售 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际销售 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    计划销售率 = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class PlanDaily(models.Model):
    上批批次 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    种植日期 = models.DateField(null=True)
    采收 = models.CharField(max_length=255, null=True)
    打地 = models.CharField(max_length=255, null=True)
    SC = models.CharField(max_length=255, null=True)
    FF = models.CharField(max_length=255, null=True)
    下一批种植日期 = models.DateField(null=True)
    种植品种 = models.CharField(max_length=255, null=True)
    未K = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=255, null=True)
    种植规格 = models.CharField(max_length=255, null=True)


class ProductionWage(models.Model):
    基地 = models.CharField(max_length=255, null=True)
    日期 = models.DateField(null=True, default=timezone.now)
    工人 = models.CharField(max_length=255, null=True)
    一级分类 = models.CharField(max_length=255, null=True)
    二级分类 = models.CharField(max_length=255, null=True)
    一级工种 = models.CharField(max_length=255, null=True)
    二级工种 = models.CharField(max_length=255, null=True)
    工时 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    工价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    累计工时 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    合计工资 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)
    负责人 = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=255, null=True, blank=True)


class CostAgriculture(models.Model):
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单据编号 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    商品全名 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    规格 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    备注 = models.CharField(max_length=255, null=True)


class CostPesticide(models.Model):
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际打药面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    次数 = models.IntegerField(null=True)
    服务人员 = models.CharField(max_length=255, null=True)
    申请打药时间 = models.DateField(null=True)
    预计打药时间 = models.DateField(null=True)
    实际打药时间 = models.DateField(null=True)


class CostAllocation(models.Model):
    月度 = models.CharField(max_length=255, null=True)
    散装工时 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    农家肥 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    材料 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    管理费 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    生活费 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    水电费 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    地租 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    大棚管架 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    大棚棚膜 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    大棚喷灌 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    其他资产 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    有机肥 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    出勤奖 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    服务费 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    基地经理 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    批次 = models.CharField(max_length=255, null=True)


class CostLandPreparation(models.Model):
    月份 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=10, null=True)
    批次 = models.CharField(max_length=255, null=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实际打药面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    备注 = models.CharField(max_length=255, null=True)
    打地人姓名 = models.CharField(max_length=255, null=True)
    申请打地时间 = models.DateField(null=True)
    预计打地时间 = models.DateField(null=True)
    实际打地时间 = models.DateField(null=True)
    工种 = models.CharField(max_length=255, null=True)


class SalesOutbound(models.Model):
    日期 = models.DateField(null=True)
    车牌 = models.CharField(max_length=255, null=True)
    公司 = models.CharField(max_length=255, null=True)
    市场 = models.CharField(max_length=255, null=True)
    品类 = models.CharField(max_length=255, null=True)
    规格 = models.CharField(max_length=255, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    重量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    地块 = models.CharField(max_length=255, null=True)
    批次 = models.CharField(max_length=255, null=True)
    盖布 = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=255, null=True)
    挑菜 = models.CharField(max_length=255, null=True)
    客户 = models.CharField(max_length=255, null=True)


class SalesDetail(models.Model):
    日期 = models.DateField(null=True)
    车次 = models.CharField(max_length=255, null=True)
    销售地区 = models.CharField(max_length=255, null=True)
    品类 = models.CharField(max_length=255, null=True)
    规格 = models.CharField(max_length=255, null=True)
    框数 = models.IntegerField(null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    重量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    销售额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)
    是否正常产量 = models.CharField(max_length=255, null=True)


class SalesSummary(models.Model):
    出库日期 = models.DateField(null=True)
    收款日期 = models.DateField(null=True)
    公司 = models.CharField(max_length=255, null=True)
    市场 = models.CharField(max_length=255, null=True)
    车牌 = models.CharField(max_length=255, null=True)
    销售人员 = models.CharField(max_length=255, null=True)
    客户 = models.CharField(max_length=255, null=True)
    类别 = models.CharField(max_length=255, null=True)
    品种 = models.CharField(max_length=255, null=True)
    应销框数 = models.IntegerField(null=True)
    实际框数 = models.IntegerField(null=True)
    单位 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    规格 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    数量 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    地块 = models.CharField(max_length=255, null=True)
    批次 = models.CharField(max_length=255, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    应收金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实收金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    应收金额合计 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    实收金额合计 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    差额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    合计框数 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    上车拨入框数 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    本车拨入框数 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    备注 = models.CharField(max_length=255, null=True)
    收款方式 = models.CharField(max_length=255, null=True)


class Agriculture_cost(models.Model):
    ID = models.AutoField(primary_key=True)
    日期 = models.DateField(null=True, blank=True)
    二级工种 = models.CharField(max_length=255, null=True)
    数量 = models.FloatField(null=True, blank=True)
    农资种类 = models.CharField(max_length=255, null=True)
    名称 = models.CharField(max_length=255, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)


from django.db import models
from django.utils import timezone


class Plant_batch(models.Model):
    ID = models.AutoField(primary_key=True)
    批次ID = models.CharField(max_length=50, unique=True, null=True, blank=True)  # 生成的批次ID
    二级分类 = models.CharField(max_length=255, null=True, blank=True)
    一级分类 = models.CharField(max_length=255, null=True, blank=True)
    基地 = models.CharField(max_length=255, null=True, blank=True)  # 新增的基地字段
    地块 = models.CharField(max_length=255, null=True, blank=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    基地经理 = models.CharField(max_length=255, null=True, blank=True)
    种植日期 = models.DateField(default=timezone.now, null=True, blank=True)  # 默认值为当天日期
    移栽板量 = models.FloatField(null=True, blank=True)
    移栽数量 = models.FloatField(null=True, blank=True)
    点籽日期 = models.DateField(null=True, blank=True)
    用籽量 = models.FloatField(null=True, blank=True)
    备注 = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.DateField(null=True, blank=True, default=timezone.now)
    uploader = models.CharField(max_length=255, null=True, blank=True)
    生长周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    采收期 = models.CharField(max_length=255, null=True, blank=True)
    采收初期 = models.DateField(null=True, blank=True)
    采收末期 = models.DateField(null=True, blank=True)
    周期批次 = models.CharField(max_length=255, null=True, blank=True)
    总周期天数 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    销毁面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    销毁备注 = models.CharField(max_length=255, null=True, blank=True)
    栽种方式 = models.CharField(max_length=255, null=True, blank=True)
    正常产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    正常亩产 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    总产量 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    总亩产 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    下批前一天时间 = models.DateField(null=True, blank=True)
    周期 = models.CharField(max_length=255, null=True, blank=True)

    # 新增工种的开始时间、结束时间、周期和数量字段
    打地开始时间 = models.DateField(null=True, blank=True)
    打地结束时间 = models.DateField(null=True, blank=True)
    打地周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    打地数量 = models.FloatField(null=True, blank=True)

    移栽开始时间 = models.DateField(null=True, blank=True)
    移栽结束时间 = models.DateField(null=True, blank=True)
    移栽周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    移栽数量 = models.FloatField(null=True, blank=True)

    除草开始时间 = models.DateField(null=True, blank=True)
    除草结束时间 = models.DateField(null=True, blank=True)
    除草周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    除草数量 = models.FloatField(null=True, blank=True)

    采收开始时间 = models.DateField(null=True, blank=True)
    采收结束时间 = models.DateField(null=True, blank=True)
    采收周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    采收数量 = models.FloatField(null=True, blank=True)

    清棚开始时间 = models.DateField(null=True, blank=True)
    清棚结束时间 = models.DateField(null=True, blank=True)
    清棚周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    清棚数量 = models.FloatField(null=True, blank=True)

    点籽开始时间 = models.DateField(null=True, blank=True)
    点籽结束时间 = models.DateField(null=True, blank=True)
    点籽周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    点籽数量 = models.FloatField(null=True, blank=True)

    间菜开始时间 = models.DateField(null=True, blank=True)
    间菜结束时间 = models.DateField(null=True, blank=True)
    间菜周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    间菜数量 = models.FloatField(null=True, blank=True)

    吹生菜开始时间 = models.DateField(null=True, blank=True)
    吹生菜结束时间 = models.DateField(null=True, blank=True)
    吹生菜周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    吹生菜数量 = models.FloatField(null=True, blank=True)

    施肥开始时间 = models.DateField(null=True, blank=True)
    施肥结束时间 = models.DateField(null=True, blank=True)
    施肥周期 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    施肥数量 = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 保持原逻辑：生成批次ID
        if not self.批次ID:
            base_code = self.基地 if self.基地 else "BASE"
            plant_date_str = self.种植日期.strftime('%Y%m%d') if self.种植日期 else "DATE"
            category_name = self.二级分类 if self.二级分类 else "CAT"
            self.批次ID = f"{base_code}-{plant_date_str}-{category_name}"

        # 同步相关字段的值，不改变原来的逻辑
        if self.移栽数量:
            self.移栽数量 = self.移栽数量
        if self.点籽日期:
            self.点籽开始时间 = self.点籽日期
        if self.用籽量:
            self.点籽数量 = self.用籽量
        if self.采收初期:
            self.采收开始时间 = self.采收初期
        if self.采收末期:
            self.采收结束时间 = self.采收末期
        if self.总产量:
            self.采收数量 = self.总产量

        super().save(*args, **kwargs)  # 保存到数据库

    def __str__(self):
        return f"批次: {self.批次ID}, 种植日期: {self.种植日期}, 基地: {self.基地}, 面积: {self.面积}"
class Salary_by_plople(models.Model):
    日期 = models.CharField(max_length=6)  # 假设日期字段已经是 "YYYYMM" 格式
    公司 = models.CharField(max_length=100)
    归属业主 = models.CharField(max_length=100)
    姓名 = models.CharField(max_length=100)
    清棚 = models.DecimalField(max_digits=10, decimal_places=2)
    点籽 = models.DecimalField(max_digits=10, decimal_places=2)
    移栽 = models.DecimalField(max_digits=10, decimal_places=2)
    锄草 = models.DecimalField(max_digits=10, decimal_places=2)
    间菜 = models.DecimalField(max_digits=10, decimal_places=2)
    拔草 = models.DecimalField(max_digits=10, decimal_places=2)
    打药 = models.DecimalField(max_digits=10, decimal_places=2)
    施肥 = models.DecimalField(max_digits=10, decimal_places=2)
    吹生菜 = models.DecimalField(max_digits=10, decimal_places=2)
    插竹竿绑线 = models.DecimalField(max_digits=10, decimal_places=2)
    收菜 = models.DecimalField(max_digits=10, decimal_places=2)
    清废菜 = models.DecimalField(max_digits=10, decimal_places=2)
    绑线 = models.DecimalField(max_digits=10, decimal_places=2)
    散工 = models.DecimalField(max_digits=10, decimal_places=2)
    修枝 = models.DecimalField(max_digits=10, decimal_places=2)
    绑枝 = models.DecimalField(max_digits=10, decimal_places=2)
    插竹竿 = models.DecimalField(max_digits=10, decimal_places=2)
    其它 = models.DecimalField(max_digits=10, decimal_places=2)
    铲沟草 = models.DecimalField(max_digits=10, decimal_places=2)
    锄拔草 = models.DecimalField(max_digits=10, decimal_places=2)
    合计工时 = models.DecimalField(max_digits=10, decimal_places=2)
    合计工资 = models.DecimalField(max_digits=10, decimal_places=2)
    平均工资 = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'views_工资花名册'
        managed = False  # 不让 Django 管理表的创建和删除
        verbose_name = '工资花名册'
        verbose_name_plural = '工资花名册'

    def __str__(self):
        return self.姓名

class Salary_by_daily(models.Model):
    id = models.AutoField(primary_key=True)  # 添加ID字段
    工人 = models.CharField(max_length=100)
    基地 = models.CharField(max_length=100)
    负责人 = models.CharField(max_length=100)
    月份 = models.CharField(max_length=6)  # 假设月份字段已经是 "YYYYMM" 格式
    day_1 = models.DecimalField(max_digits=10, decimal_places=2)
    day_2 = models.DecimalField(max_digits=10, decimal_places=2)
    day_3 = models.DecimalField(max_digits=10, decimal_places=2)
    day_4 = models.DecimalField(max_digits=10, decimal_places=2)
    day_5 = models.DecimalField(max_digits=10, decimal_places=2)
    day_6 = models.DecimalField(max_digits=10, decimal_places=2)
    day_7 = models.DecimalField(max_digits=10, decimal_places=2)
    day_8 = models.DecimalField(max_digits=10, decimal_places=2)
    day_9 = models.DecimalField(max_digits=10, decimal_places=2)
    day_10 = models.DecimalField(max_digits=10, decimal_places=2)
    day_11 = models.DecimalField(max_digits=10, decimal_places=2)
    day_12 = models.DecimalField(max_digits=10, decimal_places=2)
    day_13 = models.DecimalField(max_digits=10, decimal_places=2)
    day_14 = models.DecimalField(max_digits=10, decimal_places=2)
    day_15 = models.DecimalField(max_digits=10, decimal_places=2)
    day_16 = models.DecimalField(max_digits=10, decimal_places=2)
    day_17 = models.DecimalField(max_digits=10, decimal_places=2)
    day_18 = models.DecimalField(max_digits=10, decimal_places=2)
    day_19 = models.DecimalField(max_digits=10, decimal_places=2)
    day_20 = models.DecimalField(max_digits=10, decimal_places=2)
    day_21 = models.DecimalField(max_digits=10, decimal_places=2)
    day_22 = models.DecimalField(max_digits=10, decimal_places=2)
    day_23 = models.DecimalField(max_digits=10, decimal_places=2)
    day_24 = models.DecimalField(max_digits=10, decimal_places=2)
    day_25 = models.DecimalField(max_digits=10, decimal_places=2)
    day_26 = models.DecimalField(max_digits=10, decimal_places=2)
    day_27 = models.DecimalField(max_digits=10, decimal_places=2)
    day_28 = models.DecimalField(max_digits=10, decimal_places=2)
    day_29 = models.DecimalField(max_digits=10, decimal_places=2)
    day_30 = models.DecimalField(max_digits=10, decimal_places=2)
    day_31 = models.DecimalField(max_digits=10, decimal_places=2)
    合计 = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'views_每日工资表'
        managed = False  # 不让 Django 管理表的创建和删除
        verbose_name = '每日工资表'
        verbose_name_plural = '每日工资表'

    def __str__(self):
        return self.姓名


class Workhour_by_daily(models.Model):
    id = models.AutoField(primary_key=True)  # 添加ID字段
    工人 = models.CharField(max_length=100)
    基地 = models.CharField(max_length=100)
    负责人 = models.CharField(max_length=100)
    月份 = models.CharField(max_length=6)  # 假设月份字段已经是 "YYYYMM" 格式
    day_1 = models.DecimalField(max_digits=10, decimal_places=2)
    day_2 = models.DecimalField(max_digits=10, decimal_places=2)
    day_3 = models.DecimalField(max_digits=10, decimal_places=2)
    day_4 = models.DecimalField(max_digits=10, decimal_places=2)
    day_5 = models.DecimalField(max_digits=10, decimal_places=2)
    day_6 = models.DecimalField(max_digits=10, decimal_places=2)
    day_7 = models.DecimalField(max_digits=10, decimal_places=2)
    day_8 = models.DecimalField(max_digits=10, decimal_places=2)
    day_9 = models.DecimalField(max_digits=10, decimal_places=2)
    day_10 = models.DecimalField(max_digits=10, decimal_places=2)
    day_11 = models.DecimalField(max_digits=10, decimal_places=2)
    day_12 = models.DecimalField(max_digits=10, decimal_places=2)
    day_13 = models.DecimalField(max_digits=10, decimal_places=2)
    day_14 = models.DecimalField(max_digits=10, decimal_places=2)
    day_15 = models.DecimalField(max_digits=10, decimal_places=2)
    day_16 = models.DecimalField(max_digits=10, decimal_places=2)
    day_17 = models.DecimalField(max_digits=10, decimal_places=2)
    day_18 = models.DecimalField(max_digits=10, decimal_places=2)
    day_19 = models.DecimalField(max_digits=10, decimal_places=2)
    day_20 = models.DecimalField(max_digits=10, decimal_places=2)
    day_21 = models.DecimalField(max_digits=10, decimal_places=2)
    day_22 = models.DecimalField(max_digits=10, decimal_places=2)
    day_23 = models.DecimalField(max_digits=10, decimal_places=2)
    day_24 = models.DecimalField(max_digits=10, decimal_places=2)
    day_25 = models.DecimalField(max_digits=10, decimal_places=2)
    day_26 = models.DecimalField(max_digits=10, decimal_places=2)
    day_27 = models.DecimalField(max_digits=10, decimal_places=2)
    day_28 = models.DecimalField(max_digits=10, decimal_places=2)
    day_29 = models.DecimalField(max_digits=10, decimal_places=2)
    day_30 = models.DecimalField(max_digits=10, decimal_places=2)
    day_31 = models.DecimalField(max_digits=10, decimal_places=2)
    合计工时 = models.DecimalField(max_digits=10, decimal_places=2)
    累积工时 = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'views_每月工时表'
        managed = False  # 不让 Django 管理表的创建和删除
        verbose_name = '每月工时表'
        verbose_name_plural = '每月工时表'

    def __str__(self):
        return self.姓名


from django.db import models

class ExpenseAllocation(models.Model):
    批次= models.CharField(max_length=100)
    散工工时 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="散工工时")
    浇水打杂费用 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="浇水打杂费用")
    材料费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="材料费")
    管理费1 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="管理费1")
    生活费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="生活费")
    水电费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="水电费")
    报销费用 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="报销费用")
    其他费用 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="其他费用")
    地租 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="地租")
    其他资产 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="其他资产")
    农家肥 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="农家肥")
    有机肥 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="有机肥")
    草莓土 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="草莓土")
    出勤奖 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="出勤奖")
    服务费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="服务费")
    地租大棚摊销 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="地租大棚摊销")
    基地经理 = models.CharField(max_length=100)
    燃油费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="燃油费", default=0)
    维修费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="维修费", default=0)
    销售费 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="销售费", default=0)
    class Meta:
        verbose_name = "费用摊销"
        verbose_name_plural = "费用摊销"

    def __str__(self):
        return f"ExpenseAllocation({self.id})"


class DepreciationAllocation(models.Model):
    地租 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="地租")
    大棚管架 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="大棚管架")
    大棚棚膜 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="大棚棚膜")
    大棚喷灌 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="大棚喷灌")
    其他资产 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="其他资产")
    材料 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="材料")
    基地经理 = models.ForeignKey(BaseInfoBase, on_delete=models.CASCADE, verbose_name="基地经理")
    月份 = models.DateField(verbose_name="月份", default=datetime.now().strftime("%Y-%m-01"))

    class Meta:
        verbose_name = "折旧摊销"
        verbose_name_plural = "折旧摊销"

    def __str__(self):
        return f"DepreciationAllocation({self.id})"

class LossReport(models.Model):
    报损时间 = models.DateTimeField(verbose_name="报损时间", default=datetime.now)
    报损人 = models.CharField(max_length=255, verbose_name="报损人")
    批次 = models.CharField(max_length=255, verbose_name="批次")
    报损地块 = models.CharField(max_length=255, verbose_name="报损地块")
    报损类型 = models.CharField(max_length=50, choices=[('地内报损', '地内报损'), ('销售报损', '销售报损')], verbose_name="报损类型")
    报损数量 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="报损数量")
    报损单位 = models.CharField(max_length=50, verbose_name="报损单位")
    报损面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 新增报损面积
    备注 = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "报损"
        verbose_name_plural = "报损"

    def __str__(self):
        return f"LossReport({self.id})"


class Salesperson(models.Model):
    姓名 = models.CharField(max_length=255, verbose_name="姓名")
    所属公司 = models.CharField(max_length=255, verbose_name="所属公司")
    电话 = models.CharField(max_length=20, verbose_name="电话")

    class Meta:
        verbose_name = "销售人员"
        verbose_name_plural = "销售人员"

    def __str__(self):
        return self.姓名
from django.db import models

class Market(models.Model):
    市场名称 = models.CharField(max_length=255, unique=True, verbose_name="市场名称")
    地区 = models.CharField(max_length=255, verbose_name="地区")
    地址 = models.CharField(max_length=255, verbose_name="地址")
    联系人 = models.CharField(max_length=255, verbose_name="联系人")
    插入时间 = models.DateTimeField(auto_now_add=True, verbose_name="插入时间")

    class Meta:
        verbose_name = "市场信息"

    def __str__(self):
        return self.市场名称


class Vehicle(models.Model):
    车牌 = models.CharField(max_length=50, unique=True, verbose_name="车牌")
    司机 = models.CharField(max_length=255, verbose_name="司机")
    电话 = models.CharField(max_length=20, verbose_name="电话")
    型号 = models.CharField(max_length=255, verbose_name="型号")
    颜色 = models.CharField(max_length=255, verbose_name="颜色")
    类型 = models.CharField(max_length=255, verbose_name="类型")
    备注 = models.TextField(verbose_name="备注", null=True, blank=True)
    身份证号码 = models.CharField(max_length=18, verbose_name="身份证号码", null=True, blank=True)
    市场分类 = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="市场分类")

    class Meta:
        verbose_name = "车辆管理"
        verbose_name_plural = "车辆管理"

    def __str__(self):
        return self.车牌





class Customer(models.Model):
    """
    客户管理模型，用于存储客户相关的信息。
    """
    # 基本信息
    客户名称 = models.CharField(max_length=255, verbose_name="客户名称")
    联系人 = models.CharField(max_length=255, verbose_name="联系人")
    联系电话 = models.CharField(max_length=20, verbose_name="联系电话")
    邮箱 = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    地址 = models.CharField(max_length=255, verbose_name="地址", null=True, blank=True)
    销售地区 = models.CharField(max_length=255, verbose_name="销售地区")
    客户类型 = models.CharField(
        max_length=50,
        verbose_name="客户类型",
        choices=[('个人', '个人'), ('企业', '企业')]
    )
    公司名称 = models.CharField(max_length=255, verbose_name="公司名称", null=True, blank=True)
    公司网站 = models.URLField(verbose_name="公司网站", null=True, blank=True)
    公司地址 = models.CharField(max_length=255, verbose_name="公司地址", null=True, blank=True)
    行业 = models.CharField(max_length=255, verbose_name="行业", null=True, blank=True)
    备注 = models.TextField(verbose_name="备注", null=True, blank=True)

    # 新增字段
    是否新客户 = models.CharField(
        max_length=10,
        verbose_name="是否新客户",
        choices=[('新客户', '新客户'), ('老客户', '老客户')],
        default='新客户'
    )
    主要销售地区 = models.CharField(
        max_length=255,
        verbose_name="主要销售地区",
        null=True,
        blank=True
    )
    主要销售品种 = models.CharField(
        max_length=255,
        verbose_name="主要销售品种",
        null=True,
        blank=True
    )
    客户流失时间 = models.DateField(
        verbose_name="客户流失时间",
        null=True,
        blank=True
    )
    客户流失原因 = models.TextField(
        verbose_name="客户流失原因",
        null=True,
        blank=True
    )

    # 外键字段
    市场分类 = models.ForeignKey(
        Market,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="市场分类"
    )

    # 时间戳
    创建时间 = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    更新时间 = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "客户管理"
        verbose_name_plural = "客户管理"

    def __str__(self):
        return self.客户名称

class OutboundRecord(models.Model):
    日期 = models.DateField(null=True, default=timezone.now, verbose_name="日期")
    运送数量 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运送数量")
    车牌 = models.CharField(max_length=255, verbose_name="车牌")
    公司 = models.CharField(max_length=255, verbose_name="公司")
    市场 = models.CharField(max_length=255, verbose_name="市场")
    品类 = models.CharField(max_length=255, verbose_name="品类")
    品种 = models.CharField(max_length=255, verbose_name="品种")
    规格 = models.CharField(max_length=255, verbose_name="规格")
    单位 = models.CharField(max_length=255, verbose_name="单位")
    数量_筐 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="数量/筐")
    重量_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="重量/kg")
    地块 = models.CharField(max_length=255, verbose_name="地块")
    批次 = models.CharField(max_length=255, verbose_name="批次")
    盖布_块 = models.CharField(max_length=255, verbose_name="盖布/块")
    备注 = models.TextField(verbose_name="备注", null=True, blank=True)
    挑菜 = models.CharField(max_length=255, verbose_name="挑菜")
    客户 = models.CharField(max_length=255, verbose_name="客户")

    class Meta:
        verbose_name = "出库记录"
        verbose_name_plural = "出库记录"

    def __str__(self):
        return f"{self.日期} - {self.车牌} - {self.公司}"
class SalesRecord(models.Model):
    出库记录 = models.ForeignKey(OutboundRecord, on_delete=models.CASCADE, related_name='sales_records')
    批次 = models.CharField(max_length=255, verbose_name="批次", default=None)
    销售日期 = models.DateField(null=True, default=timezone.now, verbose_name="销售日期")
    客户 = models.CharField(max_length=255, verbose_name="客户")
    数量 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="数量", default=0)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价", default=0)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额", default=0)
    应收金额 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="应收金额", default=0)
    实收金额 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="实收金额", default=0)
    备注 = models.TextField(verbose_name="备注", null=True, blank=True)
    # 新增字段
    收款日期 = models.DateField(null=True, blank=True, verbose_name="收款日期")
    销售人员 = models.CharField(max_length=255, verbose_name="销售人员", null=True, blank=True)
    单位 = models.CharField(max_length=255, verbose_name="单位", null=True, blank=True)
    规格 = models.CharField(max_length=255, verbose_name="规格", null=True, blank=True)
    收款方式 = models.CharField(max_length=255, verbose_name="收款方式", null=True, blank=True)

    class Meta:
        verbose_name = "销售记录"
        verbose_name_plural = "销售记录"

    def __str__(self):
        return f"{self.客户} - {self.数量}"

from django.db import models

class V_Profit_Summary(models.Model):
    批次 = models.CharField(max_length=255, primary_key=True)
    工时费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    农资费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    散工工时 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    浇水打杂费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    材料费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    管理费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    生活费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    水电费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    报销费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    其他费用 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    地租 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    其他资产 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    农家肥 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    有机肥 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    草莓土 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    出勤奖金 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    服务费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    地租大棚摊销 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    燃油费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    维修费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    销售费 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    销售收入 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    总成本 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    利润 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False  # Django不管理这个模型
        db_table = 'V_Profit_Summary'  # 对应的数据库视图名

# 分类表
class JobCategoryInfo(models.Model):
    LEVEL_CHOICES = (
        (1, "一级分类"),
        (2, "二级分类"),
    )

    category_name = models.CharField(verbose_name="分类名称", max_length=50)
    category_level = models.IntegerField(verbose_name="分类级别", choices=LEVEL_CHOICES)
    parent_category = models.ForeignKey('self', verbose_name="父分类", null=True, blank=True, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return self.category_name

# 工种表
# models.py
class JobTypeDetailInfo(models.Model):
    CATEGORY_CHOICES = (
        (1, "一级工种"),
        (2, "二级工种"),
    )

    job_name = models.CharField(verbose_name="工种名称", max_length=50)
    job_level = models.IntegerField(verbose_name="工种级别", choices=CATEGORY_CHOICES)
    parent_job = models.ForeignKey('self', verbose_name="父工种", null=True, blank=True, on_delete=models.CASCADE, related_name="sub_work_types")

    def __str__(self):
        return self.job_name


class DailyPriceReport(models.Model):
    日期 = models.DateField(verbose_name="日期")
    品种 = models.ForeignKey(JobCategoryInfo, verbose_name="品种", on_delete=models.CASCADE)
    市场 = models.ForeignKey(Market, verbose_name="市场", on_delete=models.CASCADE)
    价格 = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "每日价格上报"
        verbose_name_plural = "每日价格上报"

    def __str__(self):
        return f"{self.日期} - {self.品种.category_name} - {self.市场.market_name}"  # 假设 category_name 和 market_name 是字段名

class MonthlyPlan(models.Model):
    日期 = models.DateField()
    二级分类 = models.ForeignKey(JobCategoryInfo, on_delete=models.CASCADE)
    面积 = models.DecimalField(max_digits=10, decimal_places=2)
    周期 = models.IntegerField()
    基地 = models.CharField(max_length=255)
    地块 = models.CharField(max_length=255)
   # 添加反馈字段
    未达成反馈 = models.TextField(verbose_name="未达成反馈", null=True, blank=True)
# 日计划
class DailyPlan(models.Model):
    批次ID = models.CharField(max_length=100, primary_key=True, verbose_name="批次 ID")
    基地经理 = models.CharField(max_length=255, verbose_name="基地经理")
    地块 = models.CharField(max_length=255, verbose_name="地块")
    面积 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="面积")
    种植日期 = models.DateField(verbose_name="种植日期")
    生长周期 = models.IntegerField(verbose_name="生长周期", help_text="单位为天")
    采收期 = models.IntegerField(verbose_name="采收期", help_text="单位为天")
    采收初期 = models.DateField(verbose_name="采收初期", null=True, blank=True)
    采收末期 = models.DateField(verbose_name="采收末期", null=True, blank=True)
    备注 = models.TextField(verbose_name="备注", null=True, blank=True)

    def __str__(self):
        return self.批次ID


# 费用超支反馈
class CostAlertFeedback(models.Model):
    批次ID = models.CharField(max_length=50)
    工种 = models.CharField(max_length=255, null=True, blank=True)
    反馈内容 = models.TextField(null=True, blank=True)
    反馈时间 = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.批次ID} - {self.工种} - 反馈时间: {self.反馈时间}"

class BatchCost(models.Model):
    批次ID = models.CharField(max_length=50)
    计划内成本 = models.DecimalField(max_digits=10, decimal_places=2)

    # 其他字段...

    class Meta:
        managed = False
        db_table = 'views_批次计划内成本'


class ProcessAlert(models.Model):
    一级分类 = models.CharField(max_length=100)
    二级分类 = models.CharField(max_length=100)
    一级工种 = models.CharField(max_length=100)
    二级工种 = models.CharField(max_length=100)
    最小时间 = models.PositiveIntegerField(help_text="最小时间（单位：天）")
    最大时间 = models.PositiveIntegerField(help_text="最大时间（单位：天）")

    def __str__(self):
        return f"{self.一级分类} - {self.二级分类} - {self.一级工种} - {self.二级工种}"