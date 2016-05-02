# coding: utf-8
from datetime import datetime, timedelta
import tweepy
import re
import sys
import logging.config
import logging
from lib.db_cancel import todayinfo
import lib.jholiday
from lib.tweeter import tweet, get_api

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')


def del_yesterday_info():
    # 昨日の日付を取得
    d = datetime.now() + timedelta(days=-1)
    yesterday = "%s/%s/%s" % (d.year, d.month, d.day)

    api = get_api()

    # アカウント情報及びTLの取得
    myinfo = api.me()
    try:
        tweets = tweepy.Cursor(api.user_timeline, id=myinfo.id).items(100)
    except Exception as e:
        log.exception(e)

    # 昨日の定期ツイートを削除
    for t in tweets:
        r = re.compile(yesterday)
        sentence = t.text.encode('utf-8')
        s = re.match(r, sentence)
        if s is None:
            pass
        else:
            try:
                api.destroy_status(t.id)
            except Exception as e:
                log.exception(e)


def get_today_info():
    # 今日の日付を取得
    d = datetime.now()  # + timedelta(days=3)
    # 祝日を取得
    holiday = lib.jholiday.holiday_name(date=datetime.date(d))
    date = u"%s/%s/%s" % (d.year, d.month, d.day)

    # 取得した日付を元にDBから情報を取得
    today = todayinfo(date)
    if holiday is None:
        # Tweet
        if len(today) is 0:
            # tweet(u"%s 本日休講はありません" % (date))
            print(u"%s 本日休講はありません" % (date))
        else:
            today = map(decode_utf8, today)
            i = u", ".join(today)
            t = u"%s 本日の休講\n%s" % (date, i)
            if len(t) < 140:
                tweet(t)
                # print t
            else:
                all = [t[i:i + 120] for i in range(0, len(t), 120)]
                for one in all:
                    # print one
                    tweet(t[0:140])
    else:
        t = u'本日は%sです．課題やレポートは終わりましたか？意義のある祝日をお過ごしください．' % (
            holiday)
        tweet(t)


def decode_utf8(txt):
    return txt.decode('utf-8')

if __name__ == "__main__":
    del_yesterday_info()
    get_today_info()
