# 1. setup API
create a file called .env

add the following contents

OPENAI_API_KEY=your_openai_api

STABILITY_API_KEY=your_stability_api

# 2. Install libraries
pip install -r requirements.txt

# 3. Check the environments
python check_environment.py

Expected result

✅ 正在检查必要库的安装状态...

✅ 成功导入：openai
✅ 成功导入：requests
✅ 成功导入：huggingface_hub
pygame 2.6.1 (SDL 2.28.4, Python 3.10.16)
Hello from the pygame community. https://www.pygame.org/contribute.html
✅ 成功导入：pygame
✅ 成功导入：yaml
✅ 成功导入：dotenv
✅ 成功导入：gradio
✅ 成功导入：PIL
✅ 实际导入 pyyaml 成功

✅ 库导入检查完毕。

🔄 尝试调用 OpenAI（新版 SDK）...
✅ OpenAI 成功返回示例文本：

大家好，我是galgame中的女主角。我的名字是小雨，我是一个活泼可爱的女孩子。我喜欢画画，弹钢琴和唱歌。我的梦想是成为一名音乐家，让我的音乐传达我的情感和故事给大家。虽然有时候我

🔄 尝试调用 Stability AI API（稳定模型）...
Sending REST request to https://api.stability.ai/v2beta/stable-image/generate/core...
✅ Stability AI 图像请求成功（内容为二进制图像）
🖼️ 图像已保存为 test_output.png

