# coding: utf-8
import lib.login
import re
from datetime import datetime, timedelta
from icalendar import Calendar, Event, vDate
import os


def get_plan(html):
    events = []
    for tr in html.findAll('tr', attrs={'class': re.compile('^gen_tbl')}):
        td = tr.findAll('td')
        plans = map(text, td[0:3])
        r = '(\d{4})/(\d{1,2})/(\d{1,2})'
        date_pattern = re.compile(r)
        match_r = re.findall(date_pattern, plans[0])
        if len(match_r) > 1:
            dates = []
            for date in match_r:
                y, m, d = date
                date = map(integer, [y, m, d])
                dates.append(date)
            start_day = dates[0]
            end_day = dates[1]
            event = create_event(start_day, end_day, plans[1], plans[2])
        else:
            for date in match_r:
                y, m, d = date
                date = map(integer, [y, m, d])
                event = create_event(date, plans[1], plans[2])
        events.append(event)
    else:
        return events


def create_event(*args):
    event = Event()
    # 一日だけの予定と数日に渡った予定で場合分け
    if len(args) > 3:
        start = args[0]
        end = args[1]
        d = datetime(*end)
        # 2日以上に渡った予定では終了日を一日伸ばさないとインポートしたとき一日短くなってしまう
        d += timedelta(days=1)
        event.add('summary', args[2])
        event.add('description', args[3])
        event.add('dtstart', vDate(datetime(*start)))
        event.add('dtend', vDate(d))
    else:
        date = args[0]
        event.add('summary', args[1])
        event.add('description', args[2])
        event.add('dtstart', vDate(datetime(*date)))
        event.add('dtend', vDate(datetime(*date)))
    return event


def text(td):
    return td.text.strip()


def integer(date):
    return int(date)

if __name__ == "__main__":
    ical = Calendar()
    ical.add('prodid', '-//poyo.info//Qkou_kit//')
    ical.add('version', '2.0')
    html = lib.login.soupinfo("?c=cur_schedule_ug")
    events = get_plan(html)
    for event in events:
        ical.add_component(event)
    directory = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(directory, 'kit_events.ics'), 'wb')
    f.write(ical.to_ical())
    f.close()
