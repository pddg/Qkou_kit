# coding: utf-8
import main
import sys
from Queue import Queue
from lib.db_cancel import deactive_cancel, id_cancel
from lib.db_info import deactive_info, id_info
from lib.db_news import deactive_news, id_news
import argparse


def default_do(q, bool):
    GIThread = main.GetInfoThread(q)
    GCThread = main.GetCancelThread(q)
    NwThread = main.GetNewsThread(q)
    TwThread = main.TweetThread(q, bool)

    # 初回実行時は以下の2文をコメントアウトする必要がある (要改善)
    deactive_info()
    deactive_cancel()
    deactive_news()

    # 各スレッド開始
    GIThread.start()
    GCThread.start()
    NwThread.start()
    TwThread.start()
    # 全てのスレッドが終了するまで待機
    GIThread.join()
    GCThread.join()
    NwThread.join()
    TwThread.join()


def operate_DB(q):
    GIThread = main.GetInfoThread(q)
    GCThread = main.GetCancelThread(q)
    NwThread = main.GetNewsThread(q)

    # 各スレッド開始
    GIThread.start()
    GCThread.start()
    NwThread.start()
    # 全てのスレッドが終了するまで待機
    GIThread.join()
    GCThread.join()
    NwThread.join()

if __name__ == "__main__":
    q = Queue()
    parser = argparse.ArgumentParser(
        description="Automatically collect the lecture information of Kyoto Institute of Technology and tweet update.")
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
                        help="Creating table. You should use this option, if your MySQL server doesn't have the table.",
                        action="store_true"
                        )

    group = parser.add_argument_group(
        'Show information', 'This option is showing the information of lecture and news.')
    group.add_argument("-i",
                       "--id",
                       dest="info_id",
                       default="",
                       type=str,
                       nargs="*",
                       help="To show information of some lectures, input their ids."
                       )

    group.add_argument("-d",
                       "--db_name",
                       dest="DB_name",
                       default=1,
                       type=str,
                       nargs="?",
                       choices=['info', 'cancel', 'news'],
                       help="Choose the database to use."
                       )

    ids = parser.parse_args().info_id
    name = parser.parse_args().DB_name
    nodata = u"お問い合わせされた情報は現在存在しません。"

    if len(ids) > 0:
        # -i,-dが設定されている時
        for id in ids:
            if name is 'info':
                info = id_info(id)
            elif name is 'cancel':
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

    if parser.parse_args().create:
        # -cが指定されている時(True)、テーブル作成のみ
        operate_DB(q)
    else:
        # DBの更新及び更新結果をツイート(False)orコマンドラインに表示(True)
        default_do(q, parser.parse_args().notweet)
