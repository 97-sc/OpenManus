# OpenManus 二次开发：本地化 AI 智能体财报分析系统

> 基于 [FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus) 的二次开发项目
> 在保留原框架核心能力的基础上，新增简体中文提示词、可视化 Web UI、自动化财报分析工具三大能力

## 项目简介

OpenManus 是 FoundationAgents 开源的通用 AI 智能体框架。本项目在其基础上做二次开发，重点解决三个问题：

- 英文提示词对中文用户不友好
- 命令行交互缺乏可视化界面
- 没有针对垂直领域（财报分析）的开箱即用工具

## 二次开发内容

### 1. 简体中文提示词（汉化方向）

将系统提示词与默认示例全部汉化，降低中文用户理解成本，输出更贴近本地化表达习惯。

### 2. Gradio Web UI（可视化方向）

基于 Gradio 4.31.0 + starlette 0.40.0 搭建浏览器可视化界面，支持：

- 自然语言输入任务
- 实时查看智能体思考过程
- 工具调用轨迹可视化

### 3. FinancialReportTool（核心工具 - 财报分析方向）

新增 `app/tool/financial_report.py`，针对零售/制造类企业财报自动计算：

- 盈利能力：毛利率、净利率、ROE、ROA
- 偿债能力：资产负债率、流动比率、速动比率
- 多期同比分析（YoY，按中国股市习惯用 📈/📉 标注涨跌）

## 技术栈

- 语言：Python 3.13
- 框架：OpenManus（基于 ReAct 智能体架构）
- LLM：Ollama 本地推理（qwen2.5:7b）
- Web UI：Gradio 4.31.0 + starlette 0.40.0
- 数据处理：openpyxl（xlsx 读写）、pandas（数据清洗）
- 报告生成：reportlab（PDF 输出）

## 快速开始

### 1. 克隆与虚拟环境

```bash
git clone https://github.com/97-sc/OpenManus.git
cd OpenManus
python -m venv venv
source venv/Scripts/activate   # Git Bash 环境
pip install -r requirements.txt
```

### 2. 配置 LLM

复制 `config/config.example.toml` 为 `config/config.toml`，填入 Ollama 地址：

```toml
[llm]
model = "qwen2.5:7b"
base_url = "http://localhost:11434/v1"
api_key = "ollama"
```

> 注：config/config.toml 已在 .gitignore 中，不会上传到 GitHub

### 3. 启动 Web UI

```bash
python web_ui.py
```

浏览器访问 http://127.0.0.1:7860

### 4. 直接测试财报分析工具（无需启动智能体）

```bash
python test_financial_tool.py
```

## 示例报告（真实输出）

对 examples/tesco_fy2024_sample.xlsx 运行 FinancialReportTool 得到的完整分析报告：

```markdown
# 财报分析报告

**分析期间**：2024, 2023, 2022
**分析类型**：full

## 一、原始数据（单位：万元）

| 科目 | 2024 | 2023 | 2022 |
|---|---|---|---|
| 营业收入 | 1000000.00 | 900000.00 | 800000.00 |
| 营业成本 | 700000.00 | 650000.00 | 600000.00 |
| 净利润 | 100000.00 | 80000.00 | 60000.00 |
| 总资产 | 1500000.00 | 1300000.00 | 1200000.00 |
| 总负债 | 900000.00 | 800000.00 | 750000.00 |
| 股东权益 | 600000.00 | 500000.00 | 450000.00 |
| 流动资产 | 600000.00 | 550000.00 | 500000.00 |
| 流动负债 | 400000.00 | 380000.00 | 350000.00 |
| 存货 | 150000.00 | 140000.00 | 130000.00 |

## 二、核心财务比率

| 比率 | 2024 | 2023 | 2022 |
|---|---|---|---|
| 毛利率(%) | 30.00 | 27.78 | 25.00 |
| 净利率(%) | 10.00 | 8.89 | 7.50 |
| ROE(%) | 16.67 | 16.00 | 13.33 |
| ROA(%) | 6.67 | 6.15 | 5.00 |
| 资产负债率(%) | 60.00 | 61.54 | 62.50 |
| 流动比率 | 1.50 | 1.45 | 1.43 |
| 速动比率 | 1.12 | 1.08 | 1.06 |

## 三、同比分析

### 2024 → 2023
- 📉 毛利率(%): 30.00 → 27.78（-2.22）
- 📉 净利率(%): 10.00 → 8.89（-1.11）
- 📉 ROE(%): 16.67 → 16.00（-0.67）
- 📉 ROA(%): 6.67 → 6.15（-0.51）
- 📈 资产负债率(%): 60.00 → 61.54（+1.54）
- 📉 流动比率: 1.50 → 1.45（-0.05）
- 📉 速动比率: 1.12 → 1.08（-0.05）

### 2023 → 2022
- 📉 毛利率(%): 27.78 → 25.00（-2.78）
- 📉 净利率(%): 8.89 → 7.50（-1.39）
- 📉 ROE(%): 16.00 → 13.33（-2.67）
- 📉 ROA(%): 6.15 → 5.00（-1.15）
- 📈 资产负债率(%): 61.54 → 62.50（+0.96）
- 📉 流动比率: 1.45 → 1.43（-0.02）
- 📉 速动比率: 1.08 → 1.06（-0.02）
```

## 效果展示

### 智能体自动调用 FinancialReportTool

用户只需用自然语言提出需求（如"分析 examples/tesco_fy2024_sample.xlsx 的财报"），Manus 智能体即**自主识别意图、决策并调用** FinancialReportTool，无需人工指定工具名称。完整调用链路：

```mermaid
flowchart LR
    A[用户输入自然语言<br/>分析财报] --> B[Manus 智能体<br/>理解意图]
    B --> C[自主决策<br/>选用 financial_report 工具]
    C --> D[FinancialReportTool<br/>读取 Excel 并计算]
    D --> E[输出 Markdown 报告<br/>7 项比率 + 同比分析]
```

- 智能体可自主识别 Excel 表头、按期间分组
- 自动计算 7 项核心财务比率
- 多期同比分析（YoY），按中国股市习惯用 📈/📉 标注涨跌
- 输出 Markdown 结构化报告，可直接粘贴到周报/年报

## 项目结构

```
OpenManus/
├── app/
│   ├── agent/          # 智能体核心逻辑
│   ├── tool/           # 工具集
│   │   └── financial_report.py   # 新增：财报分析工具
│   └── prompt/         # 提示词（已汉化）
├── config/             # 配置文件（config.toml 已 gitignore）
├── examples/           # 示例数据（含 tesco_fy2024_sample.xlsx）
├── web_ui.py           # 新增：Gradio Web UI 入口
├── test_financial_tool.py  # 新增：工具测试脚本
└── README.md           # 本文件
```

## 开源信息

- GitHub：https://github.com/97-sc/OpenManus
- 上游：https://github.com/FoundationAgents/OpenManus
- 二次开发提交：5 次提交（3 次 feat 功能 + 1 次 docs 文档 + 1 次 chore 清理），新增文件 5+ 个，代码 247+ 行
- 许可证：沿用上游 MIT License
