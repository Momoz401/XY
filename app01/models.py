from datetime import timedelta

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


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


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")

    # 本质上数据库也是CharField，自动保存数据。
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')


class LotNumber(models.Model):
    """ 批次表 """
    lot_id = models.CharField(verbose_name="批次ID", max_length=32)
    lot_area = models.DecimalField(verbose_name="面积", decimal_places=2, max_digits=10)
    base_id = models.ForeignKey(to="BasePlace", to_field="base_id", max_length=32, on_delete=models.SET_NULL())  # 置空处理
    destroy_area = models.DecimalField(verbose_name="销毁面积", decimal_places=5, max_digits=2)
    product_id = models.ForeignKey(verbose_name="产品", to="Products", to_field="product_id",
                                   on_delete=models.SET_NULL(), null=True)
    lot_massif = models.CharField(verbose_name="地块", max_length=10, blank=True)
    lot_number = models.CharField(verbose_name="批次", max_length=10, blank=True)
    growth_cycle = models.CharField(verbose_name="生长周期", max_length=10, blank=True)
    recovery_start_date = models.DateField(verbose_name="采摘初期")
    recovery_end_date = models.DateField(verbose_name="采摘末期")
    recovered_period = models.DurationField(verbose_name="采摘周期", blank=True, null=True)  # 通过计算得到
    all_period_date = models.DateField(verbose_name="总周期", blank=True, null=True)
    all_production = models.DecimalField(verbose_name="总产量", max_digits=5, decimal_places=2, default=0)
    normal_production = models.DecimalField(verbose_name="总产量", max_digits=5, decimal_places=2, default=0)
    all_per_mu_production = models.DecimalField(verbose_name="总亩产量", max_digits=5, decimal_places=2, default=0)
    normal_per_mu_production = models.DecimalField(verbose_name="正常亩量", max_digits=5, decimal_places=2, default=0)


'''
@receiver是Django框架中用于连接信号（Signal）和信号处理器（Signal handler）的装饰器。在Django中，
信号是一种发布-订阅模式的实现，允许一个组件发送消息并让其他组件在消息发送时做出响应。
当某个事件发生时，例如保存一个模型实例，Django会触发相应的信号。然后，您可以使用@receiver装饰器将信号连接到一个函数，这个函数会在信号触发时执行。
'''


@receiver(pre_save, sender=LotNumber)
def calculate_date_difference(sender, instance, **kwargs):
    if instance.recovery_start_date and instance.recovery_end_date:
        difference = instance.recovery_end_date - instance.recovery_start_date
        instance.recovered_period = timedelta(days=difference.days)


class BasePlace(models.Model):
    """基地表"""
    base_id = models.CharField(verbose_name="基地id", max_length=32, primary_key=True)
    base_name = models.CharField(verbose_name="基地名称", max_length=32)
    base_manager = models.CharField(verbose_name="基地经理", max_length=32)

    def __str__(self):
        return self.base_name


class Plants(models.Model):
    lot_id = models.CharField(verbose_name="批次ID", max_length=32, primary_key=True)
    plant_date = models.DateField(verbose_name="种植日期")
    plant_type = models.CharField(verbose_name="栽种类型", max_length=32)


class Products(models.Model):
    product_id = models.CharField(verbose_name="品类id", max_length=10, primary_key=True)
    product_category_name = models.CharField(verbose_name="品类名称", max_length=10, null=False)
    product_brand = models.CharField(verbose_name="品种名称", max_length=10, null=False)


class WorkType(models.Model):
    name = models.CharField(max_length=50, verbose_name='工种名称')
    parent_work_type = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                         related_name='sub_work_types', verbose_name='父工种')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.parent_work_type:
            return f"{self.parent_work_type.get_full_name()} - {self.name}"
        return self.name


"""
这里非常重要这里是一个工时单价表
"""


class Task(models.Model):
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='工种')
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name='分类')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    unit = models.CharField(max_length=10, verbose_name='单位')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f"{self.work_type.get_full_name()} - {self.category if self.category else '无分类'}"
