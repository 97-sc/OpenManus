import json
from pathlib import Path
from typing import Dict, List, Optional

import openpyxl

from app.tool.base import BaseTool


class FinancialReportTool(BaseTool):
    """财报分析工具：读取 Excel 财报数据，计算核心财务比率，生成结构化分析报告。"""

    name: str = "financial_report"
    description: str = (
        "读取 Excel 财报数据（.xlsx 文件），计算核心财务比率"
        "（毛利率、净利率、ROE、ROA、资产负债率、流动比率、速动比率），"
        "并生成 Markdown 格式的财务分析报告，支持多期对比。"
    )

    parameters: dict = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Excel 财报文件的绝对路径，例如 D:\\\\reports\\\\tesco_fy2024.xlsx",
            },
            "periods": {
                "type": "array",
                "items": {"type": "string"},
                "description": "要分析的期数列表，例如 ['2024', '2023']，留空则分析所有期数",
            },
            "analysis_type": {
                "type": "string",
                "enum": ["ratios", "comparison", "full"],
                "description": "分析类型：ratios=只算比率，comparison=多期对比，full=完整分析",
            },
        },
        "required": ["file_path"],
    }

    async def execute(
        self,
        file_path: str,
        periods: Optional[List[str]] = None,
        analysis_type: str = "full",
    ) -> str:
        """执行财报分析"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"错误：文件不存在 - {file_path}"
            if path.suffix.lower() not in [".xlsx", ".xlsm"]:
                return f"错误：仅支持 .xlsx 格式，当前文件是 {path.suffix}"

            # 1. 读取 Excel
            data = self._read_excel(path)
            if not data["data"]:
                return "错误：Excel 文件没有可识别的数据，请检查文件格式"

            # 2. 计算财务比率
            target_periods = periods if periods else data["periods"]
            ratios = self._compute_ratios(data, target_periods)

            # 3. 生成报告
            report = self._generate_report(data, ratios, target_periods, analysis_type)
            return report

        except Exception as e:
            return f"错误：财报分析失败 - {type(e).__name__}: {e}"

    def _read_excel(self, path: Path) -> Dict:
        """读取 Excel，假定结构：第一行是期数（年份/季度），第一列是科目名"""
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.active

        # 第一行：期数（年份/季度名）
        periods = []
        for col in range(2, ws.max_column + 1):
            header = ws.cell(row=1, column=col).value
            if header is not None:
                periods.append(str(header).strip())

        # 后续行：科目 + 各期数据
        data = {}
        for row in range(2, ws.max_row + 1):
            item_name = ws.cell(row=row, column=1).value
            if not item_name:
                continue
            values = {}
            for idx, period in enumerate(periods):
                cell_value = ws.cell(row=row, column=idx + 2).value
                values[period] = float(cell_value) if cell_value is not None else 0.0
            data[str(item_name).strip()] = values

        return {"periods": periods, "data": data}

    def _compute_ratios(self, data: Dict, target_periods: List[str]) -> Dict[str, Dict[str, float]]:
        """计算核心财务比率（所有比率按行业标准计算）"""
        items = data["data"]

        def safe_div(numerator: float, denominator: float) -> float:
            """安全除法，避免除零"""
            if not denominator:
                return 0.0
            return (numerator / denominator) * 100 if "%" in "" else numerator / denominator

        ratios = {}
        for period in target_periods:
            d = {k: v.get(period, 0) for k, v in items.items()}

            revenue = d.get("营业收入", 0)
            cost = d.get("营业成本", 0)
            net_profit = d.get("净利润", 0)
            total_assets = d.get("总资产", 0)
            total_liab = d.get("总负债", 0)
            equity = d.get("股东权益", 0)
            current_assets = d.get("流动资产", 0)
            current_liab = d.get("流动负债", 0)
            inventory = d.get("存货", 0)

            ratios[period] = {
                "毛利率(%)": (revenue - cost) / revenue * 100 if revenue else 0,
                "净利率(%)": net_profit / revenue * 100 if revenue else 0,
                "ROE(%)": net_profit / equity * 100 if equity else 0,
                "ROA(%)": net_profit / total_assets * 100 if total_assets else 0,
                "资产负债率(%)": total_liab / total_assets * 100 if total_assets else 0,
                "流动比率": current_assets / current_liab if current_liab else 0,
                "速动比率": (current_assets - inventory) / current_liab if current_liab else 0,
            }
        return ratios

    def _generate_report(
        self, data: Dict, ratios: Dict, target_periods: List[str], analysis_type: str
    ) -> str:
        """生成 Markdown 格式的分析报告"""
        items = data["data"]

        report = "# 财报分析报告\n\n"
        report += f"**分析期间**：{', '.join(target_periods)}\n"
        report += f"**分析类型**：{analysis_type}\n\n"
        report += "---\n\n"

        # 一、原始数据
        report += "## 一、原始数据（单位：万元）\n\n"
        report += "| 科目 | " + " | ".join(target_periods) + " |\n"
        report += "|" + "---|" * (len(target_periods) + 1) + "\n"
        for item_name, values in items.items():
            row = (
                f"| {item_name} | "
                + " | ".join(f"{values.get(p, 0):.2f}" for p in target_periods)
                + " |"
            )
            report += row + "\n"

        # 二、财务比率
        report += "\n## 二、核心财务比率\n\n"
        report += "| 比率 | " + " | ".join(target_periods) + " |\n"
        report += "|" + "---|" * (len(target_periods) + 1) + "\n"
        ratio_names = list(ratios[target_periods[0]].keys())
        for ratio_name in ratio_names:
            row = (
                f"| {ratio_name} | "
                + " | ".join(f"{ratios[p][ratio_name]:.2f}" for p in target_periods)
                + " |"
            )
            report += row + "\n"

        # 三、同比分析（仅当多期且 analysis_type 包含 comparison/full）
        if analysis_type in ["comparison", "full"] and len(target_periods) >= 2:
            report += "\n## 三、同比分析\n\n"
            for i in range(1, len(target_periods)):
                cur, prev = target_periods[i], target_periods[i - 1]
                report += f"### {prev} → {cur}\n\n"
                for ratio_name in ratio_names:
                    cur_val = ratios[cur][ratio_name]
                    prev_val = ratios[prev][ratio_name]
                    if prev_val:
                        change = cur_val - prev_val
                        if abs(change) < 0.01:
                            emoji = "➡️"
                        elif change > 0:
                            emoji = "📈"
                        else:
                            emoji = "📉"
                        report += f"- {emoji} {ratio_name}: {prev_val:.2f} → {cur_val:.2f}（{'+' if change >= 0 else ''}{change:.2f}）\n"
                report += "\n"

        return report
