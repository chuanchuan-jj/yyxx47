import streamlit as st
from zhipuai import ZhipuAI
import os
os.environ["ZHIPUAI_API_KEY"] = "83b03fe1cefd496aa27d25ca19b6561e.u10qjnmpoRVvlYdS"
st.set_page_config(page_title="我的专属AI助手")
st.title("智能问答演示 (基于 ZhipuAI)")
st.write("输入你的问题，AI 会根据你文档的内容进行回答。")
try:
    with open("my_data.txt", "r", encoding="utf-8") as f:
        doc_content = f.read()
except FileNotFoundError:
    doc_content = "未找到文档，请确保 my_data.txt 文件与代码在同一目录。"
query = st.text_input("请输入你想问的问题：")
if query:
    with st.spinner("正在思考中..."):
        client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
        prompt = f"请根据以下文档内容，回答用户的问题。\n\n文档内容：{doc_content[:500]}\n\n用户问题：{query}"
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.success("回答如下：")
        st.write(response.choices[0].message.content)
