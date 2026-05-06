#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import sys
from cached30min import get_cached_text

def main(page=1):
    url = 'https://www.gazeta.ru/'
    if page > 1:
        url += f'ru/feed/page{page}/'
    url += '?utm_auth=false'
    response_text = get_cached_text(url)
    soup = BeautifulSoup(response_text, 'lxml')
    main_part = soup.find(id='_id_gazeta_main_article')
    main_row = main_part.find(class_='row')
    main_siblings = main_row.find_next_siblings(class_=['row', 'b_photo_digest'])
    main_b_ear = main_part.find_all('a', class_='b_ear')
    if not (len(main_b_ear) > 2):
        raise Exception("Weird, not more than 2 class b_ear tags a in main row")
    result = []
    j = 0
    for i in main_b_ear:
        info = {}
        i_title = i.find(class_='b_ear-title').text.strip()
        info['title'] = i_title
        info['data-essence'] = i.get('data-essence')
        if i.time:
            info['time'] = i.time.text.strip()
        info['href'] = i.get('href')
        result.append(info)
        j += 1
    return result

if __name__ == '__main__':
    result = main()
    print(json.dumps(result, indent=4, ensure_ascii=False))

