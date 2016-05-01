# coding: utf-8
import db_info
import db_cancel
import db_news
import hashlib
from tweeter import format_info, format_cancel, format_news
import settings

log = settings.log


def add_info_to_queue(q, *args):
    try:
        # 更新した数をカウント
        updated = 0
        for lec_info in args:
            id = db_info.add_info(*lec_info)
            if id is not False:
                lec_info.append(id)
                # Tweetする用に文章をフォーマット
                t = format_info(*lec_info)
                # キューに投入
                q.put(t)
                updated += 1
            else:
                pass
        else:
            # 更新した数を返す
            return updated
    except Exception as e:
        log.exception(e)


def add_cancel_to_queue(q, *args):
    try:
        # 更新した数をカウント
        updated = 0
        for lec_cancel in args:
            cancel_id = db_cancel.add_cancel(*lec_cancel)
            if cancel_id is not False:
                lec_cancel.append(cancel_id)
                # Tweetする用に文章をフォーマット
                t = format_cancel(*lec_cancel)
                # キューに投入
                q.put(t)
                updated += 1
            else:
                pass
        else:
            # 更新数を返す
            return updated
    except Exception as e:
        log.exception(e)


def add_news_to_queue(q, *args):
    try:
        # 更新した数をカウント
        updated = 0
        for news in args:
            news_id = db_news.add_news(*news)
            if news_id is not False:
                news.append(news_id)
                # Tweetする用に文章をフォーマット
                t = format_news(*news)
                # キューに投入
                q.put(t)
                updated += 1
            else:
                pass
        else:
            # 更新数を返す
            return updated
    except Exception as e:
        log.exception(e)
