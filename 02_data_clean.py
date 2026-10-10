import pandas as pd

# 1. 读取原始数据
df = pd.read_csv("financial_facts.csv")
print(f"原始数据行数：{len(df)}")

# 2. 保留核心分析字段，去掉冗余描述字段
keep_cols = [
    "concept", "unit", "value",
    "accn", "form", "filed",
    "fy", "fp", "start", "end", "frame"
]
df = df[keep_cols]

# 3. 日期字段标准化
df["filed"] = pd.to_datetime(df["filed"], errors="coerce")
df["start"] = pd.to_datetime(df["start"], errors="coerce")
df["end"] = pd.to_datetime(df["end"], errors="coerce")

# 4. 去除空值与重复行
df = df.dropna(subset=["value", "filed"])
df = df.drop_duplicates()
df['reportDate'] = df['reportDate'].fillna(df['filingDate'])

# 5. 数值字段类型转换
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df["fy"] = df["fy"].astype("Int64")

print(f"清洗后数据行数：{len(df)}")
print(f"字段：{df.columns.tolist()}")
print("\n清洗后前3行：")
print(df.head(3))

# 6. 输出清洗后的文件
df.to_csv("aapl_filings_clean.csv", index=False, encoding="utf-8-sig")
print("\n✅ 清洗完成，已输出：aapl_filings_clean.csv")
