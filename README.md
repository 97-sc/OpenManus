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
- 多期同比分析（YoY，按中国股市习惯涨红跌绿标色）

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

对 examples/tesco_fy2024_sample.xlsx 运行 FinancialReportTool 得到的分析报告（节选）：

```markdown
# 财报分析报告

**分析期间**：2024, 2023, 2022
**分析类型**：full

## 关键财务比率

| 指标 | 2024 | 2023 | 同比 |
|------|------|------|------|
| 毛利率 | 30.00% | 28.50% | +1.50pp |
| 净利率 | 10.00% | 8.20% | +1.80pp |
| ROE | 16.67% | 14.50% | +2.17pp |
| ROA | 6.67% | 5.80% | +0.87pp |
| 资产负债率 | 60.00% | 62.00% | -2.00pp |
| 流动比率 | 1.50 | 1.45 | +0.05 |
| 速动比率 | 1.12 | 1.05 | +0.07 |
```

## 效果展示

- 智能体可自主识别 Excel 表头、按期间分组
- 自动计算 7 项核心财务比率
- 多期同比分析（YoY），按中国股市习惯标红/标绿
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
- 二次开发提交：3 次 feat 提交，新增 5 个文件，247+ 行代码
- 许可证：沿用上游 MIT License
