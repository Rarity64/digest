#!/usr/bin/env python3
import psycopg
import datetime
import sys
import os
import json

def bashinform_href_parse(href):
    parts = [i.split(sep='-') for i in href.split(sep='/')]
    if len(parts) < 1 or parts[0] != ['']:
        return None
    result = []
    for i in parts[1:]:
        if len(i) == 3 and sum(j.isdigit() for j in i) == 3:
            result.append(datetime.date(*map(int, i)))
            continue
        if len(i) > 0 and i[-1].isdigit():
            name = '-'.join(i[:-1])
            article_id = int(i[-1])
            result.append((name, article_id))
            continue
        result.append('-'.join(i))
    return result

def parse_time_as_time(time):
    try:
        result = datetime.datetime.strptime(time, '%H:%M')
        return result.time()
    except ValueError:
        return None

def parse_time_as_date(time):
    try:
        result = datetime.datetime.strptime(time, '%d.%m.%Y')
        return result.date()
    except ValueError:
        return None

month_in_russian_genetive = {
    'Января': 1,
    'Февраля': 2,
    'Марта': 3,
    'Апреля': 4,
    'Мая': 5,
    'Июня': 6,
    'Июля': 7,
    'Августа': 8,
    'Сентября': 9,
    'Октября': 10,
    'Ноября': 11,
    'Декабря': 12,
}

def parse_time_as_day_month(time):
    result = time.split()
    if len(result) != 2:
        return None
    if not result[0].isdigit():
        return None
    day = int(result[0])
    if result[1] not in month_in_russian_genetive:
        return None
    month = month_in_russian_genetive[result[1]]
    return day, month

class Card:
    def __init__(self, obj=None):
        self.title = None
        self.href = None
        self.level1section = None
        self.level2section = None
        self.date = None
        self.time = None
        self.section_text = None
        self.translit = None
        self.article_id = None
        self.weird = False
        self.datetime = None
        if obj:
            self.title = obj.get('title')
            self.href = obj.get('href')
            if self.href:
                parsed = bashinform_href_parse(self.href)
                if parsed is None:
                    self.weird = True
                else:
                    if len(parsed) >= 1 and isinstance(parsed[0], str):
                        self.level1section = parsed[0]
                    if len(parsed) >= 2 and isinstance(parsed[1], str):
                        self.level2section = parsed[1]
                    if len(parsed) >= 1 and isinstance(parsed[-1], tuple):
                        self.translit, self.article_id = parsed[-1]
                    for i in parsed:
                        if isinstance(i, datetime.date):
                            self.date = i
                            break
            self.time = obj.get('time')
            if self.time:
                time = parse_time_as_time(self.time)
                date = parse_time_as_date(self.time)
                day_month = parse_time_as_day_month(self.time)
                if time:
                    self.time = time
                elif date:
                    if date != self.date:
                        self.time = date
                        self.weird = True
                elif day_month:
                    if day_month != (self.date.day, self.date.month):
                        self.time = day_month
                        self.weird = True
                else:
                    self.weird = True
            self.section_text = obj.get('section_text')
            we_have_date = isinstance(self.date, datetime.date)
            we_have_time = isinstance(self.time, datetime.time)
            if we_have_date and we_have_time:
                dt = datetime.datetime.combine(self.date, self.time)
                self.datetime = dt

def article_card_parse(obj, out=dict):
    card = Card(obj)
    if card.weird or not card.article_id:
        return None
    if out == Card:
        return card
    out_obj = {
        'title': card.title,
        'href': card.href,
    }
    if card.level1section:
        out_obj['level1'] = card.level1section
    if card.level2section:
        out_obj['level2'] = card.level2section
    if card.date and isinstance(card.date, datetime.date):
        out_obj['date'] = card.date.strftime('%Y-%m-%d')
    if card.time and isinstance(card.time, datetime.time):
        out_obj['time'] = card.time.strftime('%H:%M')
    if card.datetime and isinstance(card.datetime, datetime.datetime):
        out_obj['datetime'] = card.datetime.strftime('%Y-%m-%d %H:%M')
    if card.section_text:
        out_obj['section_text'] = card.section_text
    if card.article_id:
        out_obj['id'] = card.article_id
    if out == dict:
        return out_obj
    if out == str:
        return json.dumps(out_obj, indent=4, ensure_ascii=False)
    return out_obj
