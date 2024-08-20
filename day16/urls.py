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
    WorkHour, planplantbatch, productionwage, agriculturecost, Plant_batch, views, report
from app01.views.views import create_expense_allocation, expense_allocation_list, expense_allocation_add, \
    expense_allocation_edit, expense_allocation_delete, depreciation_allocation_list, depreciation_allocation_add, \
    depreciation_allocation_edit, depreciation_allocation_delete, loss_report_list, loss_report_add, loss_report_edit, \
    loss_report_delete, get_plant_batch_dk, loss_report_autocomplete, salesperson_list, salesperson_add, \
    salesperson_edit, salesperson_delete, vehicle_list, vehicle_add, vehicle_edit, vehicle_delete, market_list, \
    market_add, market_edit, market_delete, customer_list, customer_add, customer_edit, customer_delete, \
    add_sales_record, fetch_unique_second_level_categories, outbound_list, outbound_add, outbound_edit, \
    outbound_delete, get_sales_records, add_sale_form, sales_record_edit, sales_record_delete, sales_record_add

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
    path('BaseInfo/<int:nid>/edit/',baseinfo.BaseInfo_edit),
    path('BaseInfo/<int:nid>/delete/', baseinfo.BaseInfo_delete),



    # 工时管理
    path('production_wage_list/list/', productionwage.production_wage_list),
    path('productionwate/add/undefined/', productionwage.production_wage_list),
    path('productionwate/add/', productionwage.production_wage_add),
    path('productionwate/<int:nid>/delete/', productionwage.production_wage_delete),
    path('productionwate/<int:nid>/edit/', productionwage.productionwate_edit),
    path('upload/productionwate/', upload.upload_productionwate_modal_form),  # 工时批量上传
    path('get_productionwate/', productionwage.get_productionwate), # ajax获得价格和类型
    path('get_productionwate_price/', productionwage.get_productionwate_price),  # ajax获得价格和类型
    path('get_Plant_batch_dk/', productionwage.get_Plant_batch_dk),  # ajax获得地块
    path('get_second_level_categories/', WorkHour.get_second_level_categories),  # ajax二级类型和类型


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
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('autocomplete_baseinfo/', views.autocomplete_baseinfo, name='autocomplete_baseinfo'),
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
    # 工资明细表
    path('report/list/', report.report_list),  # 工资明细表
    path('report/get_tables_date/', report.data_table_view, name="data_table_view"),
    # 散工工资
    path('report_salary_temp_by_daily/list', report.report_salary_temp_by_daily),  # 工资明细表
    path('report_salary_temp_by_daily/get_tables_date/', report.report_salary_temp_by_daily_data_table_view, name="report_salary_temp_by_daily"),
    # 工资花名册
    path('report_salary_by_plople/list/', report.report_salary_by_plople),
    path('report_salary_by_plople/get_tables_date/', report.report_salary_by_plople_data_table_view, name="report_salary_by_plople"), # 获取工资花名册
    # 每日工资表
    path('report_salary_by_daily/list/', report.report_salary_by_daily),# 每日工资表
    path('report_salary_by_daily/get_tables_date/', report.report_salary_by_daily_data_table_view,name="report_salary_by_daily"),
    # 每日工时
    path('report_workhour_by_daily/list/', report.report_workhour_by_daily),  # 每日工时
    path('report_workhour_by_daily/get_tables_date/', report.report_workhour_by_daily_data_table_view,name="report_workhour_by_daily"),

    # 对照管理
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

    # 费用分摊
    path('expense_allocation/list/', expense_allocation_list, name='expense_allocation_list'),
    path('expense_allocation/add/', expense_allocation_add, name='expense_allocation_add'),
    path('expense_allocation/<int:nid>/edit/', expense_allocation_edit, name='expense_allocation_edit'),
    path('expense_allocation/<int:nid>/delete/', expense_allocation_delete, name='expense_allocation_delete'),
    # 折旧摊销
    path('depreciation_allocation/list/', depreciation_allocation_list, name='depreciation_allocation_list'),
    path('depreciation_allocation/add/', depreciation_allocation_add, name='depreciation_allocation_add'),
    path('depreciation_allocation/<int:nid>/edit/', depreciation_allocation_edit, name='depreciation_allocation_edit'),
    path('depreciation_allocation/<int:nid>/delete/', depreciation_allocation_delete,name='depreciation_allocation_delete'),
    # 报损
    path('loss_report/list/', loss_report_list, name='loss_report_list'),
    path('loss_report/add/', loss_report_add, name='loss_report_add'),
    path('loss_report/<int:nid>/edit/', loss_report_edit, name='loss_report_edit'),
    path('loss_report/<int:nid>/delete/', loss_report_delete, name='loss_report_delete'),
    path('loss_report_autocomplete/', loss_report_autocomplete, name='loss_report_autocomplete'),
    path('get_plant_batch_dk/', get_plant_batch_dk, name='get_plant_batch_dk'),
    # 销售
    path('salesperson/list/', salesperson_list, name='salesperson_list'),
    path('salesperson/add/', salesperson_add, name='salesperson_add'),
    path('salesperson/<int:nid>/edit/', salesperson_edit, name='salesperson_edit'),
    path('salesperson/<int:nid>/delete/', salesperson_delete, name='salesperson_delete'),
    # 车辆
    path('vehicle/list/', vehicle_list, name='vehicle_list'),
    path('vehicle/add/', vehicle_add, name='vehicle_add'),
    path('vehicle/<int:nid>/edit/', vehicle_edit, name='vehicle_edit'),
    path('vehicle/<int:nid>/delete/', vehicle_delete, name='vehicle_delete'),
    # 市场
    path('market/list/', market_list, name='market_list'),
    path('market/add/', market_add, name='market_add'),
    path('market/<int:nid>/edit/', market_edit, name='market_edit'),
    path('market/<int:nid>/delete/', market_delete, name='market_delete'),
    # 客户
    path('customer/list/', customer_list, name='customer_list'),
    path('customer/add/', customer_add, name='customer_add'),
    path('customer/<int:nid>/edit/', customer_edit, name='customer_edit'),
    path('customer/<int:nid>/delete/', customer_delete, name='customer_delete'),
    # 出库
    path('outbound/list/', outbound_list, name='outbound_list'),
    path('outbound/add/', outbound_add, name='outbound_add'),
    path('outbound/edit/<int:nid>/', outbound_edit, name='outbound_edit'),
    path('outbound/delete/<int:nid>/', outbound_delete, name='outbound_delete'),
    path('get_sales_records/', get_sales_records, name='get_sales_records'),
    path('add_sale_form/', add_sale_form, name='add_sale_form'),
    path('fetch_unique_second_level_categories/', fetch_unique_second_level_categories,
         name='fetch_unique_second_level_categories'),
    path('sales_record/add/<int:outbound_id>/', sales_record_add, name='sales_record_add'),
    path('sales_record/edit/<int:pk>/', sales_record_edit, name='sales_record_edit'),
    path('sales_record/delete/<int:pk>/', sales_record_delete, name='sales_record_delete'),

    # 单独管理销售记录的URL
    path('sales_record/management/list/', views.sales_record_management_list, name='sales_record_management_list'),
    path('sales_record/management/add/', views.sales_record_management_add, name='sales_record_management_add'),
    path('sales_record/management/<int:pk>/edit/', views.sales_record_management_edit,
         name='sales_record_management_edit'),
    path('sales_record/management/<int:pk>/delete/', views.sales_record_management_delete,
         name='sales_record_management_delete'),

    # 日历显示种植批次
    path('Plant_batch/calendar/', views.plant_batch_calendar_view, name='plant_batch_calendar_view'),


]
