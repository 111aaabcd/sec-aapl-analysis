import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/sec_analysis?charset=utf8mb4')

# 校验总记录数
sql = "SELECT COUNT(*) AS total FROM aapl_financial_facts;"
total = pd.read_sql(sql, engine).iloc[0, 0]
print(f"✅ 表内总记录数：{total}")
