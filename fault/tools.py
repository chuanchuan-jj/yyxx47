import json
import subprocess
import os
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import retrievesss
search_manual = retrievesss.search_manual
HISTORY_DB = {
    "E001": {"reason": "电源模块过载烧毁", "last_fix": "2026-05-12", "count": 3},
    "E002": {"reason": "散热风扇积灰卡死", "last_fix": "2026-03-01", "count": 1},
}
def query_history(error_code: str) -> str:
    record = HISTORY_DB.get(error_code, {"reason": "无历史记录", "count": 0})
    return json.dumps(record, ensure_ascii=False)

@tool
def query_manual_tool(question: str) -> str:
    """当需要查询故障诊断手册时调用此工具，输入为故障描述或代码"""
    return search_manual(question)

@tool
def query_history_tool(error_code: str) -> str:
    """当需要查询设备历史维修记录时调用此工具，输入为故障代码"""
    return query_history(error_code)

@tool
def generate_chart_tool(instruction: str) -> str:
    """当用户要求画图、分析趋势、生成统计图表时调用此工具"""
    llm = ChatOpenAI(
        model="glm-4",
        api_key="eb3fb13fc3754bfaa275799a36aea051.7seUY4DH9NIlJvJH",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.1
    )
    prompt = f"根据指令：'{instruction}'，生成一段直接能运行的 Python 代码。要求用 matplotlib 画图，保存为 chart.png。只输出代码，不含解释。"
    code = llm.invoke(prompt).content
    temp_file = "temp_code.py"
    with open(temp_file, "w", encoding='utf-8') as f:
        f.write(code)
    try:
        subprocess.run(["python", temp_file], check=True, timeout=15, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return "图表已生成，请查看当前目录下的 chart.png"
    except Exception as e:
        return f"画图失败，错误：{str(e)}"
