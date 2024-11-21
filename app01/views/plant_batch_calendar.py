from django.shortcuts import render
from app01.models import Plant_batch, JobCategoryInfo, JobTypeDetailInfo
from django.db.models import Min, Max

def plant_batch_calendar_view(request):
    # 获取筛选条件
    second_category_filter = request.GET.get('二级分类', None)
    batch_id_filter = request.GET.get('批次ID', None)

    # 构建筛选条件
    filters = {}
    if second_category_filter:
        filters['二级分类'] = second_category_filter
    if batch_id_filter:
        filters['批次ID__icontains'] = batch_id_filter  # 使用模糊查询批次ID

    # 获取符合筛选条件的批次记录
    plant_batches = Plant_batch.objects.filter(**filters).values(
        '批次ID', '二级分类', '移栽开始时间', '点籽日期', '采收初期', '采收末期',
        '打地开始时间', '清棚开始时间', '间菜开始时间', '施肥开始时间', '吹生菜开始时间', '除草开始时间'
    )

    # 获取所有二级分类
    job_categories = JobCategoryInfo.objects.filter(category_level=2)

    # 获取所有一级工种信息，并记录每个工种的最早时间
    job_types = JobTypeDetailInfo.objects.all()

    # 创建事件列表
    events = []
    for batch in plant_batches:
        for job_type in job_types:
            # 获取一级工种的名称
            work_name = job_type.job_name  # 例如 "采收"
            time_field = get_time_field(work_name)

            # 查找每个批次对应的工种时间，并记录最早时间
            if batch.get(time_field):
                events.append({
                    'title': f"{work_name}: {batch['批次ID']}",
                    'start': batch[time_field].strftime('%Y-%m-%d'),
                    'color': get_work_color(work_name),  # 设置不同颜色
                    'work_name': work_name,
                    'batch_id': batch['批次ID'],
                })

    context = {
        'events': events,
        'job_categories': job_categories,
        'work_colors': get_work_colors(),  # 传递工种与颜色的映射
    }

    return render(request, 'plant_batch_calendar.html', context)


# 返回工种对应的时间字段
def get_time_field(work_name):
    work_time_fields = {
        '采收': '采收初期',
        '点籽': '点籽日期',
        '打地': '打地开始时间',
        '清棚': '清棚开始时间',
        '间菜': '间菜开始时间',
        '施肥': '施肥开始时间',
        '吹生菜': '吹生菜开始时间',
        '除草': '除草开始时间',
        '移栽': '移栽开始时间',
    }
    return work_time_fields.get(work_name, None)


# 根据工种类型返回颜色
def get_work_color(work_name):
    colors = {
        '移栽': 'green',
        '点籽': 'blue',
        '采收': 'orange',
        '施肥': 'yellow',
        '打地': 'brown',
        '清棚': 'purple',
        '间菜': 'pink',
        '吹生菜': 'red',
        '除草': 'limegreen',
    }
    return colors.get(work_name, 'gray')


# 获取工种与颜色的映射
def get_work_colors():
    return {
        '移栽': 'green',
        '点籽': 'blue',
        '采收': 'orange',
        '施肥': 'yellow',
        '打地': 'brown',
        '清棚': 'purple',
        '间菜': 'pink',
        '吹生菜': 'red',
        '除草': 'limegreen',
    }
