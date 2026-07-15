import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="glm-4",
    api_key="eb3fb13fc3754bfaa275799a36aea051.7seUY4DH9NIlJvJH",
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    temperature=0.1
)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
if __name__ == "__main__":
    print("正在调用大模型进行诊断...")
    test_input = "机器报错E001，请分析故障原因，并给出解决建议。"
    result = llm.invoke(test_input)
    print("\\n=== 大模型诊断结果 ===")
    print(result.content)
    print("\\n正在生成故障趋势图...")
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    fault_counts = [3, 2, 5, 1, 0, 2, 4, 6, 1, 3, 5, 2]
    plt.figure(figsize=(10, 5))
    plt.plot(months, fault_counts, marker='o', color='b', linestyle='-', linewidth=2)
    plt.title('故障趋势图', fontsize=15)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('故障次数', fontsize=12)
    plt.grid(True)
    plt.savefig('chart.png')
    print("图表生成成功！请查看左侧项目目录下的 chart.png")
    plt.show()