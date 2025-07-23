import base64
import os

from PIL import Image
from openai import OpenAI


# 1.使用日志来记录执行步骤，以及日志打印顺序的问题；
# 2.图片在识别处理完成后清理临时文件；
# 3.多个平台测试os.path.split()和os.path.splitext()的功能；
# 4.添加处理图片的笔记(获取格式、修改格式)

def encode_image(image_path):  # 读取本地图片文件判断其是否为PNG格式，如果不是则将其转换为PNG格式，最后将图片转化为base64编码
    # 生成PNG输出路径（在原文件名后添加.png后缀）
    file_dir, file_name = os.path.split(image_path)  # 获取文件目录和文件名（包括后缀名），os.path.split()将路径分割为目录部分和文件名部分
    base_file_name, _ = os.path.splitext(file_name)  # 获取不包含后缀的文件名，os.path.splitext()将路径分割为文件名部分和扩展名部分
    output_path = os.path.join(file_dir, f"{base_file_name}.png")  # 获取转换后缀后的文件路径
    try:
        with Image.open(image_path) as img:
            if img.format != "PNG":
                img.save(output_path, "PNG")
                print(f"已将图片从{img.format}格式转换为PNG")
                image_path = output_path  # 使用转换后的PNG路径
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"图片处理错误: {e}")
        return None


def image_recognition(image_path, command):  # 图像识别
    print("开始交给大模型处理")
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
    local_image_path = "resource/image4.jpg"  # 本地图片路径
    print(image_recognition(local_image_path, "描述一下图片"))
