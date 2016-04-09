# coding: utf-8

from sqlalchemy import create_engine, Column, VARCHAR, Integer, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker
import logging
import logging.config
import ConfigParser
import pymysql

config = ConfigParser.ConfigParser()
config.read('./conf/settings.conf')

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')

engine = create_engine('mysql+pymysql://' + config.get('mysql', 'user') + ':' +
                       config.get('mysql', 'pass') + '@' + config.get('mysql', 'host') + '/' +
                       config.get('mysql', 'DBname'), encoding='utf-8', pool_recycle=3600)

# モデルの定義
Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    update = Column(VARCHAR(length=10))
    detail = Column(VARCHAR(length=1000))
    link = Column(VARCHAR(length=200))
    active = Column(Integer, nullable=False)

    def __init__(self, update, detail, link, active):
        self.update = update
        self.detail = detail
        self.link = link
        self.active = active

    def __repr__(self):
        return "<News('%s', '%s', '%s', '%s')>"\
            % (self.update, self.detail, self.link, self.active)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_news(update, detail, link):
    session = Session()
    qkou = session.query(News)
    # utf-8にエンコードしないとエラー
    update = update.encode('utf-8')
    detail = detail.encode('utf-8')
    if len(link) is not 0:
        link = link.encode('utf-8')
    active = 1
    newinfo = News(update, detail, link, active)
    try:
        # 既存かどうかの確認
        qkou.filter(and_(News.update == update, News.detail == detail)).one()
        ex_info = qkou.filter(
            and_(News.update == update, News.detail == detail)).first()
        if ex_info is not None:
            # 既存の場合
            log.debug('News: %s %s … [既存]', update, detail[0:10])
            ex_info.active = active
            session.commit()
            session.close()
            return False
        else:
            # 更新の場合
            log.warning('News: %s %s … [想定外のエラー]', update, detail[0:10])
            session.close()
            return False
    except NoResultFound:
        # 新規の場合
        log.debug('News: %s %s … [新規]', update, detail[0:10])
        session.add(newinfo)
        session.commit()
        new_id = newinfo.id
        session.close()
        return new_id
    except MultipleResultsFound:
        # 重複している場合
        log.warning('News: %s %s … [重複]', update, detail[0:10])
        session.close()
        return False


def deactive_news():
    session = Session()
    qkou = session.query(News)
    try:
        news = qkou.filter(News.active == 1).all()
        for new in news:
            new.active = 0
            session.commit()
        session.close()
    except Exception as e:
        log.exception(e)


def del_deactive_news():
    session = Session()
    qkou = session.query(News)
    try:
        qkou.filter(News.active == 0).delete()
        session.commit()
        session.close()
        log.debug('古いデータを削除')
    except Exception as e:
        session.close()
        log.exception(e)


def id_news(id):
    session = Session()
    qkou = session.query(News)
    try:
        news_info = qkou.filter(News.id == id).first()
        session.close()
        if news_info is not None:
            return news_info
        else:
            return 0
    except Exception as e:
        session.close()
        log.exception(e)
        return False
