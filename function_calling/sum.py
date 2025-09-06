import json
import os

from openai import OpenAI


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
        temperature=0.7,
        tools=[{  # 定义模型可以调用的工具列表，仅支持将函数作为工具
            'type': 'function',
            'function': {
                'name': 'my_sum',
                'description': '加法器，计算一组数的和',
                'parameters': {  # 函数参数定义
                    'type': 'object',  # 参数类型为对象
                    'properties': {  # 具体属性
                        'numbers': {  # 参数名为numbers
                            'type': 'array',  # 类型为数组
                            'items': {
                                'type': 'number'  # 数组元素为数字类型
                            }
                        }
                    }
                }
            }
        }],
    )
    return response.choices[0].message


def my_sum(*vals):  # 大模型会自动调用此工具函数来求和
    total = 0
    for val in vals:
        if isinstance(val, list):  # 如果参数是列表，递归处理其中的元素
            total += my_sum(*val)
        else:
            total += val  # 如果不是列表则直接相加即可
    return total


if __name__ == '__main__':
    prompt = '告诉我1，2，3，4，5，6，7，8，9，10加起来的总和'
    # prompt = "桌上有2个苹果，四个桃子和3本书，还有3个番茄，以及三个傻瓜，一共有几个水果？"  # 使用该prompt时模型不会去调用工具来求和
    # prompt = "1+2+3...+99+100"
    my_messages = [{'role': 'system', 'content': '你是一个数学家'},
                   {'role': 'user', 'content': prompt}]
    model_response = calling_model(my_messages)  # 第一次调用模型
    my_messages.append(model_response)  # 将上一步调用模型的响应结果添加至历史会话中
    if model_response.tool_calls is not None:  # 如果返回的是函数工具的调用结果
        tool_call = model_response.tool_calls[0]  # 获取第一个工具调用
        if tool_call.function.name == 'my_sum':  # 检查是否调用的是my_sum函数
            args = json.loads(tool_call.function.arguments)  # 解析函数调用的参数（JSON字符串转Python字典）
            result = my_sum(args['numbers'])  # 调用工具函数将参数求和
            my_messages.append({  # 将工具调用的结果添加到对话历史中，用以验证是否调用了工具
                'tool_call_id': tool_call.id,  # 工具调用ID
                'role': 'tool',
                'name': tool_call.function.name,  # 工具的名称
                'content': str(result)  # 工具返回的结果
            })
            model_response = calling_model(my_messages)  # 第二次调用模型，传入包含工具结果的完整对话历史
            my_messages.append(model_response)  # 将第二次的模型响应的结果添加到对话历史
    print("==模型的最终回复==")
    print(model_response.content)
    print("==对话历史==")
    print_json(my_messages)
