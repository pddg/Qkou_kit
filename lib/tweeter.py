# coding:utf-8
import tweepy
import logging.config
import logging
import ConfigParser

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')
config = ConfigParser.ConfigParser()
config.read('./conf/settings.conf')

CK = config.get('twitter', 'CK')
CS = config.get('twitter', 'CS')
AT = config.get('twitter', 'AT')
AS = config.get('twitter', 'AS')
try:
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
except Exception as e:
    log.exception(e)
    raise


def get_api():
    return api


def tweet(t):
    try:
        api.update_status(status=t)
    except Exception as e:
        log.exception(e)


def format_info(*args):
    tweet_text = u"\n授業名：%s\n教員名：%s\n日程：%s, %s限\n概要：%s\n詳細：%s" \
                 % (args[0], args[1], args[2], args[3], args[4], args[5])
    print args
    num = u" #lec%s" % args[8]
    if 131 >= len(tweet_text) > 0:
        tweet_text += num
        return tweet_text
    elif len(tweet_text) > 131:
        formatted_text = tweet_text[0:131] + num
        return formatted_text


def format_cancel(*args):
    tweet_text = u"\n授業名：%s\n教員名：%s\n休講日：%s %s %s限\n概要：%s" \
                 % (args[0], args[1], args[2], args[3], args[4], args[5])
    if 140 >= len(tweet_text) > 0:
        return tweet_text
    elif len(tweet_text) > 140:
        return tweet_text[0:139]

