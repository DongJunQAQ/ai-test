import base64
import os

from PIL import Image


def encode_image(image_path):  # 读取本地图片文件判断其是否为PNG格式，如果不是则将其转换为PNG格式，最后将图片转化为base64编码
    # 生成PNG输出路径（在原文件名后添加.png后缀）
    file_dir, file_name = os.path.split(image_path)  # 获取文件目录和文件名（包括后缀名）
    base_name, _ = os.path.splitext(file_name)  # 获取不包含后缀的文件名
    output_path = os.path.join(file_dir, f"{base_name}.png")  # 获取转换后缀后的文件路径
    with Image.open(image_path) as img:
        if img.format != "PNG":
            img.save(output_path, "PNG")
            print(f"已将图片从{img.format}格式转换为PNG")
            image_path = output_path  # 使用转换后的PNG路径
            # 读取并编码图片
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


encode_image("resource/image3.jpeg")
