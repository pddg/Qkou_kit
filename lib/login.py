# coding: utf-8

import mechanize
from bs4 import BeautifulSoup
import logging.config
import logging
import ConfigParser

logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')

config = ConfigParser.ConfigParser()
config.read('./conf/settings.conf')


def soupinfo(url):
    log.debug('ログイン開始')
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent','Mozila/5.0(X11; U; Linux i686; en-us; rv:1.9.0.1) \
                        Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    loginurl = 'https://portal.student.kit.ac.jp/'
    lecinfo = loginurl + url
    # 学務課にログイン
    try:
        br.open(loginurl)
        br.select_form(nr=0)
        br['j_username'] = config.get('shibboleth', 'user')
        br['j_password'] = config.get('shibboleth', 'pass')
        br.submit()
        log.debug('ユーザ名とパスワードを送信完了')
        br.select_form(nr=0)
        br.submit() # 続行ボタンを押すため
        log.debug('ログイン完了')
    except Exception as e:
        log.exception(e)
    br.open(lecinfo)
    html = br.response().read()
    bs = BeautifulSoup(html, 'lxml')
    return bs
          




