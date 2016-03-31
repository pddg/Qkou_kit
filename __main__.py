# coding: utf-8
import main
from Queue import Queue
from lib.db_cancel import deactive_cancel
from lib.db_info import deactive_info
from lib.db_news import deactive_news

if __name__ == "__main__":
    q = Queue()
    GIThread = main.GetInfoThread(q)
    GCThread = main.GetCancelThread(q)
    NwThread = main.GetNewsThread(q)
    TwThread = main.TweetThread(q)

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
