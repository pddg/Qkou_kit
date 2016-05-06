# coding:utf-8
import lib.add_db
from lib.login import soupinfo
from lib.db_info import del_old_info
from lib.db_cancel import del_old_cancel
from lib.db_news import del_old_news
from lib.collect import collect_info, collect_cancel, collect_news
import lib.tweeter
import time
from math import pow
from threading import Thread, active_count
import lib.settings

log = lib.settings.log


class TweetThread(Thread):

    def __init__(self, queue):
        super(TweetThread, self).__init__()
        self.daemon = True
        self.queue = queue

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
                if i < 12:
                    i += 1
                # 1.5^(ループ数)秒待機
                w = pow(a, i)
                time.sleep(w)
                lib.tweeter.tweet(t)


class PrintThread(Thread):

    def __init__(self, queue):
        super(PrintThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        log.debug('[ Start PrintThread ]')
        # GetInfoThreadとGetCancelThread, GetNewsThreadが終了するまで待機
        while active_count() >= 3:
            time.sleep(1)
        else:
            while True:
                try:
                    t = self.queue.get(block=False, timeout=None)
                except Exception:
                    # キューが空になったら終了
                    log.debug('[ End PrintThread ]\n')
                    break
                print t


class GetInfoThread(Thread):

    def __init__(self, queue, html):
        super(GetInfoThread, self).__init__()
        self.daemon = True
        self.queue = queue
        self.html = html

    def run(self):
        log.debug('[ Start GetInfoThread ]')
        info_list = collect_info(self.html)
        update = lib.add_db.add_info_to_queue(self.queue, *info_list)
        if update is 0:
            log.debug('[ GetInfoThread ] 更新はありませんでした．')
        else:
            log.debug('[ GetInfoThread ] %s個の情報を更新しました．', update)
        del_old_info()
        log.debug('[ End GetInfoThread ]')


class GetCancelThread(Thread):

    def __init__(self, queue, html):
        super(GetCancelThread, self).__init__()
        self.daemon = True
        self.queue = queue
        self.html = html

    def run(self):
        log.debug('[ Start GetCancelThread ]')
        cancel_list = collect_cancel(self.html)
        update = lib.add_db.add_cancel_to_queue(self.queue, *cancel_list)
        if update is 0:
            log.debug('[ GetCancelThread ] 更新はありませんでした．')
        else:
            log.debug('[ GetCancelThread ] %s個の情報を更新しました．', update)
        del_old_cancel()
        log.debug('[ End GetCancelThread ]')


class GetNewsThread(Thread):

    def __init__(self, queue, html):
        super(GetNewsThread, self).__init__()
        self.daemon = True
        self.queue = queue
        self.html = html

    def run(self):
        log.debug('[ Start GetNewsThread ]')
        # BeautifulSoup4で取得したhtmlからデータ抽出
        news_list = collect_news(self.html)
        update = lib.add_db.add_news_to_queue(self.queue, *news_list)
        if update is 0:
            log.debug('[ GetNewsThread ] 更新はありませんでした．')
        else:
            log.debug('[ GetNewsThread ] %s個の情報を更新しました．', update)
        del_old_news()
        log.debug('[ End GetNewsThread ]')


def define_do(q, tweet, *htmls):
    GIThread = GetInfoThread(q, htmls[0])
    GCThread = GetCancelThread(q, htmls[1])
    NwThread = GetNewsThread(q, htmls[2])
    if tweet is False:
        OutThread = TweetThread(q)
    else:
        OutThread = PrintThread(q)

    # 各スレッド開始
    GIThread.start()
    GCThread.start()
    NwThread.start()
    OutThread.start()

    # 全てのスレッドが終了するまで待機
    GIThread.join()
    GCThread.join()
    NwThread.join()
    OutThread.join()


def create_tables(q, *htmls):
    GIThread = GetInfoThread(q, htmls[0])
    GCThread = GetCancelThread(q, htmls[1])
    NwThread = GetNewsThread(q, htmls[2])

    # 各スレッド開始
    GIThread.start()
    GCThread.start()
    NwThread.start()

    # 全てのスレッドが終了するまで待機
    GIThread.join()
    GCThread.join()
    NwThread.join()
