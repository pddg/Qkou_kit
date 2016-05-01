# coding: utf-8

import mechanize
from bs4 import BeautifulSoup
import settings

log = settings.log


def soupinfo(*urls):
    log.debug('ログイン開始')
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozila/5.0(X11; U; Linux i686; en-us; rv:1.9.0.1) \
                        Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    loginurl = 'https://portal.student.kit.ac.jp/'
    # 学務課にログイン
    try:
        br.open(loginurl)
        br.select_form(nr=0)
        br['j_username'] = settings.shibboleth_user
        br['j_password'] = settings.shibboleth_pass
        br.submit()
        log.debug('ユーザ名とパスワードを送信完了')
        br.select_form(nr=0)
        br.submit()  # 続行ボタンを押すため
        log.debug('ログイン完了')
    except Exception as e:
        log.exception(e)
    htmls = []
    for url in urls:
        target = loginurl + url
        br.open(target)
        log.debug('URL: %s … [完了]', url)
        html = br.response().read()
        bs = BeautifulSoup(html, 'lxml')
        htmls.append(bs)
    return htmls
