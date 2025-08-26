import os

from openai import OpenAI

# 定义系统提示词
messages = [{"role": "system", "content": """
你是一个手机流量套餐的客服代表，可以帮助用户选择最合适的流量套餐产品，可以选择的套餐包括：
经济套餐，月费50元，10G流量；
畅游套餐，月费180元，100G流量；
无限套餐，月费300元，1000G流量；
校园套餐，月费150元，200G流量，仅限在校生；
"""}]


def calling_model(user_prompt):
    messages.append({"role": "user", "content": user_prompt})  # 接收用户输入并添加到对话历史
    response = OpenAI(api_key=os.environ.get("ARK_API_KEY"),
                      base_url="https://ark.cn-beijing.volces.com/api/v3", ).chat.completions.create(
        model="ep-20250819144501-s6qrx",
        messages=messages,  # 对话历史
    )
    res = response.choices[0].message.content
    messages.append({"role": "assistant", "content": res})  # 将模型回复存入对话历史以维持上下文
    return res


calling_model("最便宜的套餐是什么")  # 第一轮对话
calling_model("多少钱")  # 第二轮对话
calling_model("给我办一个")  # 第三轮对话
print(messages)
