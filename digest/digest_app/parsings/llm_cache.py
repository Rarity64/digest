#!/usr/bin/env python3
import json
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

cache_path = 'cache'
if 'CACHE_PATH' in os.environ:
    cache_path = os.environ['CACHE_PATH']

def filename_hash(obj):
    payload_str = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
    payload_bytes = payload_str.encode('utf-8')
    payload_hash = hashlib.blake2b(payload_bytes, digest_size=8).hexdigest()
    return payload_hash

def get_cache(inp, topic=None):
    if not topic:
        topic = filename_hash(inp)
    search_by = inp if isinstance(inp, str) else filename_hash(inp)
    filename = 'llm_cache_' + topic + '.json'
    Path(cache_path).mkdir(exist_ok=True)
    fullname = cache_path + '/' + filename
    if not Path(fullname).is_file():
        return None
    with open(fullname, encoding='utf-8') as f:
        content = f.read()
    obj = json.loads(content)
    if obj['input'] != search_by:
        return None
    return obj['output'], obj['model'], obj['time']

def put_cache(inp, out, topic=None, model=None, time=None):
    if not topic:
        topic = filename_hash(inp)
    search_by = inp if isinstance(inp, str) else filename_hash(inp)
    filename = 'llm_cache_' + topic + '.json'
    Path(cache_path).mkdir(exist_ok=True)
    fullname = cache_path + '/' + filename
    obj = {
        'input': search_by,
        'output': out,
        'model': model,
        'time': time,
    }
    with open(fullname, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, separators=(',', ':'), ensure_ascii=False))

def clear_cache(topic=None, inp=None):
    if not topic:
        if not inp:
            for filepath in Path(cache_path).glob('llm_cache_*.json'):
                filepath.unlink()
            return
        topic = filename_hash(inp)
    filename = 'llm_cache_' + topic + '.json'
    fullname = cache_path + '/' + filename
    if Path(fullname).is_file():
        Path(fullname).unlink()
