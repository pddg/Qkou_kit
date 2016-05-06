# coding: utf-8
from main import create_tables, define_do
import sys
from lib.login import soupinfo
from Queue import Queue
from lib.db_cancel import id_cancel
from lib.db_info import id_info
from lib.db_news import id_news
import lib.settings
from logging import StreamHandler, DEBUG
import argparse


def main():
    q = Queue()
    parser = argparse.ArgumentParser(
        description="Automatically collect the lecture information of Kyoto Institute of Technology, and tweet its updates.")
    parser.add_argument("-v",
                        "--verbose",
                        dest="verbose",
                        default=False,
                        help="Debug on CLI. Show more information on console window.",
                        action="store_true"
                        )

    parser.add_argument("-n",
                        "--no-tweet",
                        dest="notweet",
                        default=False,
                        help="Only update database and show result of that on CLI. In this option, Qkou_kit don't tweet any.",
                        action="store_true"
                        )

    parser.add_argument("-c",
                        "--create-table",
                        dest="create",
                        default=False,
                        help="Creating table. If your MySQL server doesn't have the table you should use this option.",
                        action="store_true"
                        )

    group = parser.add_argument_group(
        'Show information', 'This option is showing the information of lecture and news by id.')
    group.add_argument("-i",
                       "--id",
                       dest="info_id",
                       default="",
                       type=str,
                       nargs="*",
                       help="To show information of some lectures, input their id numbers."
                       )

    group.add_argument("-d",
                       "--db_name",
                       dest="db_name",
                       default='info',
                       type=str,
                       nargs="?",
                       choices=['info', 'cancel', 'news'],
                       help="Choose the database to use."
                       )

    ids = parser.parse_args().info_id
    name = parser.parse_args().db_name
    nodata = u"お問い合わせされた情報は現在存在しません。"

    if parser.parse_args().verbose is True:
        log = lib.settings.log
        shandler = StreamHandler()
        shandler.setLevel(DEBUG)
        log.addHandler(shandler)
    else:
        pass

    if len(ids) > 0:
        # -i,-dが設定されている時
        for id in ids:
            if name == 'info':
                info = id_info(id)
            elif name == 'cancel':
                info = id_cancel(id)
            else:
                info = id_news(id)
            if info is 0:
                print nodata
            else:
                print info
        else:
            # 全てprintしたら終了
            sys.exit()
    else:
        pass
    htmls = soupinfo(*lib.settings.urls)
    if parser.parse_args().create is True:
        # -cが指定されている時。テーブル作成のみ
        create_tables(q, *htmls)
    else:
        define_do(q, parser.parse_args().notweet, *htmls)

if __name__ == "__main__":
    main()
