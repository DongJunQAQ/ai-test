import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("ARK_API_KEY"), base_url="https://ark.cn-beijing.volces.com/api/v3", )
