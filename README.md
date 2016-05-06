# Qkou_kit
京都工芸繊維大学の非公式休講通知botです。仲良くしてあげてね。
[@Qkou_kit](https://twitter.com/Qkou_kit)

## 概要
休講通知、また授業関係連絡について、ただWeb上に通知されるだけ、しかもわざわざログインしないと見れないという
現在の状況に対抗するための暫定的手段です。このクソbotを見た大学公式が似た機能を実装してくれますように。

基本はcronでスクリプトを定期実行し、定期的に休講情報および授業関係連絡をツイートという使い方をします。
また、授業関係連絡は長文になることが多いため、該当の授業関係連絡ツイートに対し「詳しく」や「詳しい情報を教えて」などとリプライを送ると、
DMで140字という制限を超えて全ての通知を受け取ることが出来るようになっています(stream.pyによる)。
さらに、一日に一度today.pyを定期実行することで、その日一日の休講科目一覧をツイートします。

***DEMO:***

|ツイート|DM|
|:---:|:---:|
|![](https://raw.github.com/wiki/pddg/Qkou_kit/imgs/スクショ1.png)|![](https://raw.github.com/wiki/pddg/Qkou_kit/imgs/スクショ2.png)|

## 環境
Ubuntu Server 14.04 LTSおよびMac OS X 10.11.3(pyenv及びvirtualenv使用)において以下の構成での動作は確認しています。

* Python 2.7.10
* MySQL Server version: 5.5.47-0ubuntu0.14.04.1 (Ubuntu)
* BeautifulSoup4 4.4.1
* lxml 3.5.0
* mechanize 0.2.5
* oauthlib 1.0.3
* PyMySQL 0.7.2
* requests 2.9.1
* requests-oauthlib 0.6.1
* SQLAlchemy 1.0.12
* tweepy 3.5.0

##使い方
サーバー、又はローカルにMySQLサーバーが既にあり、データベースが作成されている、
またPython 2.7.10及びpipのインストールが完了しているという前提で話を進めます。

```bash
$ git clone https://github.com/pddg/Qkou_kit.git
$ cd Qkou_kit
# 各種必要なパッケージがないとモジュールインストール時にエラーが出る。
# 以下はubuntuのコンテナで必要だった例
$ sudo apt-get install libxml2 libxslt1-dev zlib1g-dev
$ pip install -r requirements.txt
```

ここから設定に入ります。

```bash
$ cd lib
$ cp settings.py.example settings.py
$ vim settings.py
```

settings.pyに設定を記述してください．

-h又は--helpオプションを付けることでヘルプメッセージが表示されます。

```bash
$ cd /path/to/Qkou_kit
$ python ../Qkou_kit -h
usage: Qkou_kit [-h] [-n] [-c] [-i [INFO_ID [INFO_ID ...]]]
                [-d [{info,cancel,news}]]

Automatically collect the lecture information of Kyoto Institute of Technology
and tweet update.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Debug on CLI. Show more information on console window.
  -n, --no-tweet        Only update database and show result of that on CLI.
                        In this option, Qkou_kit don't tweet any.
  -c, --create-table    Creating table. You should use this option, if your
                        MySQL server doesn't have the table.

Show information:
  This option is showing the information of lecture and news.

  -i [INFO_ID [INFO_ID ...]], --id [INFO_ID [INFO_ID ...]]
                        To show information of some lectures, input their ids.
  -d [{info,cancel,news}], --db_name [{info,cancel,news}]
                        Choose the database to use.
```

最初に必ず-cまたは--create-tableオプションを付けて試運転を行ってください(テーブル及びカラムの作成が行われます)。

```bash
$ cd /path/to/Qkou_kit 
$ python ../Qkou_kit -c
$ cat log/debug.log
2016-05-01 18:25:02,121 - soupinfo - DEBUG - ログイン開始
2016-05-01 18:25:02,438 - soupinfo - DEBUG - ユーザ名とパスワードを送信完了
2016-05-01 18:25:03,772 - soupinfo - DEBUG - ログイン完了
2016-05-01 18:25:04,325 - soupinfo - DEBUG - URL: ?c=lecture_information … [完了]
2016-05-01 18:25:04,921 - soupinfo - DEBUG - URL: ?c=lecture_cancellation … [完了]
2016-05-01 18:25:06,104 - soupinfo - DEBUG - URL: ?c=news … [完了]
2016-05-01 18:25:06,141 - run - DEBUG - [ Start GetInfoThread ]
2016-05-01 18:25:06,142 - run - DEBUG - [ Start GetCancelThread ]
2016-05-01 18:25:06,206 - run - DEBUG - [ Start GetNewsThread ]
2016-05-01 18:25:06,300 - add_info - DEBUG - 授業名: 電子システム工学セミナーⅠ … [既存]
2016-05-01 18:25:06,307 - add_cancel - DEBUG - 授業名: 有機化学Ⅰmb … [既存]
2016-05-01 18:25:06,307 - add_news - DEBUG - News: 2016.4.28 平成２� … [既存]
2016-05-01 18:25:06,882 - add_info - DEBUG - 授業名: 科学と芸術の出会い … [既存]
2016-05-01 18:25:06,898 - add_news - DEBUG - News: 2016.4.27 1回生（ … [既存]
2016-05-01 18:25:06,899 - add_cancel - DEBUG - 授業名: 蛋白質分子工学 … [既存]

省略

2016-05-01 18:25:07,528 - add_cancel - DEBUG - 授業名: 情報処理演習ma … [既存]
2016-05-01 18:25:07,530 - del_old_news - DEBUG - [ GetNewsThread ] 最終更新が2016-04-30 18:25:01.957592以前の古いデータを削除
2016-05-01 18:25:07,530 - run - DEBUG - [ End GetNewsThread ]
2016-05-01 18:25:07,538 - add_info - DEBUG - 授業名: ガラス・アモルファス材料科学 … [既存]

省略

2016-05-01 18:25:07,604 - add_info - DEBUG - 授業名: 論理設計(情)(電) … [既存]
2016-05-01 18:25:07,615 - del_old_cancel - DEBUG - [ GetCancelThread ] 最終更新が2016-04-30 18:25:01.957592以前の古いデータを削除
2016-05-01 18:25:07,615 - run - DEBUG - [ End GetCancelThread ]

省略

2016-05-01 18:25:09,354 - add_info - DEBUG - 授業名: 生体分子機能化学 … [既存]
2016-05-01 18:25:09,363 - del_old_info - DEBUG - [ GetInfoThread ] 最終更新が2016-04-30 18:25:01.957592以前の古いデータを削除
2016-05-01 18:25:09,363 - run - DEBUG - [ End GetInfoThread ]
```

うまくいけばdebug.logに以上のような感じで出力され、error.logにはなにも出力されていないと思います。
一度実行して成功すれば、後はオプション指定なしで実行すればツイートを行うようになります。

また、実行時にconfigparserがセクションエラーを吐いた時は、設定ファイルのミス、または実行時のカレントディレクトリがQkou_kit(git cloneしたディレクトリ)になっているか確認してください。

cronへの登録は以下のように行います。例として、新規情報の確認は5分に一回、一日の休講情報のツイートは毎朝7時5分に実行されるようにしています。

```bash
$ crontab -e
*/5 * * * * cd /path/to/Qkou_kit;/path/to/python ../Qkou_kit
5 7 * * * cd /path/to/Qkou_kit;/path/to/python today.py
```

最後に、stream.pyを起動させて終わりです。
ここではUbuntu 14.04 LTSの場合(init.dの場合)の起動スクリプトを例に出しています。
その他のシステムでは別途記載するシェルスクリプトを作成し実行する、またはそのシステムに合った起動スクリプトを自作してください。

```bash
$ sudo apt-get install sysv-rc-conf
$ cd /path/to/Qkou_kit
$ vim q-stream
# Settings
QKOU_PATH='/home/kyukou/Qkou_kit'
PYTHON_PATH='/usr/bin/python'
USERNAME='kyukou'
SERVICE='stream.py'
LOG='/dev/null'

$ sudo chmod a+x q-stream
$ sudo cp q-stream /etc/init.d/
$ sudo sysv-rc-conf q-stream on

# Start service
$ sudo service q-stream start
# Stop service
$ sudo service q-stream stop
# Restart service
$ sudo service q-stream restart
```

以下は超適当なスクリプトです。nohupを使ってバックグラウンドで使用すること、pkillでプロセスキルするあたりは上記の起動スクリプトと共通です。

```bash
$ vim start.sh
nohup /path/to/python stream.py > /dev/null &

$ vim stop.sh
pkill -u [username] -f 'stream.py'
```

ログは自動的にdebug.logまたはerror.logに書き込まれますが、stream.pyにおいては例外的にストリーム中にエラーが起こった場合、settings.pyに書いたidあてにダイレクトメッセージで通知が行われます。

##今後の課題

* 実行が遅い(もう限界？)
* 連続してツイートする際の遅延をもうちょっとインテリジェンスに
* サーバの維持費(お金欲しい)


##作者
[@pudding_info](https://twitter.com/pudding_info)
ホームページ及びブログは以下
[poyo.info](https://www.poyo.info)

##ライセンス
MIT
