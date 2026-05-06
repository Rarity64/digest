#!/usr/bin/env python3
import habr
import gazetaru
import lentaru
import kommersant
import vedomosti
import bashinform

def habr_get():
    from_habr = sum((habr.main(i) for i in range(50)), [])
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

def kommersant_get():
    from_kommersant = kommersant.get_newsline()
    result = [
        {
            'title': i['Title'] + '. ' + i['Subtitle'],
            'url': f'https://www.kommersant.ru/doc/{i['DocId']}',
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
