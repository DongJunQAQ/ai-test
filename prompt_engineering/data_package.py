from general.keys import client


def get_res(user_prompt, model='ep-20250819144501-s6qrx'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": """
你是一个手机流量套餐的客服，可以帮助用户选择合适的流量套餐产品。可以选择的套餐包括：
{"name":"经济套餐","price":50,"data":10,"requirement":None},
{"name":"畅游套餐","price":180,"data":100,"requirement":None},
{"name":"无限套餐","price":300,"data":1000,"requirement":None},
{"name":"校园套餐","price":150,"data":200,"requirement":"在校生"},
"""},
                  {"role": "user", "content": user_prompt}],
        temperature=0,
        stream=False,
    )
    return response.choices[0].message.content


def make_prompt():  # 构造用户prompt
    # 任务目标描述
    instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件；
每种流量套餐产品包含三个属性：名称(name)、每月流量(data)、每月价格(price)；
请根据用户的输入识别用户在上述三种属性上的需求是什么。
"""
    # 用户的输入
    input_text = """办个10G的套餐"""

    # 输出格式
    output_format = """
以JSON格式进行输出：
1.name字段的取值为string类型，取值必须为以下之一：经济套餐、畅游套餐、无限套餐、校园套餐，每次输出时都需要去数据库查询对应的套餐名并输出name字段，
数据库中共有以下4种套餐：
{"name":"经济套餐","price":50,"data":10,"requirement":None},
{"name":"畅游套餐","price":180,"data":100,"requirement":None},
{"name":"无限套餐","price":300,"data":1000,"requirement":None},
{"name":"校园套餐","price":150,"data":200,"requirement":"在校生"},


2.price字段的取值为一个结构体或null，该结构体包含以下两个字段：
(1)operator：string类型，取值范围：'<='（小于等于）,'>='（大于等于）,'=='（等于）；
(2)value：int类型；

3.data字段的取值为一个结构体或null，该结构体包含以下两个字段：
(1)operator：string类型，取值范围：'<='（小于等于）,'>='（大于等于）,'=='（等于）；
(2)value：int类型或string类型，当为string类型时值只能为'无上限'；

4.输出的结果中可以按照price或data排序，并以sort字段标识，取值为一个结构体：
(1)结构体中以'order'='descend'表示按照降序排序，以'value'字段存储待排序的字段；
(2)结构体中以'order'='ascend'表示按照升序排序，以'value'字段存储待排序的字段；

5.输出中只包含用户提及的字段，不要猜测任何用户未直接提及的字段，不输出值为null的字段。
"""
    # 示例
    example = """
办个100G的套餐：{"name":"畅游套餐"}
便宜的套餐：{"sort":{"order":"ascend","value"="price"}}
有没有不限流量的：{"data":{"operator":"==","value":"无上限"}}
流量大的：{"sort":{"order":"descend","value"="data"}}
100G以上流量的套餐最便宜的是哪一个：{"data":{"operator":">=","value":100},"sort":{"order":"ascend","value"="price"}}
月费不超过200块的：{"price":{"operator":"<=","value":200}}
就要月费180块的哪个套餐：{"price":{"operator":"==","value":180}}
经济套餐：{"name":"经济套餐"}
土豪套餐：{"name":"无限套餐"}
"""

    # 构造prompt
    prompt = f"""
# 目标:
{instruction}
# 用户输入:
{input_text}
# 输出格式:
{output_format}
# 示例:
{example}
"""
    return prompt


if __name__ == "__main__":
    print(get_res(make_prompt()))
    # 暂无数据库查询功能，即只能根据提示词输出一些筛选条件，无法输出相应套餐的name字段；
