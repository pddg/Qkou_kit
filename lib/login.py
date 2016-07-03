# coding: utf-8

import mechanize
from bs4 import BeautifulSoup
import settings
import models
from tweeter import tweet

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
        session = models.Session()
        fault = session.query(models.Fault).filter(models.Fault.now == 1).first()
        if fault is None:
            new_fault = models.Fault(now=1, created_at=settings.now, status=e.encode('utf-8'))
            session.add(new_fault)
            session.commit()
            tweet('%s 学務課サーバへのログインに失敗しました．障害が発生している可能性があります．'
                  % (settings.now.strftime('%Y/%m/%d %H:%M:%S')))
        session.close()
        log.exception(e)
    # 障害復旧時
    session = models.Session()
    fault = session.query(models.Fault).filter(models.Fault.now == 1).first()
    if fault is not None:
        fault.now = 0
        fault.ended_at = settings.now
        session.commit()
        tweet('%s 学務課サーバへのログインに成功しました．'
              % (settings.now.strftime('%Y/%m/%d %H:%M:%S')))
    session.close()
    htmls = []
    for url in urls:
        target = loginurl + url
        br.open(target)
        log.debug('URL: %s … [完了]', url)
        html = br.response().read()
        bs = BeautifulSoup(html, 'lxml')
        htmls.append(bs)
    return htmls
