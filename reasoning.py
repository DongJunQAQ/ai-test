from openai import OpenAI

client = OpenAI(api_key="pwPBpXKwB17zDk0dxY4S0yfRLpesJPauZPyMdfynU2tAgkVHL-funCQAUHjDeCzwxMPhnW06Vv1XRJeNuXcWbw",
                # ModelArts的API Key
                base_url="https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1")

response = client.chat.completions.create(
    model="DeepSeek-R1",  # 指定使用的模型
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},  # 设定模型的角色和行为准则
        {"role": "user", "content": "python如何获取环境变量中的值"},  # 用户的实际问题
    ],
    temperature=1,
    stream=False  # 不使用流式响应，会等待模型生成完整回答后一次性返回而不是一个字一个字的生成
)

print("------以下为推理过程:------")
print(response.choices[0].message.reasoning_content)
print("------以下为推理结果:------")
print(response.choices[0].message.content)
