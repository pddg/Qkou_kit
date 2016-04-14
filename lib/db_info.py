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


class Qkou(Base):
    __tablename__ = 'lec_info'

    id = Column(Integer, primary_key=True)
    subject = Column(VARCHAR(length=100))
    teacher = Column(VARCHAR(length=100))
    week = Column(VARCHAR(length=15))
    period = Column(VARCHAR(length=5))
    abstract = Column(VARCHAR(length=40))
    detail = Column(VARCHAR(length=10000))
    first = Column(VARCHAR(length=10))
    up_date = Column(VARCHAR(length=10))
    active = Column(Integer, nullable=False)

    def __init__(self, subject, teacher, week, period, abstract, detail, first, up_date, active):
        self.subject = subject
        self.teacher = teacher
        self.week = week
        self.period = period
        self.abstract = abstract
        self.detail = detail
        self.first = first
        self.up_date = up_date
        self.active = active

    def __repr__(self):
        return "<Qkou('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s, %s')>"\
            % (self.subject, self.teacher, self.week, self.period,
               self.abstract, self.detail, self.first, self.up_date, self.active)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_info(subject, teacher, week, period, abstract, detail, first, update):
    session = Session()
    qkou = session.query(Qkou)
    # utf-8にエンコードしないとエラー
    subject = subject.encode('utf-8')
    teacher = teacher.encode('utf-8')
    week = week.encode('utf-8')
    period = period.encode('utf-8')
    abstract = abstract.encode('utf-8')
    detail = detail.encode('utf-8')
    first = first.encode('utf-8')
    update = update.encode('utf-8')
    active = 1
    newinfo = Qkou(
        subject, teacher, week, period, abstract, detail, first, update, active)
    try:
        # 既存かどうかの確認
        qkou.filter(and_(Qkou.subject == subject, Qkou.week == week, Qkou.detail == detail,
                         Qkou.first == first, Qkou.up_date == update)).one()
        # 更新があった場合の確認
        ex_info = qkou.filter(and_(Qkou.subject == subject, Qkou.week == week,
                                   Qkou.first == first, Qkou.up_date != update)).first()
        if ex_info is None:
            # 既存の場合
            log.debug('授業名: %s … [既存]', subject)
            ex_info = qkou.filter(and_(Qkou.subject == subject, Qkou.week == week, Qkou.detail == detail,
                                       Qkou.first == first, Qkou.up_date == update)).first()
            ex_info.active = active
            session.commit()
            session.close()
            return False
        else:
            # 更新の場合
            log.debug('授業名: %s … [更新]', subject)
            ex_info.abstract = abstract
            ex_info.detail = detail
            ex_info.up_date = update
            ex_info.active = active
            session.commit()
            # sessionを閉じる前にidを取得
            ex_id = ex_info.id
            session.close()
            return ex_id
    except NoResultFound:
        # 新規の場合
        log.debug('授業名: %s … [新規]', subject)
        session.add(newinfo)
        session.commit()
        new_id = newinfo.id
        session.close()
        return new_id
    except MultipleResultsFound:
        # 重複している場合
        log.warning('授業名: %s … [重複]', subject)
        session.close()
        return False


def deactive_info():
    session = Session()
    qkou = session.query(Qkou)
    try:
        cancels = qkou.filter(Qkou.active == 1).all()
        for cancel in cancels:
            cancel.active = 0
            session.commit()
        session.close()
    except Exception as e:
        log.exception(e)


def del_deactive_info():
    session = Session()
    qkou = session.query(Qkou)
    try:
        qkou.filter(Qkou.active == 0).delete()
        session.commit()
        session.close()
        log.debug('古いデータを削除')
    except Exception as e:
        session.close()
        log.exception(e)


def id_info(id):
    session = Session()
    qkou = session.query(Qkou)
    try:
        lecture_info = qkou.filter(Qkou.id == id).first()
        session.close()
        if lecture_info is not None:
            return lecture_info
        else:
            return 0
    except Exception as e:
        session.close()
        log.exception(e)
        return False
