import json

input_file = 'final_clean_data_cleaned.json'
output_file = '1.json'

# 读取 JSON 文件
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 排除视图相关的记录
exclude_models = [
    'app01.salary_by_plople',
    'app01.salary_by_daily',
    'views_工资花名册',
    'views_每日工资表'
]

filtered_data = [entry for entry in data if entry.get('model') not in exclude_models]

# 保存过滤后的数据
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"已成功删除视图相关数据，并保存到 {output_file}")