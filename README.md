# Apple SEC Financial Facts Analysis

## 项目简介

本项目基于美国 SEC 官方 API 中 Apple Inc. (AAPL) 的 XBRL companyfacts 与 submissions 数据，整理财务事实数据和申报元数据，并通过 Python / CSV / MySQL 完成数据读取、清洗、入库和基础查询分析。

数据来源：

- `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json`
- `https://data.sec.gov/submissions/CIK0000320193.json`

当前数据文件包含 25,135 条 financial facts observations 和 1,001 条 filings metadata。数据保留 SEC accession number、form、filed date、period、unit、XBRL concept 等字段。该项目分析的是 SEC 基本面与申报数据，不包含日频股票 OHLCV 行情。

## 流程梳理

1. `01_data_load.py`：读取 `financial_facts.csv` 和 `company_profile.json`，预览字段与公司基础信息。
2. `02_data_clean.py`：保留核心分析字段，标准化日期与数值类型，去除关键字段空值和重复行，输出 `aapl_filings_clean.csv`。
3. `03_import_mysql.py`：使用环境变量连接 MySQL，自动创建数据库并导入清洗后的数据表。
4. `04_query_analysis.py`：校验表内记录数，按 filing form 汇总，并查询近期收入类 USD 观测值。

## 文件说明

| 文件名 | 说明 |
| :--- | :--- |
| `financial_facts.csv` | SEC companyfacts 展开的财务事实数据 |
| `filings.csv` | SEC submissions 申报元数据 |
| `company_profile.json` | Apple 公司基础信息 |
| `data_dictionary.csv` | 字段说明 |
| `01_data_load.py` | 数据读取与字段预览 |
| `02_data_clean.py` | 数据清洗脚本 |
| `03_import_mysql.py` | MySQL 入库脚本 |
| `04_query_analysis.py` | MySQL 查询分析脚本 |
| `requirements.txt` | Python 依赖 |

## 运行方式

安装依赖：

```bash
pip install -r requirements.txt
```

读取与清洗：

```bash
python 01_data_load.py
python 02_data_clean.py
```

如需导入 MySQL，先设置连接信息。示例：

```bash
set MYSQL_USER=root
set MYSQL_PASSWORD=your_password
set MYSQL_HOST=127.0.0.1
set MYSQL_PORT=3306
set MYSQL_DB=sec_analysis
```

然后运行：

```bash
python 03_import_mysql.py
python 04_query_analysis.py
```

## 已修正的问题

- 修复 `02_data_clean.py` 引用不存在的 `reportDate` / `filingDate` 字段导致脚本报错的问题。
- 将 MySQL 连接信息从硬编码账号密码改为环境变量，避免仓库暴露本机密码。
- 增加文件存在性、关键字段和数据库名校验，减少静默失败。

## 简历表述建议

可写为：基于 SEC 官方 Apple XBRL 数据，完成财务事实 CSV 读取、字段清洗、MySQL 入库与基础 SQL 查询，保留 accession number、申报类型、申报日期、期间、单位和 XBRL concept，用于公司基本面数据分析练习。

## 可核实性说明

当前仓库可核实的是 Python / CSV / MySQL 数据处理流程。若简历中需要写 AI 辅助实践，建议补充真实使用过的 AI 工具、提示词、代码修改记录或提交说明后再写入。
