# coding: utf-8
import settings
import hashlib
import re

log = settings.log


def collect_info(html):
    try:
        info_list = []
        for tr in html.findAll('tr', attrs={'class': re.compile('^gen_')}):
            td = tr.findAll('td')
            # リンクの有無判定
            links = []
            if td[8].a is not None:
                for a in td[8].findAll('a'):
                    link = a.get('href')
                    links.append(link)
            # タグ除去
            lec_info = map(text, td[3:11])
            # リンクを追加
            lec_info[5] = lec_info[5] + " " + " ".join(links)
            # ハッシュを取る
            # 一意識別用ハッシュ
            unique = lec_info[0] + lec_info[1] + \
                lec_info[2] + lec_info[3] + lec_info[4] + lec_info[6]
            unique_hash = hashlib.sha1(unique.encode('utf-8')).hexdigest()
            lec_info.append(unique_hash)
            # 更新識別用ハッシュ
            renew = lec_info[5] + lec_info[7]
            renew_hash = hashlib.sha1(renew.encode('utf-8')).hexdigest()
            lec_info.append(renew_hash)
            info_list.append(lec_info)
        else:
            return info_list
    except Exception as e:
        log.exception(e)


def collect_cancel(html):
    try:
        cancels_list = []
        for tr in html.findAll('tr', attrs={'class': re.compile('^gen_')}):
            td = tr.findAll('td')
            # タグ除去
            lec_cancel = map(text, td[2:9])
            # 一意識別用ハッシュ
            s = lec_cancel[0] + lec_cancel[1] + lec_cancel[2] + \
                lec_cancel[3] + lec_cancel[4] + lec_cancel[6]
            unique_hash = hashlib.sha1(s.encode('utf-8')).hexdigest()
            lec_cancel.append(unique_hash)
            cancels_list.append(lec_cancel)
        else:
            return cancels_list
    except Exception as e:
        log.exception(e)


def collect_news(html):
    try:
        news_list = []
        now_notice = html.find('div', attrs={'id': 'now_notice_area'})
        for tr in now_notice.findAll('tr'):
            td = tr.findAll('td')
            news = map(text, td[0:2])
            # 文中にlinkが存在するか確認
            links = []
            if td[1].a is not None:
                for a in td[1].findAll('a'):
                    link = a.get('href')
                    links.append(link)
            urls = " ".join(links)
            # URLを付加
            news.append(urls)
            # 一意識別用ハッシュ
            s = news[0] + news[1]
            unique_hash = hashlib.sha1(s.encode('utf-8')).hexdigest()
            news.append(unique_hash)
            news_list.append(news)
        else:
            return news_list
    except Exception as e:
        log.exception(e)


def text(td):
    return td.text.strip()
