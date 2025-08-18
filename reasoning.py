import os

from openai import OpenAI


def reasoning(question):
    client = OpenAI(api_key=os.environ.get("ARK_API_KEY"), base_url="https://ark.cn-beijing.volces.com/api/v3", )
    response = client.chat.completions.create(
        model="ep-20250723215341-vncq7",  # 指定使用的模型，这里使用的是DeepSeek-R1
        messages=[
            {"role": "system", "content": "你是一个程序员智能助手"},  # 设定模型的角色和行为准则
            {"role": "user", "content": question},  # 用户的实际问题
        ],
        temperature=1,  # 控制着模型生成文本时的随机性和创造性程度，通常是0到2之间的浮点数
        stream=False  # 不使用流式响应，会等待模型生成完整回答后一次性返回而不是一个字一个字的生成
    )
    process = response.choices[0].message.reasoning_content  # 推理过程
    results = response.choices[0].message.content  # 推理结果
    return process, results


if __name__ == "__main__":
    reasoning_process, reasoning_results = reasoning("python如何获取环境变量里的值")
    print("------以下为推理过程------")
    print(reasoning_process)
    print("------以下为推理结果------")
    print(reasoning_results)
