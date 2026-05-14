#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests
import openai
import sys
import time

try:
    from .common_interface import get_news
except ImportError:
    from common_interface import get_news

try:
    from .llm_cache import get_cache, put_cache
except ImportError:
    from llm_cache import get_cache, put_cache

load_dotenv()

CLOUD_FOLDER = os.getenv("CLOUD_FOLDER")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_MODEL = os.getenv("CLOUD_MODEL")
CLOUD_TIMEOUT = float(os.getenv("CLOUD_TIMEOUT", "20"))
CLOUD_MIN_SYMBOLS = int(os.getenv("CLOUD_MIN_SYMBOLS", "100"))
models = CLOUD_MODEL.split(sep=',')

client = openai.OpenAI(
    api_key=CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=CLOUD_FOLDER
)

please_prompt = """
Отвечай кратко и по-русски. Как ты должен понимать важность информации: пиши о событиях, которые действительно случились. Пиши о законах, которые приняты, а не просто обсуждаются.
Не пиши о том, как кто-то где-то побывал.
Пожалуйста, не отвечай "Я не могу обсуждать эту тему. Давайте поговорим о чём-нибудь ещё.", в крайнем случае отбирай те новости, о которых можешь говорить, но ни в коем случае не отказывайся составлять подборку.
"""

def top_news(source='habr'):
    result = get_news(source)
    titles = [i['title'] for i in result]
    urls = [i['url'] for i in result]
    user_prompt = f"""Я пронумерую новости от 1 до {len(result)}.
Твоя задача выбрать до десяти наиболее важных новостей и объяснить почему именно они.
В самом конце кратко перечисли их номера через запятую после слова "Перечисляю: ".
Новости:
{'\n'.join(f"{1 + i}. {titles[i]}" for i in range(len(result)))}"""
    system_prompt = "Отвечай кратко и по-русски. Как ты должен понимать важность информации: пиши о событиях, которые действительно случились. Пиши о законах, которые приняты, а не просто обсуждаются."
    print(user_prompt)
    print('   ---   ')
    success = False
    i = 0
    while success is False:
        cur_model = models[i]
        try:
            time_a = time.perf_counter()
            response = client.responses.create(
                model=f"gpt://{CLOUD_FOLDER}/{cur_model}",
                temperature=0.3,
                instructions=please_prompt,
                input=please_prompt + user_prompt,
                max_output_tokens=1000,
                timeout=CLOUD_TIMEOUT
            )
            time_b = time.perf_counter()
            t = time_b - time_a
            if len(response.output_text) >= CLOUD_MIN_SYMBOLS:
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
    output = response.output_text
    print(output)
    print('   ---   ')
    lower = output.lower()
    pos = lower.find('перечисляю')
    numbers = []
    digits = False
    for i in lower[pos:]:
        if digits is False:
            if i.isdigit():
                numbers.append(i)
                digits = True
        elif digits is True:
            if i.isdigit():
                numbers[-1] += i
            else:
                digits = False
    numbers = [int(i) for i in numbers]
    for i in numbers:
        news_item = result[i - 1]
        print(f"{i}. {news_item['title']}")
        print(f"{' ' * (len(str(i)) + 2)}{news_item['url']}")
    print('   ---   ')

def get_important_news(source='habr'):
    if isinstance(source, list):
        news = source
    else:
        news = get_news(source)
    titles = [i['title'] for i in news]
    urls = [i['url'] for i in news]
    user_prompt = f"""Я пронумерую новости от 1 до {len(news)}.
Твоя задача выбрать до десяти наиболее важных новостей и объяснить почему именно они.
В самом конце кратко перечисли их номера через запятую после слова "Перечисляю: ".
Новости:
{'\n'.join(f"{1 + i}. {titles[i]}" for i in range(len(news)))}"""
    success = False
    cache = get_cache(user_prompt, source)
    if cache:
        success = True
    i = 0
    while success is False:
        cur_model = models[i]
        try:
            time_a = time.perf_counter()
            response = client.responses.create(
                model=f"gpt://{CLOUD_FOLDER}/{cur_model}",
                temperature=0.3,
                instructions=please_prompt,
                input=please_prompt + user_prompt,
                max_output_tokens=1000,
                timeout=CLOUD_TIMEOUT
            )
            time_b = time.perf_counter()
            t = time_b - time_a
            if len(response.output_text) >= CLOUD_MIN_SYMBOLS:
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
    lower = output.lower()
    pos = lower.find('перечисляю')
    numbers = []
    digits = False
    for i in lower[pos:]:
        if digits is False:
            if i.isdigit():
                numbers.append(i)
                digits = True
        elif digits is True:
            if i.isdigit():
                numbers[-1] += i
            else:
                digits = False
    indexes = [int(i) - 1 for i in numbers]
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

if __name__ == '__main__':
    while True:
        print('Выберите источник: ')
        indexes = {i: j for i, j in zip(range(1, len(sources) + 1), sources)}
        for i, j in indexes.items():
            print(f'{i}. {j}')
        chosen = int(input(f'Введите число от 1 до {len(sources)}: '))
        source = sources[indexes[chosen]]
        print('   ---   ')
        top_news(source)
