import streamlit as st
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI

# 解决网页中文乱码
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="工业故障排查助手", layout="wide")
st.title("🏭 工业设备智能诊断与预测 Agent")

# 侧边栏放 Key
with st.sidebar:
    st.header("配置")
    api_key = st.text_input("请输入你的 GLM API Key", type="password")
    if not api_key:
        st.warning("请填入 API Key 才能运行！")
        st.stop()

llm = ChatOpenAI(
    model="glm-4",
    api_key=api_key,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    temperature=0.1
)

# 主界面
user_input = st.text_input("请输入您的故障咨询（例如：机器报错E001，请分析原因）")

if st.button("开始诊断与预测") and user_input:
    with st.spinner("AI 正在查阅手册并思考中..."):
        # 1. 诊断
        response = llm.invoke(user_input)
        st.success("✅ 诊断完成")
        st.markdown("### 📄 诊断报告")
        st.write(response.content)

        # 2. 画图表数据
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        fault_counts = [3, 2, 5, 1, 0, 2, 4, 6, 1, 3, 5, 2]

        # 3. 画图并展示
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(months, fault_counts, marker='o', color='b', label='历史数据')
        ax.set_title('E001 故障趋势图')
        ax.set_xlabel('月份')
        ax.set_ylabel('故障次数')
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)