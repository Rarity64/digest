#!/usr/bin/env python3
from .cached30min import get_cached_text
import time
import json

def get_newsline():
    url = 'https://www.kommersant.ru/news/newsline'
    newsline = get_cached_text(url)
    result = json.loads(newsline)['docs']
    return result

if __name__ == '__main__':
    result = get_newsline()
    print(json.dumps(result, indent=4, ensure_ascii=False))

