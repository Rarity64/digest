#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests
import openai
import sys
import time
import json
from .common_interface import get_news
from .llm_cache import get_cache, put_cache

load_dotenv()

CLOUD_FOLDER = os.getenv("CLOUD_FOLDER")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_MODEL = os.getenv("CLOUD_MODEL")
CLOUD_TIMEOUT = float(os.getenv("CLOUD_TIMEOUT", "30"))
CLOUD_MIN_SYMBOLS = int(os.getenv("CLOUD_MIN_SYMBOLS", "100"))
models = CLOUD_MODEL.split(sep=',')

client = openai.OpenAI(
    api_key = CLOUD_API_KEY,
    base_url = "https://ai.api.cloud.yandex.net/v1",
    project = CLOUD_FOLDER
)

please_prompt = """
Ты классификатор новостей.
Твоя задача — выбрать номера важных новостей.
Не объясняй выбор.
Не рассуждай.
Не добавляй текст.
Верни только валидный JSON вида {"numbers":[1,2,3]}.
"""

def get_important_news(source='habr'):
    if isinstance(source, list):
        news = source
    else:
        news  = get_news(source)
    titles = [i['title'] for i in news]
    urls = [i['url'] for i in news]

    user_prompt = f"""Выбери до 10 наиболее важных новостей.

    Не выбирай:
    - обзоры;
    - поздравления;
    - мнения и колонки;
    - рекламу;
    - малозначимые городские происшествия;
    - материалы без реально произошедшего события.

    Новости:
    {chr(20).join(f"{i + 1}. {titles[i]}" for i in range(len(news)))}

    Ответ строго в формате:
    {{"numbers":[1,2,3]}}
    """

    success = False
    cache = get_cache(user_prompt, source)
    if cache:
        success = True
    i = 0
    while success is False:
        cur_model = models[i]
        try:
            time_a = time.perf_counter()
            print(f'please_prompt: {please_prompt}')
            print(f'user_prompt: {user_prompt}')
            response = client.responses.create(
                model=f"gpt://{CLOUD_FOLDER}/{cur_model}",
                temperature=0.0,
                instructions=please_prompt,
                input=user_prompt,
                max_output_tokens=2000,
                timeout=CLOUD_TIMEOUT
            )
            time_b = time.perf_counter()
            t = time_b - time_a
            print(f'response.output_text: {response}')
            print(f'response.output_text: {response.output_text}')
            print(f'CLOUD_MIN_SYMBOLS: {CLOUD_MIN_SYMBOLS}')
            if response.output_text:
                success = True
            else:
                print(f'{cur_model} failed: too few symbols', file=sys.stdout)
        except openai.APIError as e:
            print(f'{cur_model} failed: {e}', file=sys.stderr)
            pass
        if success is True:
            print(f'{cur_model} succeeded in {t} seconds', file=sys.stderr)
        i += 1
        if i >= len(models):
            break
    if cache:
        output, model, t = cache
        print(f'{model} previously succeeded in {t} seconds', file=sys.stderr)
    else:
        output = response.output_text
        put_cache(user_prompt, output, source, cur_model, t)
    #'```\n{"numbers":[1,4,7,12,17,18,19]}\n```'
    output_object = json.loads(output)
    indexes = [i - 1 for i in output_object['numbers']]
    result = [news[i] for i in indexes]
    return result

sources = {
    'Хабр': 'habr',
    'Газета.ру': 'gazetaru',
    'Лента.ру': 'lentaru',
    'Коммерсантъ': 'kommersant',
    'Ведомости': 'vedomosti',
    'Башинформ': 'bashinform',
}
