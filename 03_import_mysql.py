import pandas as pd
from sqlalchemy import create_engine, text

# ========== 修改为你本地MySQL的连接信息 ==========
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DB = "sec_analysis"
# ==============================================

# 1. 连接MySQL并自动创建数据库
engine_root = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}")
with engine_root.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} DEFAULT CHARACTER SET utf8mb4"))
print(f"✅ 数据库 {MYSQL_DB} 已就绪")

# 2. 连接到目标数据库
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

# 3. 读取清洗后的CSV
df = pd.read_csv("aapl_filings_clean.csv", parse_dates=["filed", "start", "end"])

# 4. 批量写入MySQL数据表
table_name = "aapl_financial_facts"
df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print(f"✅ 数据导入完成，表名：{table_name}")
print(f"✅ 共成功导入 {len(df)} 条记录")
