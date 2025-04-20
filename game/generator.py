# game/generator.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_prompt(settings):
    characters = "\n".join(
        [f"{i+1}. {char['name']}: {char['desc']}" for i, char in enumerate(settings["characters"])]
    )

    prompt = f"""
You are a visual novel writer. Please write the first scene of a galgame (dating sim) in the **same language as the player's input**.

Estimated play time: {settings['duration']} minutes

Story setting:
{settings['plot']}

Characters:
{characters}

Requirements:
- Use first-person narration (player is the main character)
- Include dialogue and emotional tone
- Break text into short readable segments (like visual novels)
- Keep it immersive, like in real galgames

Write the story in the same language as the input above.
"""

    return prompt.strip()


def generate_dialog(settings):
    try:
        prompt = generate_prompt(settings)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=800
        )
        content = response["choices"][0]["message"]["content"]
        dialog_lines = content.split("\n")
        return [line.strip() for line in dialog_lines if line.strip() != ""]
    except Exception as e:
        return [f"[ERROR] Failed to generate dialog: {e}"]
