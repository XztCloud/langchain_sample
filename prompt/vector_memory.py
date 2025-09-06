import asyncio
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_deepseek import ChatDeepSeek

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

async def async_similarity_search(context:str):
    await vectorstore.asimilarity_search("cat")

if __name__ == "__main__":
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    embedding = DashScopeEmbeddings(
        model="text-embedding-v2", # 阿里云模型
        dashscope_api_key = dashscope_api_key
    )
    # 测试文本
    test_vector = embedding.embed_query("测试文本")
    print(test_vector)  # 应返回一个向量（列表），如果返回 None 则 API 调用失败
    # 将文本嵌入向量数据库
    vectorstore = Chroma.from_documents(
        documents,
        embedding=embedding,
        # persist_directory="./chroma_db"  # 持久化存储
    )
    # 检查是否成功写入
    print(vectorstore._collection.count())  # 应返回文档数量
    # 与字符串查询的相似性返回文档和得分
    # result = vectorstore.similarity_search_with_score("cat")

    # 与字符串查询返回最相似的一组，按相似度排序
    result = vectorstore.similarity_search("cat")
    print(result)
    print("******************************")
    # 异步方法
    # result = asyncio.run(async_similarity_search(context="cat"))
    # print(f'result:{result}')

    # 创建一个可运行的检索器，限制每次查询返回最相关的1个结果
    retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)
    # 批量查询两个关键词
    result = retriever.batch(["cat", "shark"])
    print(result)
    print("******************************")

    # 相似写法
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    result = retriever.batch(["cat", "shark"])
    print(result)
    print("******************************")

    # 将向量数据库集成到链路
    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0
    )

    message = """
    Answer this question using the provided context only.
    {question}
    Context:
    {context}
    """

    prompt = ChatPromptTemplate.from_messages([("human", message)])
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
    response = rag_chain.invoke("tell me about cats")
    print(response.content)
    print("******************************")



