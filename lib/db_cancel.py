# coding: utf-8

from sqlalchemy import create_engine, Column, VARCHAR, Integer, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker
import logging
import logging.config
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./conf/settings.conf')

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')

engine = create_engine('mysql+pymysql://' + config.get('mysql', 'user') + ':' +
                       config.get('mysql', 'pass') + '@' + config.get('mysql', 'host') + '/' +
                       config.get('mysql', 'DBname'), encoding='utf-8', pool_recycle=3600)

# モデルの定義
Base = declarative_base()


class Cancel(Base):
    __tablename__ = 'lec_cancel'

    id = Column(Integer, primary_key=True)
    subject = Column(VARCHAR(length=100))
    teacher = Column(VARCHAR(length=100))
    day = Column(VARCHAR(length=15))
    week = Column(VARCHAR(length=15))
    period = Column(VARCHAR(length=5))
    abstract = Column(VARCHAR(length=40))
    first = Column(VARCHAR(length=10))
    update = Column(VARCHAR(length=10))
    active = Column(Integer)

    def __init__(self, subject, teacher, day, week, period, abstract, first, update, active):
        self.subject = subject
        self.teacher = teacher
        self.day = day
        self.week = week
        self.period = period
        self.abstract = abstract
        self.first = first
        self.update = update
        self.active = active

    def __repr__(self):
        return "<Qkou('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s, '%s')>"\
                 % (self.subject, self.teacher, self.day, self.week,
                    self.period, self.abstract, self.first, self.update, self.active)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_cancel(subject, teacher, day, week, period, abstract, first, update):
    session = Session()
    qkou = session.query(Cancel)
    # utf-8にエンコードしないとエラー
    subject = subject.encode('utf-8')
    teacher = teacher.encode('utf-8')
    day = day.encode('utf-8')
    week = week.encode('utf-8')
    period = period.encode('utf-8')
    abstract = abstract.encode('utf-8')
    first = first.encode('utf-8')
    update = update.encode('utf-8')
    active = 1
    newcancel = Cancel(subject, teacher, day, week, period, abstract, first, update, active)
    try:
        # 既存かどうかの確認
        qkou.filter(and_(Cancel.subject == subject, Cancel.day == day, Cancel.update == update)).one()
        # 更新があった場合の確認
        ex_cancel = qkou.filter(and_(Cancel.subject == subject, Cancel.day == day,
                                     Cancel.first == first, Cancel.update != update)).first()
        if ex_cancel is None:
            # 既存の場合
            log.debug('授業名: %s … [既存]', subject)
            ex_cancel.active = active
            session.commit()
            session.close()
            return False
        else:
            # 更新の場合
            log.debug('授業名: %s … [更新]', subject)
            ex_cancel.abstract = abstract
            ex_cancel.update = update
            ex_cancel.active = active
            session.commit()
            # sessionを閉じる前にidを取得
            ex_id = ex_cancel.id
            session.close()
            return ex_id
    except NoResultFound:
        # 新規の場合
        log.debug('授業名: %s … [新規]', subject)
        session.add(newcancel)
        session.commit()
        new_id = newcancel.id
        session.close()
        return new_id
    except MultipleResultsFound:
        # 重複している場合
        log.warning('授業名: %s … [重複]', subject)
        session.close()
        return False


def deactive_cancel():
    session = Session()
    qkou = session.query(Cancel)
    try:
        cancels = qkou.filter(Cancel.active == 1).all()
        for cancel in cancels:
            cancel.active = 0
            session.commit()
        session.close()
    except Exception as e:
        log.exception(e)


def del_deactive_cancel():
    session = Session()
    qkou = session.query(Cancel)
    try:
        qkou.filter(Cancel.active == 0).delete()
        log.debug('古いデータを削除')
    except Exception as e:
        log.exception(e)


# 日付から検索してデータを取得し教科名を返す
def todayinfo(day):
    infolist = []
    session = Session()
    for info in session.query(Cancel).filter(Cancel.day == day).all():
        infolist.append(info.sub)
    return infolist
