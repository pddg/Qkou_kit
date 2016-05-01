# coding: utf-8
from sqlalchemy import and_
import datetime
import models
import settings

log = settings.log
now = settings.now


def add_info(subject, teacher, week, period, abstract, detail, first, update, unique_hash, renew_hash):
    session = models.Session()
    qkou = session.query(models.Info)
    # utf-8にエンコードしないとエラー
    subject = subject.encode('utf-8')
    teacher = teacher.encode('utf-8')
    week = week.encode('utf-8')
    period = period.encode('utf-8')
    abstract = abstract.encode('utf-8')
    detail = detail.encode('utf-8')
    first = first.encode('utf-8')
    update = update.encode('utf-8')
    unique_hash = unique_hash.encode('utf-8')
    renew_hash = renew_hash.encode('utf-8')
    newinfo = models.Info(
        subject, teacher, week, period, abstract, detail, first, update, unique_hash, renew_hash, now)
    try:
        # 既存かどうかの確認
        ex_info = qkou.filter(models.Info.unique_hash == unique_hash).first()
        if ex_info is None:
            # 新規の場合
            log.debug('授業名: %s … [新規]', subject)
            session.add(newinfo)
            session.commit()
            new_id = newinfo.id
            return new_id
        else:
            # 更新かどうか確認
            if ex_info.renew_hash == renew_hash is False:
                log.debug('授業名: %s … [更新]', subject)
                ex_info.detail = detail
                ex_info.up_date = update
                ex_info.renew_hash = renew_hash
                ex_info.up_time = now
                session.commit()
                ex_id = ex_info.id
                return ex_id
            else:
                # 既存だった場合
                log.debug('授業名: %s … [既存]', subject)
                ex_info.up_time = now
                session.commit()
                return False
    except Exception as e:
        session.rollback()
        log.exception(e)
        return False
    finally:
        session.close()


def del_old_info():
    session = models.Session()
    qkou = session.query(models.Info)
    yday = now - datetime.timedelta(days=1)
    try:
        qkou.filter(models.Info.up_time < yday).delete()
        session.commit()
        log.debug('[ GetInfoThread ] 最終更新が%s以前の古いデータを削除', yday)
    except Exception as e:
        log.exception(e)
    finally:
        session.close()


def id_info(id):
    session = models.Session()
    qkou = session.query(models.Info)
    try:
        lecture_info = qkou.filter(models.Info.id == id).first()
        if lecture_info is not None:
            return lecture_info
        else:
            return 0
    except Exception as e:
        log.exception(e)
        return False
    finally:
        session.close()
