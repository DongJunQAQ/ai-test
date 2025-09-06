import json
import os

import httpx
from openai import OpenAI

amap_key = os.environ.get("AMAP_KEY")
amap_url = "https://restapi.amap.com/v5/place"
headers = {'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'}


def get_location(keywords, city):  # 获取地点经纬度坐标
    url = f"{amap_url}/text?keywords={keywords}&region={city}&key={amap_key}&page_size=1"
    response = httpx.request("GET", url, headers=headers)
    res = response.json()
    if "pois" in res and res.get("pois"):  # 如果响应体中有pois字段
        return res.get("pois")[0].get("location")


def nearby_search(location, keywords):  # 根据经纬度坐标进行周边搜索
    url = f"{amap_url}/around?location={location}&keywords={keywords}&key={amap_key}&radius=3000"
    response = httpx.request("GET", url, headers=headers)
    res = response.json()
    ans = ""
    if "pois" in res and res.get("pois"):
        for i in range(min(3, len(res.get("pois")))):  # 循环执行最多3次，如果列表长度小于3就以实际长度作为循环次数，如果列表长度大于等于3就只循环3次
            name = res.get("pois")[i].get("name")
            address = res.get("pois")[i].get("address")
            distance = res.get("pois")[i].get("distance")
            ans += f"名称：{name}\n地址：{address}\n距离：{distance}米\n\n"
        return ans


def print_json(data):
    if hasattr(data, 'model_dump_json'):  # 检查data是否有model_dump_json方法，如果有说明这是一个Pydantic模型对象
        data = json.loads(
            data.model_dump_json())  # 调用model_dump_json()方法将Pydantic模型转换为JSON字符串，再用json.loads()将JSON字符串解析为Python对象
    if isinstance(data, list):  # 检查data是否是列表类型
        for item in data:  # 如果是列表，就遍历列表中的每个元素
            print_json(item)  # 对列表中的每个元素递归调用print_json函数，实现嵌套处理
    elif isinstance(data, dict):  # 检查data是否是字典类型
        print(json.dumps(data, indent=4,
                         ensure_ascii=False))  # 如果是字典，使用json.dumps()将Python对象转换为JSON字符串，indent=4表示缩进4个空格使输出更易读，ensure_ascii=False确保非ASCII字符（中文）正常显示
    else:  # 如果既不是列表也不是字典则直接打印此数据
        print(data)


def calling_model(messages):
    response = OpenAI(api_key=os.environ.get("ARK_API_KEY"),
                      base_url="https://ark.cn-beijing.volces.com/api/v3", ).chat.completions.create(
        model="ep-20250819144501-s6qrx",
        messages=messages,
        temperature=0,
        seed=1024,  # 使得模型每次回答的结果都差不多一致
        tool_choice="auto",  # 使得模型自主判断，根据需求决定“直接生成回答”或“调用1个/多个工具”。
        tools=[  # 定义模型可以调用的工具列表，仅支持将函数作为工具
            {
                'type': 'function',
                'function': {
                    'name': 'get_location',
                    'description': '根据地点关键字和城市名获取地点的经纬度坐标',
                    'parameters': {  # 函数参数定义
                        'type': 'object',  # 参数类型为对象
                        'properties': {  # 具体属性
                            'keywords': {
                                'type': 'string',
                                'description': "要搜索的地点关键字"
                            },
                            'city': {
                                'type': 'string',
                                'description': "所在的城市名"
                            }
                        },
                        "required": ["keywords", "city"]
                    }
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'nearby_search',
                    'description': '根据关键字和经纬度坐标进行周边查找',
                    'parameters': {  # 函数参数定义
                        'type': 'object',  # 参数类型为对象
                        'properties': {  # 具体属性
                            'keywords': {
                                'type': 'string',
                                'description': "要进行周边搜索的关键字"
                            },
                            'location': {
                                'type': 'string',
                                'description': "经纬度坐标"
                            }
                        },
                        "required": ["keywords", "location"]}
                }
            }
        ]
    )
    return response.choices[0].message


if __name__ == '__main__':
    prompt = "我想在夷陵广场附近喝咖啡吃川菜，给我推荐几个"
    # prompt = "宜昌东站附近的肯德基"
    # prompt = "宜昌东站附近的麦当劳"
    my_messages = [
        {'role': 'system', 'content': '你是一个地图通，可以先查找地点的经纬度坐标然后通过经纬度坐标进行周边搜索'},
        {'role': 'user', 'content': prompt}]
    model_response = calling_model(my_messages)  # 第一次调用模型
    my_messages.append(model_response)  # 将上一步调用模型的响应结果添加至历史会话中
    while model_response.tool_calls is not None:  # 循环处理工具调用，只要模型返回了工具调用请求，就持续执行调用，即支持模型一次返回多个工具调用任务
        for tool_call in model_response.tool_calls:
            result = ""
            kwargs = json.loads(tool_call.function.arguments)  # 解析工具调用时的参数（JSON字符串转Python字典）
            print("=====函数参数=====")
            print_json(kwargs)
            # 根据工具名称调用对应的函数
            if tool_call.function.name == "get_location":
                print("调用：get_location")
                result = get_location(**kwargs)
            elif tool_call.function.name == "nearby_search":
                print("调用：nearby_search")
                result = nearby_search(**kwargs)
            # 打印工具调用的返回结果
            print("=====函数返回=====")
            print_json(result)
            # 将工具调用的结果添加到对话历史中，供模型后续处理
            my_messages.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': tool_call.function.name,
                'content': str(result)
            })
        # 工具调用完成后，最后调用一次模型，传入更新后的对话历史
        model_response = calling_model(my_messages)
        my_messages.append(model_response)  # 将模型的最终回复加入到对话历史中
    print("=====最终回复=====")
    print(model_response.content)
    print("=====对话历史=====")
    print(print_json(my_messages))
