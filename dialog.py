#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests
import openai

try:
    from .digest.digest_app.parsings.common_interface import get_news
except ImportError:
    from digest.digest_app.parsings.common_interface import get_news

load_dotenv()

CLOUD_FOLDER = os.getenv("CLOUD_FOLDER")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_MODEL = os.getenv("CLOUD_MODEL")

client = openai.OpenAI(
    api_key=CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=CLOUD_FOLDER
)

def say():
    text = input('dialog.py> ')
    print('   ---   ')
    response = client.responses.create(
        model=f"gpt://{CLOUD_FOLDER}/{CLOUD_MODEL}",
        temperature=0.3,
        instructions=None,
        input=text,
        max_output_tokens=500
    )
    output = response.output_text
    print(output)
    print('   ---   ')

if __name__ == '__main__':
    while True:
        say()
