import os

from openai import OpenAI


def get_res(user_prompt):
    response = OpenAI(api_key=os.environ.get("ARK_API_KEY"),
                      base_url="https://ark.cn-beijing.volces.com/api/v3", ).chat.completions.create(
        model='ep-20250819144501-s6qrx',
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0,
        stream=False,
    )
    return response.choices[0].message.content


def make_prompt():  # 构造用户prompt
    # 任务目标描述
    instruction = """
给定一段用户与手机流量套餐客服的对话，你的任务是判断客服的回答是否符合下面的规范：
1.必须有礼貌；
2.必须用官方口吻，不能使用网络用语；
3.介绍套餐时，必须准确提及产品名称、月费价格和月流量总量。上述信息缺失一项或多项，或信息与事实不符，都算信息不准确；
4.不可以是话题终结者；

已知产品包括：
经济套餐，月费50元，10G流量；
畅游套餐，月费180元，100G流量；
无限套餐，月费300元，1000G流量；
校园套餐，月费150元，200G流量，仅限在校生；
"""
    # 零样本思维链
    cot = "请一步一步分析对话"  # 启用思维链
    # cot = ""  # 不启用思维链

    # 输出描述
    output_text = """
如果符合规范输出：Y
如果不符合规范输出：N
"""

    # 对话上下文
    context = """
用户：你们有什么流量大的套餐
客服：亲，我们现在正在推广无限套餐，每月300元就可以享受1000G流量，您感兴趣吗？
"""

    # 构造prompt
    prompt = f"""
# 目标:
{instruction}
{cot}
# 输出描述:
{output_text}
# 对话上下文:
{context}
"""
    return prompt


print(get_res(make_prompt()))
