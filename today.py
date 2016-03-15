# coding: utf-8
from datetime import datetime, timedelta
import tweepy
import re
import logging.config
import logging
from lib.db_cancel import todayinfo
from lib.tweeter import tweet, get_api

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')


def del_yesterday_info():
    # 昨日の日付を取得
    d = datetime.now() + timedelta(days = -1)
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
    d = datetime.now()
    date = u"%s/%s/%s" % (d.year, d.month, d.day)

    # 取得した日付を元にDBから情報を取得
    today = todayinfo(date)

    # Tweet
    if len(today) is 0:
        print(u"%s 本日休講はありません" % (date))
    else:
        i = ", ".join(today)
        t = u"%s 本日の休講\n%s" % (date, i)
        if len(t) < 140:
            print type(today)
            print(t)
        else:
            print(t[0:140])

if __name__ == "__main__":
    # del_yesterday_info()
    get_today_info()
