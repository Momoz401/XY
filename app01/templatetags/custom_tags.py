# your_app/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def to_range(start, end):
    """
    将开始和结束数字转换为范围列表
    用于在模板中生成循环范围，例如月份1到12
    """
    try:
        start = int(start)
        end = int(end)
        return range(start, end + 1)
    except (ValueError, TypeError):
        return []


