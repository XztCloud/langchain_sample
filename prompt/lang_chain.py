import os

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from langserve import add_routes

app = FastAPI(
    title="Language Server",
    description="A minimal FastAPI project.",
    version="0.1.0",
)

class MyLangChain:
    def __init__(self):
        # 加载模型
        self.model = ChatDeepSeek(
            model="deepseek-chat",
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        # 提示词模板
        self.system_template = "请把这段话翻译成{language}："
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("user", "{text}")
        ])
        # 字符串解析
        self.parser = StrOutputParser()
        # ICEL连接组件
        self.chain = self.prompt_template | self.model | self.parser

    def run_simple_llm(self):
        message = [
            SystemMessage(content="Translate the following from English into Chinese"),
            HumanMessage(content="Hi"),
        ]
        result = self.model.invoke(message)

        # 提取输出中的字符串部分
        str_result = self.parser.invoke(result)
        print(str_result)

        # 简洁写法
        self.chain = self.model | self.parser
        self.chain.invoke(message)

        # 提示词模板
        result = self.prompt_template.invoke({"language":"法语", "text":"What a nice day!"})
        print(result.to_messages())

        # ICEL连接组件
        self.chain = self.prompt_template | self.model | self.parser
        self.chain.invoke({"language":"德语", "text":"What a nice day!"})

    def simple(self):
        pass

global_lang_chain = MyLangChain()

add_routes(
    app,
    global_lang_chain.chain,
    path="/chain",
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)