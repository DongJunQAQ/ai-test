from openai import OpenAI

client = OpenAI(api_key="sk-799f0469a4ef4bb495250f0295fe9319", base_url="https://api.deepseek.com")

messages = [{"role": "user", "content": "9.11 和 9.8, 那个更大?"}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages
)

reasoning_content = response.choices[0].message.reasoning_content  # 推理过程
content = response.choices[0].message.content  # 回答结果
print(reasoning_content)
print(content)
