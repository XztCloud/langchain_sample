# This is a sample Python script.
import asyncio
import time
import requests
from openai import OpenAI
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from fastapi import FastAPI, Depends
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

#定义带路径参数的接口
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str=None):
    """
    获取物品信息
    :param item_id:物品信息ID
    :param q: 可选查询参数（字符串类型）
    :return:
    """
    return {"item_id": item_id, "q":q}

@app.post("/items/")
def create_item(item: Item):
    # item是Pydantic模型实例，可通过.item访问字段
    return {"item_name":item.name, "item_price":item.price}

@app.get("/async/")
async def read_async():
    # 模拟异步任务
    await asyncio.sleep(1)
    return {"message": "Hello, FastAPI! This is an async response!"}

class City(BaseModel):
    name: str
    adcode: int=None

@app.get("/weather/")
async def get_weather(city:City = Depends()):
    print(f'get city_name:{city.name}, dcsdf')
    city_code = get_acode(city.name)
    if city_code is None:
        return {"message": "city_name is not found"}
    else:
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key=344dbfd23618c70e1ebe3cce511b8985&city={city_code}&extensions=all"
        # 发送GET请求
        response = requests.get(url)
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            print(f'{data}')
            # 获取天气信息
            try:
                weather = data['forecasts'][0]['casts'][0]['dayweather']
                return {"message": "city_name is found", "weather": weather}
            except IndexError as exc:
                print(f'failed to parse response: {exc}')
                return {"message": "city_name is found", "weather": "unknown"}
        return {"message": "weather is found", "adcode": name}

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


def get_acode(city_name):
    import pandas as pd
    # 读取整个 Excel 文件
    df = pd.read_excel('./AMap_adcode_citycode.xlsx', sheet_name='Sheet1')  # 可以指定工作表名或索引

    for i in range(len(df)):
        if df['中文名'][i] == city_name or df['中文名'][i][:-1] == city_name:
            return df['adcode'][i]
            break
    return None



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    def get_completion(prompt, model="gpt-3.5-turbo"):
        '''
        :param prompt:
        :param model:
        :return:
        '''
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    # 需要总结的文本内容
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

    response = get_completion(prompt)
    print(response)

    # 读取excel文件
    # import pandas as pd
    # print(df)
    # print(df['中文名'])
    # print(df['adcode'])
    # print(df['weather'])
    # print(df['temperature'])
    # print(df['wind_direction'])
    # print(df['wind_power'])
    # print(df['humidity'])
    # print(df['report_time'])