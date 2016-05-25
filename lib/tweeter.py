# coding: utf-8
import tweepy
import settings
log = settings.log

try:
    auth = tweepy.OAuthHandler(settings.CK, settings.CS)
    auth.set_access_token(settings.AT, settings.AS)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
except Exception as e:
    log.exception(e)


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
    num = u" #lec%s" % args[10]
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


def format_news(*args):
    # linkがない場合
    if len(args[2]) is 0:
        tweet_text = u"\n掲載日：%s\n詳細：%s" % (args[0], args[1])
        link = u''
        num = u" #news%s" % args[4]
    # linkがある場合
    else:
        tweet_text = u"\n掲載日：%s\n詳細：%s" % (args[0], args[1])
        link = u'\nリンク:%s' % args[2]
        num = u" #news%s" % args[4]
    # TwitterでのURLの文字数は22又は23
    if 95 >= len(tweet_text) > 0:
        tweet_text += link
        tweet_text += num
        return tweet_text
    elif len(tweet_text) > 95:
        formatted_text = tweet_text[0:100] + link + num
        return formatted_text
