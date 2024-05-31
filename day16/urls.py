"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.models import BaseInfoWorkHour, PlanPlantBatch
from app01.views import depart, user, pretty, admin, account, task, order, chart, upload, city, worktype, baseinfo, \
    WorkHour, planplantbatch, productionwage, agriculturecost, Plant_batch, views

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),


    path('tt/', chart.tt),
    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/multi/', depart.depart_multi),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 工种管理
    path('BaseInfoWorkType/list/', worktype.work_type_list),
    path('BaseInfoWorkType/add/', worktype.work_type_add),
    path('BaseInfoWorkType/<int:nid>/edit/', worktype.work_type_edit),
    path('BaseInfoWorkType/<int:nid>/delete/', worktype.work_type_delete),


    # 基地管理
    path('BaseInfo/list/', baseinfo.BaseInfo_list),
    path('BaseInfo/add/', baseinfo.BaseInfo_add),

    # 工时管理
    path('production_wage_list/list/', productionwage.production_wage_list),
    path('productionwate/add/undefined/', productionwage.production_wage_list),
    path('productionwate/add/', productionwage.production_wage_add),
    path('productionwate/<int:nid>/delete/', productionwage.production_wage_delete),
    path('productionwate/<int:nid>/edit/', productionwage.productionwate_edit),
    path('upload/productionwate/', upload.upload_productionwate_modal_form),  # 工时批量上传


    path('get_productionwate/', productionwage.get_productionwate), #ajax获得价格和类型
    path('get_productionwate_price/', productionwage.get_productionwate_price),  # ajax获得价格和类型
    path('get_Plant_batch_dk/', productionwage.get_Plant_batch_dk),  # ajax获得地块

    path('get_second_level_categories/', WorkHour.get_second_level_categories),#ajax二级类型和类型


    # 工价管理
    path('WorkHour/list/', WorkHour.Hour_list),
    path('WorkHour/add/', WorkHour.WorkHour_add),
    path('WorkHour/<int:nid>/edit/', WorkHour.work_hour_edit),
    path('WorkHour/<int:nid>/delete/', WorkHour.work_hour_delete),
    path('upload/WorkHour/', upload.upload_workhour_modal_form),  # 工价批量上传

    # 农资管理
    path('Agricureture/list/', agriculturecost.agriculture_cost_list),
    path('Agricureture/add/', agriculturecost.agriculture_cost_add),
    path('Agricureture/<int:nid>/edit/', agriculturecost.agriculture_cost_edit),
    path('Agricureture/<int:nid>/delete/', agriculturecost.agriculture_cost_delete),
    path('upload/agriculturecost/', upload.upload_agriculturecost_modal_form),  # 工价批量上传

    # 批次表管理
    path('Plant_batch/list/', Plant_batch.Plant_batch_list),
    path('Plant_batch/add/', Plant_batch.Plant_batch_add),
    path('Plant_batch/<int:nid>/edit/', Plant_batch.Plant_batch_edit),
    path('Plant_batch/<int:nid>/delete/', Plant_batch.Plant_batch_delete),
    path('upload/Plant_batch/', upload.upload_Plant_batch_modal_form),  # 工价批量上传
    # 实现自动补全功能
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('test/',views.add_multiple_work_hours),


    # 月度计划
    path('PlanPlantBatch/list/',planplantbatch.planplantbatch_list),


    # 靓号管理
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # 管理员的管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),  # 学习Ajax
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.highcharts),

    # 上传文件
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    #path('upload/modal/form/', upload.upload_modal_form),

    # 城市列表
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),
]
