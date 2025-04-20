import importlib
import os
import sys
import json
import time
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

print("✅ 正在检查必要库的安装状态...\n")

modules = [
    "openai", "requests", "PyQt6", "yaml", "dotenv", "gradio", "PIL"
]

for module in modules:
    try:
        importlib.import_module(module)
        print(f"✅ 成功导入：{module}")
    except ImportError:
        print(f"❌ 未安装或导入失败：{module}")

# 特别检查 pyyaml 实际导入
try:
    import yaml
except ImportError:
    print("❌ 实际导入 pyyaml 失败")
else:
    print("✅ 实际导入 pyyaml 成功")

print("\n✅ 库导入检查完毕。\n")

# 加载环境变量
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
STABILITY_KEY = os.getenv("STABILITY_API_KEY")

# ----------------- OpenAI 测试 ------------------
print("🔄 尝试调用 OpenAI（新版 SDK）...")

try:
    from openai import OpenAI

    client = OpenAI(api_key=openai_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "请用中文写一个galgame女主角的自我介绍"}],
        max_tokens=100,
    )

    result = response.choices[0].message.content.strip()
    print("✅ OpenAI 成功返回示例文本：\n")
    print(result + "\n")

except Exception as e:
    print(f"❌ OpenAI 测试失败：{e}\n")

# ----------------- Stability AI 测试 ------------------

def send_generation_request(
    host,
    params,
    files = None
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    if files is None:
        files = {}

    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image:
        files["image"] = open(image, 'rb')
    if mask:
        files["mask"] = open(mask, 'rb')
    if not files:
        files["none"] = ''

    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

print("🔄 尝试调用 Stability AI API（稳定模型）...")

try:
    prompt = "op art cat illusion red blue chromostereopsis maximum saturation"
    negative_prompt = ""
    aspect_ratio = "21:9"
    style_preset = "None"
    seed = 0
    output_format = "jpeg"

    host = f"https://api.stability.ai/v2beta/stable-image/generate/core"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format": output_format
    }

    if style_preset != "None":
        params["style_preset"] = style_preset

    response = send_generation_request(
        host,
        params
    )

    if response.status_code == 200:
        print("✅ Stability AI 图像请求成功（内容为二进制图像）")
        image = Image.open(BytesIO(response.content))
        image.save("test_output.png")
        print("🖼️ 图像已保存为 test_output.png")
    elif response.status_code == 401:
        print("❌ 请求失败：未授权（401），请检查 API 密钥是否正确。")
    else:
        print(f"❌ 请求失败，状态码：{response.status_code}")
        print("响应内容:", response.text[:200])

except Exception as e:
    print(f"❌ 请求异常：{e}")
