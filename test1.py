import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)
print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20250723215341-vncq7",  # your model endpoint ID
    messages=[
        {"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)
