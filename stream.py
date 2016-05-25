# coding: utf-8
import re
import time
import sys
import codecs
import tweepy
from threading import Thread
from Queue import Queue
import logging
import logging.config
from lib.db_info import id_info
from lib.db_news import id_news
import lib.settings

log = lib.settings.log

debug_id = lib.settings.tw_id

auth = tweepy.OAuthHandler(lib.settings.CK, lib.settings.CS)
auth.set_access_token(lib.settings.AT, lib.settings.AS)
api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
mydata = api.me()
myid = mydata.id


class Listener(tweepy.streaming.StreamListener):

    def __init__(self, queue):
        super(Listener, self).__init__()
        self.queue = queue

    def on_status(self, status):
        if status.in_reply_to_user_id == myid:
            log.debug("[ Stream ] リプライを受信")
            self.queue.put(status)
        else:
            pass

    def on_error(self, status):
        print("Receive Error Code: " + status)


class StreamRecieverThread(Thread):

    def __init__(self, queue):
        super(StreamRecieverThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        l = Listener(self.queue)
        stream = tweepy.Stream(auth, l)
        while True:
            try:
                stream.userstream()
            except Exception as e:
                api.send_direct_message(
                    screen_name=debug_id, text="Stream down. And now restarting. Wait 60s...")
                log.exception(e)
                time.sleep(60)
                stream = tweepy.Stream(auth, l)
                api.send_direct_message(
                    screen_name=debug_id, text="Start streaming.")


def get_news(id):
    sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
    try:
        news = id_news(id)
    except Exception as e:
        log.exception(e)
    if news is not False:
        if news is not 0:
            try:
                update = news.up_date.decode('utf-8')
                detail = news.detail.decode('utf-8')
                if len(news.link) is not 0:
                    link_ = news.link.decode('utf-8')
                return u"掲載日:%s\n詳細:%s\nリンク:%s" % (update, detail, link_)
            except Exception as e:
                log.exception(e)
        else:
            return u"お問い合わせされた情報は現在存在しません。"

    else:
        return u"DBエラーです。情報が取得できませんでした。"


def get_info(id):
    sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
    try:
        info = id_info(id)
    except Exception as e:
        log.exception(e)
    if info is not False:
        if info is not 0:
            try:
                subject = info.subject.decode('utf-8')
                teacher = info.teacher.decode('utf-8')
                week = info.week.decode('utf-8')
                period = info.period.decode('utf-8')
                detail = info.detail.decode('utf-8')
                return u"授業名：%s\n教員名：%s\n日程：%s, %s\n詳細：%s" % (subject, teacher, week, period, detail)
            except Exception as e:
                log.exception(e)
        else:
            return u"お問い合わせされた授業関係連絡は現在存在しません。"

    else:
        return u"DBエラーです。情報が取得できませんでした。"


def tweetassembler(**args):
    in_reply_to_status = args['in_reply_to_status']
    if in_reply_to_status is not None:
        regex = u'.*詳し.*'
        if re.match(regex, in_reply_to_status.text, re.U):
            # リプライ元のIDを取得
            id = in_reply_to_status.in_reply_to_status_id
            # リプライ元のステータスを取得
            qkou_status = api.get_status(id)
            entities = qkou_status.entities['hashtags']
            # ハッシュタグを含まない場合の判定
            if len(entities) > 0:
                hashtag = entities[0]['text']
                # ハッシュタグから数字だけ抽出
                info_num = re.search("(?<=lec)[0-9]*", hashtag)
                news_num = re.search("(?<=news)[0-9]*", hashtag)
                if info_num is not None:
                    qkou_id = info_num.group()
                    log.debug("[ Stream ] Infoの詳細を取得")
                    dm_text = get_info(qkou_id)
                elif news_num is not None:
                    news_id = news_num.group()
                    log.debug("[ Stream ] Newsの詳細を取得")
                    dm_text = get_news(news_id)
                else:
                    pass
                try:
                    api.send_direct_message(
                        user_id=in_reply_to_status.user.id, text=dm_text)
                    log.debug('[ Stream ] DMを送信')
                except Exception as e:
                    log.exception(e)
            else:
                pass


class CoreThread(Thread):

    def __init__(self, queue):
        super(CoreThread, self).__init__()
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            obj = self.queue.get()
            tweetassembler(in_reply_to_status=obj)


def StartThreads():
    q = Queue()
    CoreTh = CoreThread(q)
    StreamTh = StreamRecieverThread(q)
    CoreTh.start()
    StreamTh.start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    StartThreads()
