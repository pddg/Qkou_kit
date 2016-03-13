# coding: utf-8
import re
import db_info
import db_cancel
from tweeter import format_info, format_cancel
import logging
import logging.config

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')


def add_info(Soup, q):
    try:
        for tr in Soup.findAll('tr', attrs={'class': re.compile('^gen_')}):
            td = tr.findAll('td')
            # タグ除去
            lec_info = map(text, td[3:11])
            # データベースに投げる
            info_id = db_info.add_info(*lec_info)
            if info_id is not False:
                lec_info.append(info_id)
                # Tweetする用に文章をフォーマット
                t = format_info(*lec_info)
                #キューに投入
                q.put(t)
            else:
                pass
    except Exception as e:
        log.exception(e)


def add_cancel(Soup, q):
    try:
        for tr in Soup.findAll('tr', attrs={'class': re.compile('^gen_')}):
            td = tr.findAll('td')
            # タグ除去
            lec_cancel = map(text, td[2:9])
            # データベースに投げる
            cancel_id = db_cancel.add_cancel(*lec_cancel)
            if cancel_id is not False:
                # Tweetする用に文章をフォーマット
                t = format_cancel(*lec_cancel)
                # キューに投入
                q.put(t)
            else:
                pass
    except Exception as e:
        log.exception(e)


def text(td):
    return td.text.strip()

