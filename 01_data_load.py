import pandas as pd
import json

# 读取申报明细表（主表 financial_facts.csv）
df_filings = pd.read_csv("financial_facts.csv")
print("✅申报总条数：", len(df_filings))
print("✅字段列表：", df_filings.columns.tolist())
print("\n📋前3行预览：")
print(df_filings.head(3))

#读取公司基础信息 json
with open("company_profile.json", "r", encoding="utf-8") as f:
    profile = json.load(f)

print("\n🏢苹果公司基础信息")
print(f"公司名称：{profile['entityName']}")
print(f"股票代码：{profile['ticker']}")
print(f"行业编码&描述：{profile['sic']} | {profile['sicDescription']}")
