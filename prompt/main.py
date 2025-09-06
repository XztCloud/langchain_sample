# This is a sample Python script.
import os
# import panel as pn


# import inppip
import openai
from openai import OpenAI

from lang_chain import MyLangChain

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lang_chain = MyLangChain()
    lang_chain.run_simple_llm()


def simple_prompt():
    openai_key = os.getenv("DEEPSEEK_API_KEY")

    client = OpenAI(api_key=openai_key, base_url="https://api.deepseek.com")
    def get_completion(prompt, model='deepseek-chat'):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content

    def get_completion_from_messages(messages, model='deepseek-chat', temperature=0):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content


    ########## 原则一：编写清晰、具体的指令

    # 1.使用分隔符清晰地表示输入的不同部分
    text = f"""
    你应该提供尽可能清晰、具体的指示，以表达你希望模型执行的任务。\
    这将引导模型朝向所需的输出，并降低收到无关或不正确响应的可能性。\
    不要将写清晰的提示与写简短的提示混淆。\
    在许多情况下，更长的提示可以为模型提供更多的清晰度和上下文信息，从而导致更详细和相关的输出。
    """

    prompt = f"""
    把用三个反引号括起来的文本总结成一句话。
    ```{text}```
    """

    # 2.要求一个结构化输出
    prompt2 = f"""
    请生成包括书名、作者和类别的三本虚构书籍清单，\
    并以JSON格式返回，每本书包含一个对象，\
    包括book_id、title、author和genre。
    """

    # 3.要求模型检查是否满足条件
    text3_1 = f"""
    泡一杯茶很容易。首先，需要把水烧开。\
    在等待期间，拿一个杯子并把茶包放进去。\
    一旦水足够热，就把它倒在茶包上。\
    等待一会儿，让茶叶浸泡。几分钟后，取出茶包。\
    如果你愿意，可以加一些糖或牛奶调味。\
    就这样，你可以享受一杯美味的茶了。
    """

    text3_2 = f"""
        今天阳光明媚，鸟儿在歌唱。\
        这是一个去公园散步的美好日子。\
        鲜花盛开，树枝在微风中轻轻摇曳。\
        人们外出享受着这美好的天气，有些人在野餐，有些人在玩游戏或者在草地上放松。\
        这是一个完美的日子，可以在户外度过并欣赏大自然的美景。
    """
    prompt3 = f"""
    您将获得由三个引号括起来的文本。\
    如果它包含一系列的指令，则需要按照以下格式重新编写这些指令：
    
    第一步 - ...
    第二步 - …
    …
    第N步 - …
    
    如果文本中不包含一系列的指令，则直接写“未提供步骤”。"
    \"\"\"{text3_2}\"\"\"
    """

    # 4.提供少量示例
    prompt4 = f"""
    你的任务是以一致的风格回答问题。

    <孩子>: 教我耐心。

    <祖父母>: 挖出最深峡谷的河流源于一处不起眼的泉眼；最宏伟的交响乐从单一的音符开始；最复杂的挂毯以一根孤独的线开始编织。

    <孩子>: 教我韧性。
    """

    ########## 原则二：给模型时间去思考
    # 1.指定完成任务所需的步骤
    text = f"""
    在一个迷人的村庄里，兄妹杰克和吉尔出发去一个山顶井里打水。\
    他们一边唱着欢乐的歌，一边往上爬，\
    然而不幸降临——杰克绊了一块石头，从山上滚了下来，吉尔紧随其后。\
    虽然略有些摔伤，但他们还是回到了温馨的家中。\
    尽管出了这样的意外，他们的冒险精神依然没有减弱，继续充满愉悦地探索。
    """
    prompt_1 = f"""
    执行以下操作：
    1-用一句话概括下面用三个反引号括起来的文本。
    2-将摘要翻译成法语。
    3-在法语摘要中列出每个人名。
    4-输出一个 JSON 对象，其中包含以下键：French_summary，num_names。

    请用换行符分隔您的答案。

    Text:
    ```{text}```
    """

    prompt_2 = f"""
    1-用一句话概括下面用<>括起来的文本。
    2-将摘要翻译成英语。
    3-在英语摘要中列出每个名称。
    4-输出一个 JSON 对象，其中包含以下键：English_summary，num_names。

    请使用以下格式：
    文本：<要总结的文本>
    摘要：<摘要>
    翻译：<摘要的翻译>
    名称：<英语摘要中的名称列表>
    输出 JSON：<带有 English_summary 和 num_names 的 JSON>

    Text: <{text}>
    """

    # 2.指导模型在下结论之前找出一个自己的解法
    prompt_3 = f"""
    请判断学生的解决方案是否正确，请通过如下步骤解决这个问题：

步骤：

    首先，自己解决问题。
    然后将你的解决方案与学生的解决方案进行比较，并评估学生的解决方案是否正确。在自己完成问题之前，请勿决定学生的解决方案是否正确。

使用以下格式：

    问题：问题文本
    学生的解决方案：学生的解决方案文本
    实际解决方案和步骤：实际解决方案和步骤文本
    学生的解决方案和实际解决方案是否相同：是或否
    学生的成绩：正确或不正确

问题：

    我正在建造一个太阳能发电站，需要帮助计算财务。 
    - 土地费用为每平方英尺100美元
    - 我可以以每平方英尺250美元的价格购买太阳能电池板
    - 我已经谈判好了维护合同，每年需要支付固定的10万美元，并额外支付每平方英尺10美元
    作为平方英尺数的函数，首年运营的总费用是多少。

学生的解决方案：

    设x为发电站的大小，单位为平方英尺。
    费用：
    1. 土地费用：100x
    2. 太阳能电池板费用：250x
    3. 维护费用：100,000+100x
    总费用：100x+250x+100,000+100x=450x+100,000

实际解决方案和步骤：
    """


    # 如果模型在训练过程中接触了大量的知识，它并没有完全记住所见的信息，因此它并不很清楚自己知识的边界。这意味着它可能会尝试回答有关晦涩主题的
    # 问题，并编造听起来合理但实际上并不正确的答案。我们称这些编造的想法为幻觉。
    prompt_4 = f"""
    告诉我 Boie 公司生产的 AeroGlide UltraSlim Smart Toothbrush 的相关信息
    """

    # response = get_completion(prompt_4)
    # print(response)

    messages = [
        {'role': 'system', 'content': '你是一个像莎士比亚一样说话的助手。'},
        {'role': 'user', 'content': '给我讲个笑话'},
        {'role': 'assistant', 'content': '鸡为什么过马路'},
        {'role': 'user', 'content': '我不知道'}]

    messages =  [
        {'role':'system', 'content':'你是个友好的聊天机器人。'},
        {'role':'user', 'content':'Hi, 我是Isa'},
        {'role':'assistant', 'content': "Hi Isa! 很高兴认识你。今天有什么可以帮到你的吗?"},
        {'role':'user', 'content':'是的，你可以提醒我, 我的名字是什么?'}  ]

    response = get_completion_from_messages(messages, temperature=1)
    print(response)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
