from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
loader = PyPDFLoader("data/故障表.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
chunks = splitter.split_documents(docs)
embeddings = OpenAIEmbeddings(
    model="embedding-2",
    api_key="eb3fb13fc3754bfaa275799a36aea051.7seUY4DH9NIlJvJH",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
vectordb.persist()
def search_manual(query: str) -> str:
    docs = vectordb.similarity_search(query, k=2)
    return "\\n".join([doc.page_content for doc in docs])
def search_manual(query: str) -> str:
    docs = vectordb.similarity_search(query, k=2)
    return "\\n".join([doc.page_content for doc in docs])