from datetime import datetime

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
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


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
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
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
    update_user = models.CharField(verbose_name="上传人", max_length=100, default="admin")

    # 本质上数据库也是CharField，自动保存数据。
    excel_file = models.FileField(verbose_name="excel_file", max_length=128, upload_to='city/', default='')


class BaseInfoBase(models.Model):
    ID = models.AutoField(primary_key=True)
    基地ID = models.IntegerField(null=True)
    基地 = models.CharField(max_length=255)
    代号 = models.CharField(max_length=255)
    基地经理 = models.CharField(max_length=255)
    面积 = models.FloatField(null=True, blank=True)


class BaseInfoProduct(models.Model):
    品类iD = models.AutoField(primary_key=True)
    品类名称 = models.CharField(max_length=255)
    品种名称 = models.CharField(max_length=255)


class BaseInfoWorkType(models.Model):
    level_choices = (
        (1, "1级分类"),
        (2, "2级分类"),
    )

    工种名称 = models.CharField(max_length=255)
    工种级别 = models.IntegerField(choices=level_choices, default=1)
    父工种 = models.CharField(max_length=255, default='', null=True, blank=True)
    工种ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.父工种


class BaseInfoWorkHour(models.Model):
    工种ID = models.AutoField(primary_key=True)
    工种 = models.CharField(max_length=255)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    单位 = models.CharField(max_length=255, null=True)
    备注 = models.CharField(max_length=50, null=True)
    一级分类 = models.CharField(max_length=255, null=True)
    二级分类 = models.CharField(max_length=255, null=True)


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
    工种 = models.CharField(max_length=255, null=True)
    一级分类 = models.CharField(max_length=255, null=True)
    二级分类 = models.CharField(max_length=255, null=True)
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
    工种 = models.CharField(max_length=255, null=True)
    数量 = models.FloatField(null=True, blank=True)
    农资种类 = models.CharField(max_length=255, null=True)
    名称 = models.CharField(max_length=255, null=True)
    单价 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    金额 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    批次 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)


class Plant_batch(models.Model):
    ID = models.AutoField(primary_key=True)
    批次ID = models.CharField(max_length=10, null=True)
    品种 = models.CharField(max_length=255, null=True)
    品类 = models.CharField(max_length=255, null=True)
    地块 = models.CharField(max_length=255, null=True)
    面积 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    基地经理 = models.CharField(max_length=255, null=True, blank=True)
    移栽日期 = models.DateField(null=True, blank=True, default=timezone.now)
    移栽板量 = models.FloatField(null=True, blank=True)
    移栽数量 = models.FloatField(null=True, blank=True)
    点籽日期 = models.DateField(null=True, blank=True, default=timezone.now)
    用籽量 = models.FloatField(null=True, blank=True)
    备注 = models.CharField(max_length=255, null=True)


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