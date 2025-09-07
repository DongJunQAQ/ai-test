import json
import os
import sqlite3

from openai import OpenAI

database_schema_string = """
CREATE TABLE orders (
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    customer_id INT NOT NULL, -- 客户ID，不允许为空
    product_id STR NOT NULL, -- 产品ID，不允许为空
    price DECIMAL(10,2) NOT NULL, -- 价格，小数类型，总位数为10位，其中小数部分占2位，整数部分最多8位，不允许为空
    status INT NOT NULL, -- 订单状态，整数类型，不允许为空。0 代表待支付，1 代表已支付，2 代表已退款
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间
    pay_time TIMESTAMP -- 支付时间，可以为空
);
"""

mock_data = [  # 模拟数据
    (1, 1001, 'TSHIRT_1', 50.00, 0, '2023-09-12 10:00:00', None),
    (2, 1001, 'TSHIRT_2', 75.50, 1, '2023-09-16 11:00:00', '2023-08-16 12:00:00'),
    (3, 1002, 'SHOES_X2', 25.25, 2, '2023-10-17 12:30:00', '2023-08-17 13:00:00'),
    (4, 1003, 'SHOES_X2', 25.25, 1, '2023-10-17 12:30:00', '2023-08-17 13:00:00'),
    (5, 1003, 'HAT_Z112', 60.75, 1, '2023-10-20 14:00:00', '2023-08-20 15:00:00'),
    (6, 1002, 'WATCH_X001', 90.00, 0, '2023-10-28 16:00:00', None)
]


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
        tools=[{
            'type': 'function',
            'function': {
                'name': 'ask_database',
                'description': '使用此函数来回答用户有关业务的问题，输出应该是一个完整格式的SQL查询语句',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query_sql': {
                            'type': 'string',
                            'description': f"""将用户的需求转换为对应的SQL语句并以此回答用户的问题。
                            SQL语句应当按照此数据表结构{database_schema_string}来写。
                            查询语句应以纯文本形式返回，而非JSON格式。
                            查询语句只能包含SQLite所支持的语法。
                            """
                        }
                    },
                    'required': ["query_sql"]
                }
            }
        }],
    )
    return response.choices[0].message


def ask_database(query_sql):  # 根据大模型生成的SQL语句去查询数据库
    cursor.execute(query_sql)
    return cursor.fetchall()


if __name__ == "__main__":
    # 往数据库中插入测试数据
    conn = sqlite3.connect(':memory:')  # 创建一个内存中的临时SQLite数据库并建立连接，当数据库连接关闭后所有数据都会丢失
    cursor = conn.cursor()
    cursor.execute(database_schema_string)  # 创建数据表
    for i in mock_data:  # 依次插入数据
        cursor.execute('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)''', i)
    conn.commit()
    # 与大模型交互
    # prompt = "10月的销售额"
    prompt = "查询价格大于等于50的数据"
    my_messages = [{'role': 'system', 'content': '你是一个数据分析师，请基于数据库的数据回答问题'},
                   {'role': 'user', 'content': prompt}]
    model_response = calling_model(my_messages)  # 第一次调用模型
    my_messages.append(model_response)
    if model_response.tool_calls is not None:
        tool_call = model_response.tool_calls[0]
        if tool_call.function.name == 'ask_database':
            args = json.loads(tool_call.function.arguments)  # 解析函数调用的参数（JSON字符串转Python字典）
            print(f"模型给出的SQL：{args['query_sql']}")
            result = ask_database(args['query_sql'])
            print(f"数据库查询出的结果：{result}")
            my_messages.append({  # 将工具调用的结果添加到对话历史中，用以验证是否调用了工具
                'tool_call_id': tool_call.id,  # 工具调用ID
                'role': 'tool',
                'name': tool_call.function.name,  # 工具的名称
                'content': str(result)  # 工具返回的结果
            })
            model_response = calling_model(my_messages)  # 第二次调用模型，传入包含工具结果的完整对话历史
            my_messages.append(model_response)  # 将第二次的模型响应的结果添加到对话历史
    print("=====最终回复=====")
    print(model_response.content)
    print("=====对话历史=====")
    print_json(my_messages)
