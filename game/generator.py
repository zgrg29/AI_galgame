# game/generator.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculate_current_word_count(previous_dialog):
    """计算当前对话部分的字数"""
    return len(previous_dialog.split())  # 使用空格分隔计算字数

def generate_prompt(settings, previous_dialog=""):
    # 计算当前的字数
    current_word_count = calculate_current_word_count(previous_dialog)
    
    # 生成角色设定
    characters = "\n".join(
        [f"{i+1}. {char['name']}: {char['desc']}" for i, char in enumerate(settings["characters"])]
    )

    # 根据游戏时长估算字数
    estimated_words = settings['duration'] * 100  # 设定每分钟约100字，可以根据需要调整

    prompt = f"""
You are a visual novel writer. Please write the next scene of a galgame (dating sim) in the **same language as the player's input**.

Estimated play time: {settings['duration']} minutes
Current story progress: {str(round(100 * current_word_count / estimated_words))}%

Story setting:
{settings['plot']}

Characters:
{characters}

Previous dialog:
{previous_dialog}

Instructions:
- This is a **continuous and immersive story**, not a summary.
- Focus **primarily on dialogue** between the characters. The story should progress through **realistic, emotionally nuanced conversation**.
- **Minimize the amount of narration or description**; the story should mostly unfold through **dialogue-driven interactions**.
- The player is the protagonist, so the narration should focus on the player's inner thoughts when necessary, but **dialogue should drive the story forward**.
- **Slowly pace the story**, but avoid rushing. Don't resolve major conflicts too quickly, and don't skip ahead in time.
- Use **first-person narration** for the player's thoughts and emotions, but the characters should be the focus through their interactions.
- **Avoid long-winded explanations** or excessive narrative. Instead, focus on short, impactful lines of dialogue.
- Keep the tone immersive and fitting for a **visual novel**: alternating between dialogue and small introspective moments.
- Make sure the dialogue reveals emotional depth and character development.
- Do not end the scene, skip ahead in the plot, or resolve any major story arcs in this part of the narrative.

Important:
Write the story in the **same language as the player's input above**.
"""
    return prompt.strip()

def generate_next_dialog(settings, previous_dialog):
    try:
        # 每次调用时生成下一部分对话
        prompt = generate_prompt(settings, previous_dialog)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=800  # 每次生成最多800个token
        )
        content = response.choices[0].message.content
        dialog_lines = content.split("\n")
        return [line.strip() for line in dialog_lines if line.strip() != ""]
    except Exception as e:
        return [f"[ERROR] Failed to generate dialog: {e}"]
