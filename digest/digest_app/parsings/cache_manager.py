#!/usr/bin/env python3
import os
import sys
from . import cached30min
from . import llm_cache
from dotenv import load_dotenv

load_dotenv()

CLEAR_CACHE = os.getenv('CLEAR_CACHE')
if isinstance(CLEAR_CACHE, str):
    normalized = CLEAR_CACHE.strip().lower()
    if normalized in ['false', 'disable', 'disabled', 'off', '0']:
        CLEAR_CACHE = False

site_urls = {
    'habr': 'https://habr.com/*',
    'gazetaru': 'https://www.gazeta.ru/*',
    'lentaru': 'https://lenta.ru/*',
    'kommersant': 'https://www.kommersant.ru/*',
    'vedomosti': 'https://api.vedomosti.ru/*',
    'bashinform': 'https://www.bashinform.ru/*',
}

def clear_cache(source=None, kinds='site,llm'):
    if not kinds:
        kinds = 'site,llm'
    if 'site' in kinds:
        if source:
            cached30min.clear_cache(site_urls[source])
        else:
            cached30min.clear_cache()
    if 'llm' in kinds:
        if source:
            llm_cache.clear_cache(source)
        else:
            llm_cache.clear_cache()

if CLEAR_CACHE:
    clear_cache()

if __name__ == '__main__':
    source = input('Enter source: ')
    kinds = input('Enter kinds of cache (site and llm are available): ')
    clear_cache(source, kinds)
