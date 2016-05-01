# coding: utf-8
from sqlalchemy import and_
import datetime
import models
import settings

log = settings.log
now = settings.now


def add_cancel(subject, teacher, day, week, period, abstract, first, unique_hash):
    session = models.Session()
    qkou = session.query(models.Cancel)
    # utf-8にエンコードしないとエラー
    subject = subject.encode('utf-8')
    teacher = teacher.encode('utf-8')
    day = day.encode('utf-8')
    week = week.encode('utf-8')
    period = period.encode('utf-8')
    abstract = abstract.encode('utf-8')
    first = first.encode('utf-8')
    unique_hash = unique_hash.encode('utf-8')
    newcancel = models.Cancel(
        subject, teacher, day, week, period, abstract, first, unique_hash, now)
    try:
        ex_cancel = qkou.filter(
            models.Cancel.unique_hash == unique_hash).first()
        if ex_cancel is None:
            # 新規の場合
            log.debug('授業名: %s … [新規]', subject)
            session.add(newcancel)
            session.commit()
            new_id = newcancel.id
            return new_id
        else:
            # 既存の場合
            log.debug('授業名: %s … [既存]', subject)
            # データが存在する場合日時を記録
            ex_cancel.up_time = now
            session.commit()
            return False
    except Exception as e:
        session.rollback()
        log.exception(e)
        return False
    finally:
        session.close()


def del_old_cancel():
    session = models.Session()
    qkou = session.query(models.Cancel)
    yday = now - datetime.timedelta(days=1)
    try:
        qkou.filter(models.Cancel.up_time < yday).delete()
        session.commit()
        log.debug('[ GetCancelThread ] 最終更新が%s以前の古いデータを削除', yday)
    except Exception as e:
        log.exception(e)
    finally:
        session.close()


def id_cancel(id):
    session = models.Session()
    qkou = session.query(models.Cancel)
    try:
        cancel_info = qkou.filter(models.Cancel.id == id).first()
        if cancel_info is not None:
            return cancel_info
        else:
            return 0
    except Exception as e:
        log.exception(e)
        return False
    finally:
        session.close()


# 日付から検索してデータを取得し教科名を返す
def todayinfo(day):
    infolist = []
    session = models.Session()
    for info in session.query(models.Cancel).filter(models.Cancel.day == day).all():
        infolist.append(info.subject)
    session.close()
    return infolist
