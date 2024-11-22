import random
from datetime import datetime, timedelta

# 设置初始日期
start_date = datetime(2024, 10, 10)

# 定义市场 ID 和品种 ID
market_ids = range(2, 8)  # 市场 ID 从 2 到 7
variety_id = 3  # 品种 ID 固定为 3

# 定义随机数范围
price_min = 1  # 最低价格
price_max = 100  # 最高价格

# 设置天数
days = 100

# 生成 SQL 插入语句
values = []
for i in range(days):
    current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    for market_id in market_ids:
        price = round(random.uniform(price_min, price_max), 2)  # 生成随机价格
        values.append(f"('{current_date}', {variety_id}, {market_id}, {price})")

# 拼接 SQL
sql = "INSERT INTO app01_dailypricereport (日期, 品种_id, 市场_id, 价格) VALUES\n" + ",\n".join(values) + ";"

# 保存到文件或打印
with open('insert_daily_price_report.sql', 'w', encoding='utf-8') as file:
    file.write(sql)

print("SQL 插入语句已生成并保存到 'insert_daily_price_report.sql'")
