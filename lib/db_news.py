# coding: utf-8
from sqlalchemy import and_
import datetime
import models
import settings

log = settings.log


def add_news(update, detail, link, unique_hash):
    session = models.Session()
    qkou = session.query(models.News)
    # utf-8にエンコードしないとエラー
    update = update.encode('utf-8')
    detail = detail.encode('utf-8')
    unique_hash = unique_hash.encode('utf-8')
    if len(link) is not 0:
        link = link.encode('utf-8')
    newinfo = models.News(update, detail, link, unique_hash, settings.now)
    try:
        ex_info = qkou.filter(models.News.unique_hash == unique_hash).first()
        if ex_info is None:
            # 新規の場合
            log.debug('News: %s %s … [新規]', update, detail[0:10])
            session.add(newinfo)
            session.commit()
            new_id = newinfo.id
            return new_id
        else:
            # 既存の場合
            log.debug('News: %s %s … [既存]', update, detail[0:10])
            ex_info.up_time = settings.now
            session.commit()
            return False
    except Exception as e:
        log.exception(e)
        return False
    finally:
        session.close()


def del_old_news():
    session = models.Session()
    qkou = session.query(models.News)
    yday = settings.now - datetime.timedelta(days=1)
    try:
        qkou.filter(models.News.up_time < yday).delete()
        session.commit()
        log.debug('[ GetNewsThread ] 最終更新が%s以前の古いデータを削除', yday)
    except Exception as e:
        log.exception(e)
    finally:
        session.close()


def id_news(id):
    session = models.Session()
    qkou = session.query(models.News)
    try:
        news_info = qkou.filter(models.News.id == id).first()
        if news_info is not None:
            return news_info
        else:
            return 0
    except Exception as e:
        log.exception(e)
        return False
    finally:
        session.close()
