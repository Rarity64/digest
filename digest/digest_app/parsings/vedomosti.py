#!/usr/bin/env python3
from .cached30min import get_cached_text
from bs4 import BeautifulSoup
import json

def simple_vedomosti():
    url = 'https://api.vedomosti.ru/v2/lists/main-top'
    text = get_cached_text(url)
    parsed = json.loads(text)
    obj = [
        {
            'title': i['title'],
            'subtitle': i['subtitle'],
            'time': i['published_at'],
            'url': i['url'],
            'id': i['id'],
        }
        for i in parsed['list']['documents']
    ]
    return obj

if __name__ == '__main__':
    result = simple_vedomosti()
    print(json.dumps(result, indent=4, ensure_ascii=False))
