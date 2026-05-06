#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import sys
from cached30min import get_cached_text

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
        link = i.find('a', class_='tm-article-datetime-published')
        if link:
            info['href'] = link.get('href')
        result.append(info)
    return result

if __name__ == '__main__':
    pages = []
    for i in range(1, 51):
        print(f'{i}/50', file=sys.stderr, end='\r', flush=True)
        pages.append(main(page=i))
    print(file=sys.stderr)
    print(json.dumps(pages, indent=4, ensure_ascii=False))

