#!/usr/bin/env python3
# soup.body.div.div.div.find_next_siblings(class_='grid')
# curl 'https://api.bashinform.ru/site/matters?rubric&kind=news_item&page=100' -H 'domain: www.bashinform.ru'
from bs4 import BeautifulSoup
import json
from .cached30min import get_cached_text
from .parse_bashinform import article_card_parse

def destructive_parse_a(a, out=dict):
    href = a.get('href')
    if not href:
        return None
    spans = a.find_all('span')
    texts = [i.text.strip() for i in spans]
    for i in spans:
        i.decompose()
    title = a.text.strip()
    obj = {
        'href': href,
        'title': title,
    }
    if len(texts) >= 1:
        obj['time'] = texts[0]
    if len(texts) >= 2:
        obj['section_text'] = texts[-1]
    result = article_card_parse(obj, out)
    return result

def main(href='/'):
    url = 'https://www.bashinform.ru' + href
    text = get_cached_text(url)
    soup = BeautifulSoup(text, 'lxml')
    news = soup.body.div.div.div.find_next_sibling(class_='grid')
    a_tags = news.find_all('a')
    result = []
    for i in a_tags:
        temp = destructive_parse_a(i, out=dict)
        if temp:
            result.append(temp)
    return result

if __name__ == '__main__':
    result = main()
    print(json.dumps(result, indent=4, ensure_ascii=False))
