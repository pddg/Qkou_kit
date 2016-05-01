# coding: utf-8

from sqlalchemy import create_engine, Column, VARCHAR, Integer, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings

engine = create_engine('mysql+pymysql://' + settings.mysql_user + ':' +
                       settings.mysql_pass + '@' + settings.mysql_host + '/' +
                       settings.DBname, encoding='utf-8', pool_recycle=3600)

Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Info(Base):
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
    unique_hash = Column(VARCHAR(length=255))
    renew_hash = Column(VARCHAR(length=255))
    up_time = Column(DATETIME)

    def __init__(self, subject, teacher, week, period, abstract, detail, first, up_date, unique_hash, renew_hash, up_time):
        self.subject = subject
        self.teacher = teacher
        self.week = week
        self.period = period
        self.abstract = abstract
        self.detail = detail
        self.first = first
        self.up_date = up_date
        self.unique_hash = unique_hash
        self.renew_hash = renew_hash
        self.up_time = up_time

    def __repr__(self):
        return "<Info('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s, %s')>"\
            % (self.subject, self.teacher, self.week, self.period,
               self.abstract, self.detail, self.first, self.up_date, self.up_time)


class Cancel(Base):
    __tablename__ = 'lec_cancel'

    id = Column(Integer, primary_key=True)
    subject = Column(VARCHAR(length=100))
    teacher = Column(VARCHAR(length=100))
    day = Column(VARCHAR(length=15))
    week = Column(VARCHAR(length=15))
    period = Column(VARCHAR(length=5))
    abstract = Column(VARCHAR(length=200))
    first = Column(VARCHAR(length=10))
    unique_hash = Column(VARCHAR(length=255))
    up_time = Column(DATETIME)

    def __init__(self, subject, teacher, day, week, period, abstract, first, unique_hash, up_time):
        self.subject = subject
        self.teacher = teacher
        self.day = day
        self.week = week
        self.period = period
        self.abstract = abstract
        self.first = first
        self.unique_hash = unique_hash
        self.up_time = up_time

    def __repr__(self):
        return "<Cancel('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s)>"\
            % (self.subject, self.teacher, self.day, self.week,
               self.period, self.abstract, self.first)


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    up_date = Column(VARCHAR(length=10))
    detail = Column(VARCHAR(length=1000))
    link = Column(VARCHAR(length=200))
    unique_hash = Column(VARCHAR(length=255))
    up_time = Column(DATETIME)

    def __init__(self, up_date, detail, link, unique_hash, up_time):
        self.up_date = up_date
        self.detail = detail
        self.link = link
        self.unique_hash = unique_hash
        self.up_time = up_time

    def __repr__(self):
        return "<News('%s', '%s', '%s', '%s')>"\
            % (self.up_date, self.detail, self.link, self.active)
