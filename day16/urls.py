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

from app01.mobile.views import mobile_login, mobile_home, mobile_logout, mobile_gongshiluru, mobile_outbound_add, \
    customer_autocomplete, worker_autocomplete, batch_autocomplete, batch_autocomplete_pc, get_Plant_batch_dk_dk
from app01.models import BaseInfoWorkHour, PlanPlantBatch
from app01.views import depart, user, pretty, admin, account, task, order, chart, upload, city, worktype, baseinfo, \
    WorkHour, planplantbatch, productionwage, agriculturecost, Plant_batch, views, report, job_type_views, \
    daily_price_report_views
from app01.views.DailyPriceReport import get_price_trends, get_available_categories, get_price_trends_data
from app01.views.Plant_batch import export_plant_batches, Plant_batch_query
from app01.views.WorkHour import get_second_level_categories, get_second_level_jobs
from app01.views.auto_complete import vehicle_autocomplete
from app01.views.channel import channel_list, channel_add, channel_edit, channel_delete
from app01.views.daily_plan_report import daily_plan_rate

from app01.views.daily_price_report_views import daily_price_report
from app01.views.loss import loss_report_list, loss_report_add, loss_report_edit, loss_report_delete

from app01.views.month_plan import monthly_plan_list, monthly_plan_create, monthly_plan_edit, monthly_plan_delete
from app01.views.outbound import outbound_list, outbound_add, outbound_edit, outbound_delete
from app01.views.plan_completion_report import monthly_plan_rate, monthly_plan_download, plan_feedback
from app01.views.plant_batch_calendar import plant_batch_calendar_view
from app01.views.process_alert import process_alert_list, process_alert_create, process_alert_update, \
    process_alert_delete
from app01.views.process_alert_over import process_alert_overview
from app01.views.productionwage import get_primary_work_types, get_secondary_work_types, get_base_options, \
    get_Plant_batch_dk
from app01.views.sales import salesperson_list, salesperson_add, salesperson_edit, salesperson_delete
from app01.views.upload import upload_depreciation_excel, upload_expense_allocation, outbound_upload, \
    upload_sales_record
from app01.views.user import upload_userinfo_modal_form
from app01.views.views import create_expense_allocation, expense_allocation_list, expense_allocation_add, \
    expense_allocation_edit, expense_allocation_delete, depreciation_allocation_list, depreciation_allocation_add, \
    depreciation_allocation_edit, depreciation_allocation_delete,  \
    get_plant_batch_dk, loss_report_autocomplete, \
    add_sales_record, fetch_unique_second_level_categories, \
     get_sales_records, add_sale_form, sales_record_edit, sales_record_delete, sales_record_add, \
    plant_batch_summary, production_wage_summary, production_wage_second_level, production_wage_details, profit_summary, \
    daily_price_report_list, daily_price_report_edit, daily_price_report_delete, cost_alert_summary, cost_alert_feedback
from app01.views.views_daily_plan import daily_plan_list, daily_plan_create, daily_plan_edit, daily_plan_delete
from app01.views.vihicle import vehicle_list, vehicle_add, vehicle_edit, vehicle_delete
from app01.views.market import *
from app01.views.customer import *

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path('tt/', chart.tt),


    # 菜单第一部分
    # 部门管理路由
    path('depart/list/', depart.depart_list),  # 部门列表页面
    path('depart/add/', depart.depart_add),  # 新增部门页面
    path('depart/delete/', depart.depart_delete),  # 删除部门
    path('depart/<int:nid>/edit/', depart.depart_edit),  # 编辑部门，基于部门ID
    path('depart/multi/', depart.depart_multi),  # 批量上传部门信息

    # 用户管理路由
    path('user/list/', user.user_list),  # 显示用户列表页面
    path('user/model/form/add/', user.user_model_form_add),  # 添加新用户（使用ModelForm）
    path('user/<int:nid>/edit/', user.user_edit),  # 编辑指定用户信息（通过用户ID）
    path('user/<int:nid>/delete/', user.user_delete),  # 删除指定用户（通过用户ID）
    path('upload/UserInfo/', upload_userinfo_modal_form, name='upload_userinfo'),

    # 销售人员路由配置
    path('salesperson/list/', salesperson_list, name='salesperson_list'),  # 销售人员信息列表页面
    path('salesperson/add/', salesperson_add, name='salesperson_add'),  # 添加销售人员信息页面
    path('salesperson/<int:nid>/edit/', salesperson_edit, name='salesperson_edit'),  # 编辑销售人员信息页面
    path('salesperson/<int:nid>/delete/', salesperson_delete, name='salesperson_delete'),  # 删除销售人员信息功能

    # 工价管理
    path('WorkHour/list/', WorkHour.Hour_list),  # 工价列表视图
    path('WorkHour/add/', WorkHour.WorkHour_add),  # 添加新工种工价视图
    path('WorkHour/<int:nid>/edit/', WorkHour.work_hour_edit),  # 编辑指定工种工价视图
    path('WorkHour/<int:nid>/delete/', WorkHour.work_hour_delete),  # 删除指定工种工价视图
    path('upload/WorkHour/', upload.upload_workhour_modal_form),  # 工价批量上传视图

    # 计量对照管理
    path('order/list/', order.order_list),  # 计量对照列表页面
    path('order/add/', order.order_add),  # 添加新的计量对照条目
    path('order/delete/', order.order_delete),  # 删除计量对照条目
    path('order/detail/', order.order_detail),  # 获取指定ID的计量对照详细信息
    path('order/edit/', order.order_edit),  # 编辑计量对照条目

    # 车辆管理相关路由
    # 车辆列表页：显示所有车辆信息
    path('vehicle/list/', vehicle_list, name='vehicle_list'),  # 显示车辆列表，支持查询和分页
    # 新建车辆：跳转到车辆信息添加页面
    path('vehicle/add/', vehicle_add, name='vehicle_add'),  # 提供一个表单来添加新车辆
    # 编辑车辆：根据车辆ID编辑指定车辆信息
    path('vehicle/<int:nid>/edit/', vehicle_edit, name='vehicle_edit'),  # 根据车辆ID编辑车辆信息
    # 删除车辆：根据车辆ID删除指定的车辆
    path('vehicle/<int:nid>/delete/', vehicle_delete, name='vehicle_delete'),  # 根据车辆ID删除车辆信息

    # 月度计划
    path('PlanPlantBatch/list/', planplantbatch.planplantbatch_list),


    # 市场管理
    path('market/list/', market_list, name='market_list'),  # 显示市场信息列表
    path('market/add/', market_add, name='market_add'),  # 添加市场信息
    path('market/<int:nid>/edit/', market_edit, name='market_edit'),  # 编辑市场信息
    path('market/<int:nid>/delete/', market_delete, name='market_delete'),  # 删除市场信息


    # 客户管理相关的路径配置
    # 显示客户信息列表页面
    path('customer/list/', customer_list, name='customer_list'),
    # 添加新客户的页面
    path('customer/add/', customer_add, name='customer_add'),
    # 编辑现有客户信息的页面，基于客户ID
    path('customer/<int:nid>/edit/', customer_edit, name='customer_edit'),
    # 删除客户信息的操作路径，基于客户ID
    path('customer/<int:nid>/delete/', customer_delete, name='customer_delete'),


    # 菜单第二部分
    # 月度计划管理相关路径配置
    # 显示月度计划列表页面
    path('monthly_plan/', monthly_plan_list, name='monthly_plan_list'),
    # 创建新的月度计划的页面
    path('monthly_plan/add/', monthly_plan_create, name='monthly_plan_create'),
    # 编辑现有月度计划的页面，基于计划ID
    path('monthly_plan/edit/<int:pk>/', monthly_plan_edit, name='monthly_plan_edit'),
    # 删除月度计划的操作路径，基于计划ID
    path('monthly_plan/delete/<int:pk>/', monthly_plan_delete, name='monthly_plan_delete'),
    # 日度计划管理相关路径配置
    # 显示日度计划列表页面
    path('daily_plan/', daily_plan_list, name='daily_plan_list'),
    # 创建新的日度计划的页面
    path('daily_plan/add/', daily_plan_create, name='daily_plan_create'),
    # 编辑现有日度计划的页面，基于批次ID（字符串类型）
    path('daily_plan/<str:pk>/edit/', daily_plan_edit, name='daily_plan_edit'),
    # 删除日度计划的操作路径，基于批次ID（字符串类型）
    path('daily_plan/delete/<str:batch_id>/', daily_plan_delete, name='daily_plan_delete'),
    # 月度计划的额外功能路径配置
    # 显示月度计划达成率
    path('monthly_plan_rate/', monthly_plan_rate, name='monthly_plan_rate'),
    # 下载月度计划的功能
    path('monthly_plan/download/', monthly_plan_download, name='monthly_plan_download'),
    # 针对未达成的月度计划的反馈操作路径，基于计划ID
    path('monthly_plan/feedback/<int:plan_id>/', plan_feedback, name='feedback'),


    # 日度计划达成情况视图
    path('daily_plan_rate/', daily_plan_rate, name='daily_plan_rate'),




    # 菜单第三部分
    # 批次管理相关路径配置
    # 显示批次表列表页面
    path('Plant_batch/list/', Plant_batch.Plant_batch_list),
    path('Plant_batch/export/', export_plant_batches, name='export_plant_batches'),
    # 创建新的批次记录的页面
    path('Plant_batch/add/', Plant_batch.Plant_batch_add),
    # 编辑现有批次记录的页面，基于批次ID
    path('Plant_batch/<int:nid>/edit/', Plant_batch.Plant_batch_edit),
    # 删除批次记录的操作路径，基于批次ID
    path('Plant_batch/<int:nid>/delete/', Plant_batch.Plant_batch_delete),
    # 工价批量上传功能
    path('upload/Plant_batch/', upload.upload_Plant_batch_modal_form),
    # 日历视图显示种植批次
    path('Plant_batch/calendar/', plant_batch_calendar_view, name='plant_batch_calendar_view'),
    #批次查询
    path('Plant_batch_query/', Plant_batch_query, name='Plant_batch_query'),

    # 工种管理
    path('BaseInfoWorkType/list/', worktype.work_type_list),
    path('BaseInfoWorkType/add/', worktype.work_type_add),
    path('BaseInfoWorkType/<int:nid>/edit/', worktype.work_type_edit),
    path('BaseInfoWorkType/<int:nid>/delete/', worktype.work_type_delete),

    # 基地管理URL配置
    path('BaseInfo/list/', baseinfo.BaseInfo_list),  # 显示基地列表页面
    path('BaseInfo/add/', baseinfo.BaseInfo_add),  # 添加新的基地信息
    path('BaseInfo/<int:nid>/edit/', baseinfo.BaseInfo_edit),  # 编辑指定ID的基地信息
    path('BaseInfo/<int:nid>/delete/', baseinfo.BaseInfo_delete),  # 删除指定ID的基地信息

    # 工时管理
    path('production_wage_list/list/', productionwage.production_wage_list),
    path('productionwate/add/undefined/', productionwage.production_wage_list),
    path('productionwate/add/', productionwage.production_wage_add),
    path('productionwate/<int:nid>/delete/', productionwage.production_wage_delete),
    path('productionwate/<int:nid>/edit/', productionwage.productionwate_edit),
    path('upload/productionwate/', upload.upload_productionwate_modal_form),  # 工时批量上传
    path('get_productionwate/', productionwage.get_productionwate),  # ajax获得价格和类型
    path('get_base_options/', get_base_options, name='get_base_options'),  # h 获得基地
    path('get_productionwate_price/', productionwage.get_productionwate_price),  # ajax获得价格和类型
    path('get_Plant_batch_dk/', productionwage.get_Plant_batch_dk),  # ajax获得地块
    path('get_primary_work_types/', get_primary_work_types, name='get_primary_work_types'),  # 获得一级工种
    path('get_secondary_work_types/', get_secondary_work_types, name='get_secondary_work_types'),  # 获得二级工种

    # 功能性路由
    # 获取二级分类和工种的 Ajax 请求 URL
    path('get_second_level_categories/', get_second_level_categories,
         name='get_second_level_categories'),
    path('get_second_level_jobs/', get_second_level_jobs, name='get_second_level_jobs'),

    # 农资管理
    path('Agricureture/list/', agriculturecost.agriculture_cost_list),
    path('Agricureture/add/', agriculturecost.agriculture_cost_add),
    path('Agricureture/<int:nid>/edit/', agriculturecost.agriculture_cost_edit),
    path('Agricureture/<int:nid>/delete/', agriculturecost.agriculture_cost_delete),
    path('upload/agriculturecost/', upload.upload_agriculturecost_modal_form),  # 工价批量上传


    # 实现自动补全功能
    path('employee_autocomplete/', views.employee_autocomplete, name='employee_autocomplete'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('autocomplete_baseinfo/', views.autocomplete_baseinfo, name='autocomplete_baseinfo'),
    path('test/', views.add_multiple_work_hours),

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
    path('login/', account.login, name='login'),
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
    path('report_salary_temp_by_daily/get_tables_date/', report.report_salary_temp_by_daily_data_table_view,
         name="report_salary_temp_by_daily"),
    # 工资花名册
    path('report_salary_by_plople/list/', report.report_salary_by_plople),
    path('report_salary_by_plople/get_tables_date/', report.report_salary_by_plople_data_table_view,
         name="report_salary_by_plople"),  # 获取工资花名册
    # 每日工资表
    path('report_salary_by_daily/list/', report.report_salary_by_daily),  # 每日工资表
    path('report_salary_by_daily/get_tables_date/', report.report_salary_by_daily_data_table_view,
         name="report_salary_by_daily"),
    # 每日工时
    path('report_workhour_by_daily/list/', report.report_workhour_by_daily),  # 每日工时
    path('report_workhour_by_daily/get_tables_date/', report.report_workhour_by_daily_data_table_view,
         name="report_workhour_by_daily"),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.highcharts),

    # 上传文件
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    # path('upload/modal/form/', upload.upload_modal_form),

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
    path('depreciation_allocation/<int:nid>/delete/', depreciation_allocation_delete,
         name='depreciation_allocation_delete'),
    # 报损
    path('loss_report/list/', loss_report_list, name='loss_report_list'),
    path('loss_report/add/', loss_report_add, name='loss_report_add'),
    path('loss_report/<int:nid>/edit/', loss_report_edit, name='loss_report_edit'),
    path('loss_report/<int:nid>/delete/', loss_report_delete, name='loss_report_delete'),
    path('loss_report_autocomplete/', loss_report_autocomplete, name='loss_report_autocomplete'),
    path('get_plant_batch_dk/', get_plant_batch_dk, name='get_plant_batch_dk'),

    # 出库
    path('outbound/list/', outbound_list, name='outbound_list'),
    path('outbound/add/', outbound_add, name='outbound_add'),
    path('outbound/edit/<int:nid>/', outbound_edit, name='outbound_edit'),
    path('outbound/delete/<int:nid>/', outbound_delete, name='outbound_delete'),
    path('upload/outbound/', outbound_upload, name='outbound_upload'),
    path('get_sales_records/', get_sales_records, name='get_sales_records'),
    path('add_sale_form/', add_sale_form, name='add_sale_form'),
    path('fetch_unique_second_level_categories/', fetch_unique_second_level_categories, name='fetch_unique_second_level_categories'),
    path('sales_record/add/<int:outbound_id>/', sales_record_add, name='sales_record_add'),
    path('sales_record/edit/<int:pk>/', sales_record_edit, name='sales_record_edit'),
    path('sales_record/delete/<int:pk>/', sales_record_delete, name='sales_record_delete'),
    path('ajax/customer_autocomplete/', views.customer_autocomplete, name='customer_autocomplete'),

    # 单独管理销售记录的URL
    path('sales_record/management/list/', views.sales_record_management_list, name='sales_record_management_list'),
    path('sales_record/management/add/', views.sales_record_management_add, name='sales_record_management_add'),
    path('sales_record/management/<int:pk>/edit/', views.sales_record_management_edit,
         name='sales_record_management_edit'),
    path('sales_record/management/<int:pk>/delete/', views.sales_record_management_delete,
         name='sales_record_management_delete'),
    path('upload/sales_record/', upload_sales_record, name='upload_sales_record'),


    # 显示计划内成本汇总
    path('plant_batch_summary/', plant_batch_summary, name='plant_batch_summary'),
    path('get_batch_details/', views.get_batch_details, name='get_batch_details'),

    # 工价汇总
    path('production_wage_summary/', production_wage_summary, name='production_wage_summary'),
    path('production_wage_second_level/', production_wage_second_level, name='production_wage_second_level'),
    path('production_wage_details/', production_wage_details, name='production_wage_details'),

    # 折旧分摊表
    path('expense_allocation/list/', expense_allocation_list, name='expense_allocation_list'),
    path('expense_allocation/add/', expense_allocation_add, name='expense_allocation_add'),
    path('expense_allocation/<int:nid>/edit/', expense_allocation_edit, name='expense_allocation_edit'),
    path('expense_allocation/<int:nid>/delete/', expense_allocation_delete, name='expense_allocation_delete'),
    path('upload/expense_allocation/', upload_expense_allocation, name='upload_expense_allocation'),

    # 利润
    path('profit_summary/', profit_summary, name='profit_summary_list'),

    path('mobile_login/', mobile_login, name='mobile_login'),
    path('mobile/home/', mobile_home, name='mobile_home'),
    path('mobile/logout/', mobile_logout, name='mobile_logout'),
    # 手机端工价录入
    path('mobile/gongshiluru/', mobile_gongshiluru, name='mobile_gongshiluru'),
    # 手机端出库录入
    path('mobile/outbound/add/', mobile_outbound_add, name='mobile_outbound_add'),
    path('autocomplete/customer/', customer_autocomplete, name='customer_autocomplete'),
    path('autocomplete/worker/', worker_autocomplete, name='worker_autocomplete'),
    path('autocomplete/batch/', batch_autocomplete, name='batch_autocomplete'),

    # 分类相关的 URL 路由
    path('job_category/list/', views.job_category_list, name='job_category_list'),
    path('job_category/add/', views.job_category_add, name='job_category_add'),
    path('job_category/<int:pk>/edit/', views.job_category_edit, name='job_category_edit'),

    # 工种相关的 URL 路由
    path('job_type/list/', job_type_views.job_type_list, name='job_type_list'),
    path('job_type/add/', job_type_views.job_type_add, name='job_type_add'),
    path('job_type/<int:pk>/edit/', job_type_views.job_type_edit, name='job_type_edit'),
    path('job_type/<int:pk>/delete/', job_type_views.job_type_delete, name='job_type_delete'),
    # 根据二级分类获取父工种

    # 每日价格录入相关的 URL 路由
    path('daily_price_report/add/', daily_price_report, name='daily_price_report_add'),
    path('daily_price_report/list/', daily_price_report_list, name='daily_price_report_list'),
    path('daily_price_report/<int:pk>/edit/', daily_price_report_edit, name='daily_price_report_edit'),
    path('daily_price_report/<int:pk>/delete/', daily_price_report_delete, name='daily_price_report_delete'),





    # 费用超支
    path('cost_alert/', cost_alert_summary, name='cost_alert_summary'),
    path('cost_alert_feedback/', cost_alert_feedback, name='cost_alert_feedback'),
    path('fetch_cost_details/', views.fetch_cost_details, name='fetch_cost_details'),

    # 流程维护
    path('process_alerts/', process_alert_list, name='process_alert_list'),
    path('process_alerts/create/', process_alert_create, name='process_alert_create'),
    path('process_alerts/update/<int:pk>/', process_alert_update, name='process_alert_update'),
    path('process_alerts/delete/<int:pk>/', process_alert_delete, name='process_alert_delete'),

    # 流程预警
    path('process_alerts/overview/', process_alert_overview, name='process_alert_overview'),

    # 价格走势
    path('price_trends/', get_price_trends, name='price_trends'),
    path('api/price_trends_data/', get_price_trends_data, name='price_trends_data'),  # 新增的数据接口
    path('api/available_categories/', get_available_categories, name='available_categories'),

    # 报价渠道管理
    path('channel/list/', channel_list, name='channel_list'),  # 显示报价渠道信息列表
    path('channel/add/', channel_add, name='channel_add'),  # 添加报价渠道信息
    path('channel/<int:nid>/edit/', channel_edit, name='channel_edit'),  # 编辑报价渠道信息
    path('channel/<int:nid>/delete/', channel_delete, name='channel_delete'),  # 删除报价渠道信息


    #自动补全
    path('ajax/vehicle-autocomplete/', vehicle_autocomplete, name='vehicle_autocomplete'),
    path('ajax/get_Plant_batch_dk/', get_Plant_batch_dk, name='get_Plant_batch_dk'),
    path('ajax/batch_autocomplete/', batch_autocomplete, name='batch_autocomplete'),
    path('ajax/customer_autocomplete/', customer_autocomplete, name='customer_autocomplete'),
    path('ajax/worker_autocomplete/', worker_autocomplete, name='worker_autocomplete'),
    path('ajax/vehicle_autocomplete/', vehicle_autocomplete, name='vehicle_autocomplete'),

    path('ajax/batch_autocomplete_pc/', batch_autocomplete_pc, name='batch_autocomplete_pc'),
    path('ajax/get_Plant_batch_dk_dk/', get_Plant_batch_dk_dk, name='get_Plant_batch_dk_kd'),



]
from django.conf.urls.static import static
# 添加媒体文件的URL配置
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
