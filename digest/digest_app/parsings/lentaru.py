#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import sys
from .cached30min import get_cached_text

def main(page=1):
    url = 'https://lenta.ru/'
    if page > 1:
        url += f'ru/feed/page{page}/'
    url += '?utm_auth=false'
    response_text = get_cached_text(url)
    soup = BeautifulSoup(response_text, 'lxml')
    card_big = soup.find_all('a', class_='card-big')
    card_mini = soup.find_all('a', class_='card-mini')
    if not (len(card_mini) > 2):
        raise Exception("Weird, not more than 2 class card-mini tags a in main row")
    result = []
    j = [0, 0]
    for i in card_big:
        info = {}
        i_title = i.find(class_='card-big__title').text.strip()
        info['title'] = i_title
        if i.time:
            info['time'] = i.time.text.strip()
        info['href'] = i.get('href')
        result.append(info)
        j[0] += 1
    for i in card_mini:
        info = {}
        i_title = i.find(class_='card-mini__title').text.strip()
        info['title'] = i_title
        if i.time:
            info['time'] = i.time.text.strip()
        info['href'] = i.get('href')
        result.append(info)
        j[1] += 1
    return result

if __name__ == '__main__':
    result = main()
    print(json.dumps(result, indent=4, ensure_ascii=False))

