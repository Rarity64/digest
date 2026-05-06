#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

cache_path = 'cache'
if 'CACHE_PATH' in os.environ:
    cache_path = os.environ['CACHE_PATH']

def get_cached_text(url):
    filename = url.replace("://", "_").replace("/", "_").replace("?", "_")
    if Path(cache_path).is_dir():
        filepath = cache_path + '/' + filename
        if Path(filepath).is_file():
            mtime = os.path.getmtime(filepath)
            seconds_ago = time.time() - mtime
            if seconds_ago < 1800:
                with open(cache_path + '/' + filename) as f:
                    return f.read()
    else:
        Path(cache_path).mkdir(exist_ok=True)
    with open(cache_path + '/' + filename, 'w') as f:
        print(f'new visit: {url}', file=sys.stderr)
        f.write(requests.get(url).text)
    with open(cache_path + '/' + filename) as f:
        return f.read()

def main(page=1):
    url = 'https://habr.com/'
    if page > 1:
        url += f'ru/feed/page{page}/'
    text = get_cached_text(url)
    soup = BeautifulSoup(text, 'lxml')
    articles = soup.find_all('article')
    if not (len(articles) > 2):
        raise Exception("Weird, not more than 2 <article>s")
    result = []
    for i in articles:
        info = {}
        i_type = i.span.text
        # 'Статья', 'Пост' или 'Новость'
        info['type'] = i_type
        if i_type == 'Пост':
            i_title = i.p.text
        else:
            i_title = i.h2.text
        # заголовок
        info['title'] = i_title
        result.append(info)
    return result

if __name__ == '__main__':
    pages = []
    for i in range(1, 51):
        print(f'{i}/50', file=sys.stderr, end='\r', flush=True)
        pages.append(main(page=i))
    print(file=sys.stderr)
    #print(json.dumps(pages, indent=4, ensure_ascii=False))
    for i in pages:
        for j in i:
            print(j['title'])

