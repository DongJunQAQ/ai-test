import base64
import os

from openai import OpenAI


def encode_image(image_path):  # 读取本地图片文件并将其转化为base64编码
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_recognition(image_path, command):  # 图像识别
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),  # 读取火山引擎的API Key
    )
    response = client.chat.completions.create(
        model="doubao-1-5-thinking-vision-pro-250428",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encode_image(image_path)}"
                        },
                    },
                    {"type": "text", "text": command},
                ],
            }
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    local_image_path = "resource/image2.png"  # 本地图片路径
    print(image_recognition(local_image_path, "识别图片上的文字输出并解释其内容"))
