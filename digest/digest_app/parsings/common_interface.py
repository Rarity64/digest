#!/usr/bin/env python3
from . import habr
from . import gazetaru
from . import lentaru
from . import kommersant
from . import vedomosti
from . import bashinform
import sys

def habr_get():
    from_habr = sum((habr.main(i) for i in range(1, 2)), [])
    result = [
        {
            'title': i['title'],
            'url': 'https://habr.com' + i['href'],
        }
        for i in from_habr
    ]
    return result

def gazetaru_get():
    from_gazetaru = gazetaru.main()
    result = [
        {
            'title': i['title'],
            'url': 'https://www.gazeta.ru' + i['href'],
        }
        for i in from_gazetaru
    ]
    return result

def lentaru_get():
    from_lentaru = lentaru.main()
    result = [
        {
            'title': i['title'],
            'url': 'https://lenta.ru' + i['href'],
        }
        for i in from_lentaru
    ]
    return result

def kommersant_title(i):
    title = i['Title']
    subtitle = i['Subtitle']
    if isinstance(title, list):
        print('Title:', title, file=sys.stderr)
        title = '; '.join(title)
    if isinstance(subtitle, list):
        print('Subtitle:', subtitle, file=sys.stderr)
        subtitle = '; '.join(subtitle)
    if title and subtitle:
        return title + '. ' + subtitle
    elif title:
        return title
    elif subtitle:
        return subtitle
    return ''

def kommersant_get():
    from_kommersant = kommersant.get_newsline()
    result = [
        {
            'title': kommersant_title(i),
            'url': f'https://www.kommersant.ru/doc/{i["DocId"]}',
        }
        for i in from_kommersant
    ]
    return result

def vedomosti_get():
    from_vedomosti = vedomosti.simple_vedomosti()
    result = [
        {
            'title': i['title'] + '. ' + i['subtitle'],
            'url': 'https://www.' + i['url'],
        }
        for i in from_vedomosti
    ]
    return result

def bashinform_get():
    from_bashinform = bashinform.main()
    result = [
        {
            'title': i['title'],
            'url': 'https://www.bashinform.ru' + i['href'],
        }
        for i in from_bashinform
    ]
    return result

name_to_function = {
    'habr': habr_get,
    'gazetaru': gazetaru_get,
    'lentaru': lentaru_get,
    'kommersant': kommersant_get,
    'vedomosti': vedomosti_get,
    'bashinform': bashinform_get,
}

def get_news(source='habr'):
    return name_to_function[source]()
