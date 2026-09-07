"""直接测试 FinancialReportTool 工具，绕过 Manus"""
import asyncio
from app.tool.financial_report import FinancialReportTool

tool = FinancialReportTool()
file_path = r"D:\projects\OpenManus\examples\tesco_fy2024_sample.xlsx"

print("=" * 60)
print("测试 1: 全量分析（3 期）")
print("=" * 60)
result = asyncio.run(tool.execute(file_path=file_path))
print(result)

print()
print("=" * 60)
print("测试 2: 只看 2024 年")
print("=" * 60)
result = asyncio.run(tool.execute(file_path=file_path, periods=["2024"]))
print(result)
