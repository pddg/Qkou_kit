# coding:utf-8
from lib.add_db import add_info, add_cancel, add_news
from lib.login import soupinfo
from lib.db_info import del_deactive_info
from lib.db_cancel import del_deactive_cancel
from lib.db_news import del_deactive_news
import lib.tweeter
import ConfigParser
import logging.config
import logging
import time
from math import pow
from threading import Thread, active_count

# ログの設定
logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')

# configファイルの読み込み
config = ConfigParser.ConfigParser()
config.read('./conf/settings.conf')


class TweetThread(Thread):

    def __init__(self, queue, bool):
        super(TweetThread, self).__init__()
        self.daemon = True
        self.queue = queue
        self.bool = bool

    def run(self):
        log.debug('[ Start TweetThread ]')
        i = 1
        a = float(1.5)
        # GetInfoThreadとGetCancelThread, GetNewsThreadが終了するまで待機
        while active_count() >= 3:
            time.sleep(1)
        else:
            while True:
                try:
                    t = self.queue.get(block=False, timeout=None)
                except Exception:
                    # キューが空になったら終了
                    log.debug('[ End TweetThread ]\n')
                    break
                if bool:
                    pass
                else:
                    i += 1
                    # 1.5^(ループ数)秒待機
                    w = pow(a, i)
                    time.sleep(w)
                lib.tweeter.tweet(t, bool)


class GetInfoThread(Thread):

    def __init__(self, queue):
        super(GetInfoThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        log.debug('[ Start GetInfoThread ]')
        Soup = soupinfo("?c=lecture_information")
        # BeautifulSoup4で取得したhtmlからデータ抽出
        add_info(Soup, self.queue)
        del_deactive_info()
        log.debug('[ End GetInfoThread ]')


class GetCancelThread(Thread):

    def __init__(self, queue):
        super(GetCancelThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        log.debug('[ Start GetCancelThread ]')
        Soup = soupinfo("?c=lecture_cancellation")
        # BeautifulSoup4で取得したhtmlからデータ抽出
        add_cancel(Soup, self.queue)
        del_deactive_cancel()
        log.debug('[ End GetCancelThread ]')


class GetNewsThread(Thread):

    def __init__(self, queue):
        super(GetNewsThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        log.debug('[ Start GetNewsThread ]')
        Soup = soupinfo("?c=news")
        # BeautifulSoup4で取得したhtmlからデータ抽出
        add_news(Soup, self.queue)
        del_deactive_news()
        log.debug('[ End GetNewsThread ]')
