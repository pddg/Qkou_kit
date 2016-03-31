# coding: utf-8
import re
import db_info
import db_cancel
import db_news
from tweeter import format_info, format_cancel, format_news
import logging
import logging.config

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')


def add_info(html, q):
    try:
        for tr in html.findAll('tr', attrs={'class': re.compile('^gen_')}):
            td = tr.findAll('td')
            # タグ除去
            lec_info = map(text, td[3:11])
            # データベースに投げる
            info_id = db_info.add_info(*lec_info)
            if info_id is not False:
                lec_info.append(info_id)
                # Tweetする用に文章をフォーマット
                t = format_info(*lec_info)
                # キューに投入
                q.put(t)
            else:
                pass
    except Exception as e:
        log.exception(e)


def add_cancel(html, q):
    try:
        for tr in html.findAll('tr', attrs={'class': re.compile('^gen_')}):
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


def add_news(html, q):
    try:
        now_notice = html.find('div', attrs={'id': 'now_notice_area'})
        for tr in now_notice.findAll('tr'):
            td = tr.findAll('td')
            news = map(text, td[0:2])
            # 文中にlinkが存在するか確認
            if td[1].a is not None:
                link = td[1].a.get('href')
            else:
                link = u''
            news.append(link)
            news_id = db_news.add_news(*news)
            if news_id is not False:
                news.append(news_id)
                # Tweetする用に文章をフォーマット
                t = format_news(*news)
                # キューに投入
                q.put(t)
            else:
                pass
    except Exception as e:
        log.exception(e)


def text(td):
    return td.text.strip()
