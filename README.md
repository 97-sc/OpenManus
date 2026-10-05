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

在 `app/prompt/manus.py` 的系统提示词中加入语言约束，要求智能体始终使用简体中文交流（包括思考过程、工具调用说明、中间结果与最终回答），降低中文用户的理解成本。

### 2. Gradio Web UI（可视化方向）

基于 Gradio 4.31.0 + starlette 0.40.0 搭建浏览器可视化界面（`web_ui.py`），支持：

- 自然语言输入任务，在浏览器中直接与 Manus 智能体交互
- 复用框架默认的上下文管理，保留多轮对话历史

> **实现说明**：当前 Web UI 是「一次执行、一次返回」——`ChatInterface` 的回调里 `await agent.run(message)` 等智能体完整跑完后一次性返回结果，**尚未接入流式输出**，因此界面上看不到逐步的 Action / Observation 轨迹。流式输出与执行过程可视化是后续计划。

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
- 数据处理：openpyxl（xlsx 读写）
- 报告输出：Markdown 文本（由工具直接返回给智能体）

## 快速开始

### 1. 克隆与虚拟环境

```bash
git clone https://github.com/97-sc/OpenManus.git
cd OpenManus
python -m venv venv
source venv/Scripts/activate   # Git Bash 环境
pip install -r requirements.txt
```

> **环境复现说明**
>
> 上面的命令装好的是**命令行 Agent 所需的主干依赖**，可直接跑 `python main.py`。
>
> Web UI 的依赖**不在** `requirements.txt` 里，因为它与主干存在真实冲突（详见
> [已知局限](#已知局限)）。需要 Web UI 时单独安装：
>
> ```bash
> pip install -r requirements-webui.txt
> ```
>
> 开发本机环境的实际状态：Python 3.13 + venv，`pip check` 会报告 8 条版本告警，
> 其中以下几条是**预期的、已知的**（为让 gradio 4.31.0 可用而降级所致）：
>
> | 包 | 装到的版本 | 上游要求 | 说明 |
> |---|---|---|---|
> | starlette | 0.40.0 | fastapi 0.141.1 要求 ≥0.46.0 | 降级换取 gradio 4.31.0 可用 |
> | anyio | 4.4.0 | mcp 1.5.0 要求 ≥4.5 | 同上 |
> | pydantic | 2.13.5 | 本仓库固定 `~=2.10.6` | 实际按较新版本安装 |
> | pydantic_core | 2.46.5 | 本仓库固定 `~=2.27.2` | 同上 |
>
> 换句话说：**本仓库能跑通，但依赖并非完全自洽**，`requirements.txt` 里的版本号
> 与实际环境存在偏差。根因与改进方向见 [已知局限](#已知局限)。

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

Web UI 依赖不在主 `requirements.txt` 中，需先安装：

```bash
pip install -r requirements-webui.txt
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

FinancialReportTool 注册后，它的 `name` 与 `description` 会随其他工具一起进入模型的可用工具清单。因此用户只需用自然语言提出需求（如"分析 examples/tesco_fy2024_sample.xlsx 的财报"），智能体即可根据工具描述判断该不该调、参数怎么填，无需人工指定工具名称。完整调用链路：

```mermaid
flowchart LR
    A[用户输入自然语言<br/>分析财报] --> B[Manus 智能体<br/>理解意图]
    B --> C[自主决策<br/>选用 financial_report 工具]
    C --> D[FinancialReportTool<br/>读取 Excel 并计算]
    D --> E[输出 Markdown 报告<br/>7 项比率 + 同比分析]
```

- 工具按约定解析表格：取 `wb.active` 活动表，首行为期数、首列为科目名，其余为数值
- 智能体自主判断是否调用该工具，并组装 `file_path` / `periods` / `analysis_type` 参数
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
├── requirements-webui.txt      # 新增：Web UI 可选依赖（与主干有已知冲突，见下）
├── test_financial_tool.py      # 新增：工具测试脚本
├── generate_sample_report.py   # 新增：样例报告生成脚本
└── README.md           # 本文件
```

## 已知局限

- **Web UI 未接入流式输出**：见上文实现说明，界面需等智能体完整跑完才出结果，看不到中间的执行轨迹。
- **财报工具依赖固定表结构**：只读默认活动表（`wb.active`），且科目名硬编码为「营业收入 / 营业成本 / 净利润 / 总资产 / 总负债 / 股东权益 / 流动资产 / 流动负债 / 存货」。企业报表若使用「主营业务收入」等其他叫法或英文科目名，对应数值会取到 0 且不报错（静默失败）。后续需补同义词映射或模糊匹配。
- **仅支持 .xlsx / .xlsm**：不支持 PDF 年报，而真实企业财报多为 PDF。
- **Web UI 依赖与主干存在真实冲突**：Gradio 相关依赖不在 `requirements.txt` 中，需单独安装 `requirements-webui.txt`。冲突根因是 **gradio 4.31.0 版本过旧**（2024-06 发布），其依赖链要求较旧的 starlette / anyio，与主干要求的 `fastapi → starlette ≥0.46`、`mcp 1.5.0 → anyio ≥4.5` 直接矛盾。本项目的处理方式是**显式降级这两个包、换取 Web UI 可启动**，代价是主干依赖不再完全自洽（安装后 `pip check` 会报告冲突，属预期内，对照表见「快速开始」）。更彻底的方案是把 gradio 升到 4.44.x / 5.x 以解除冲突，但需同步改造 `web_ui.py` 的 `ChatInterface` 调用方式，属独立改动，尚未实施。
- **依赖未锁定为可复现状态**：当前 venv 是手工调平的结果，`pydantic`（实装 2.13.5 / 约束 `~=2.10.6`）、`pydantic_core`（实装 2.46.5 / 约束 `~=2.27.2`）、`fastapi`（实装 0.141.1 / 约束 `~=0.115.11`）均与 `requirements.txt` 不符。如需严格复现，应另行导出 lock 文件。
- **未建评测集**：工具与提示词的验证均基于少量样例手工核对。

## 开源信息

- GitHub：https://github.com/97-sc/OpenManus
- 上游：https://github.com/FoundationAgents/OpenManus
- 二次开发提交：8 次（3 次 feat 功能、1 次 fix 依赖、3 次 docs 文档、1 次 chore 清理），新增文件 5 个，新增代码 270+ 行
- 许可证：沿用上游 MIT License
