import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA
from zhipuai import ZhipuAI
from langchain.llms.base import LLM
from typing import Optional, List

os.environ["ZHIPUAI_API_KEY"] = "6a9ba223cdf7445bb43bebd9608b2af4.Jz3mZtMFZUyqtLTo"
class ZhipuLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "zhipu"
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
        response = client.chat.completions.create(
            model="glm-4",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

print(" 正在读取文档...")
loader = TextLoader("my_data.txt", encoding='utf-8')
documents = loader.load()
print("正在切分文档...")
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
texts = text_splitter.split_documents(documents)
print("正在存入向量数据库...")
from langchain_community.embeddings import HuggingFaceEmbeddings
from zhipuai import ZhipuAI
print("启动大模型直接测试...")
client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
user_query = "根据我提供的文档，提炼一下内容？"
prompt = f"请根据以下文档内容，回答用户的问题。\n\n文档内容：{documents[0].page_content[:500]}\n\n用户问题：{user_query}"
response = client.chat.completions.create(
    model="glm-4",
    messages=[{"role": "user", "content": prompt}]
)

print("测试成功！")
print(f"AI回答：\n{response.choices[0].message.content}")
