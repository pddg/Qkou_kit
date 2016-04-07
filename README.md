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
$ cd conf
$ cp settings_example.conf settings.conf
$ vim settings.conf
[shibboleth]
user = # 学籍番号の最初の1をbに変えた値
pass = # シボレス認証用のパスワード

[mysql]
user = # MySQLで該当のデータベースを使用するユーザ名
pass = # 上記ユーザのパスワード
host = # MySQLの場所
DBname = # データベース名

[twitter]
CK = # Consumer Key
CS = # Cnsumer Secret
AT = # Access Token
AS = # Access Secret
id = # 通知用に使用するTwitter ID
```

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
2016-03-31 22:47:28,554 - run - DEBUG - [ Start GetInfoThread ]
2016-03-31 22:47:28,554 - run - DEBUG - [ Start GetCancelThread ]
2016-03-31 22:47:28,554 - run - DEBUG - [ Start GetNewsThread ]
2016-03-31 22:47:28,562 - soupinfo - DEBUG - ログイン開始
2016-03-31 22:47:28,562 - soupinfo - DEBUG - ログイン開始
2016-03-31 22:47:28,563 - soupinfo - DEBUG - ログイン開始
2016-03-31 22:47:29,610 - soupinfo - DEBUG - ユーザ名とパスワードを送信完了
2016-03-31 22:47:29,656 - soupinfo - DEBUG - ユーザ名とパスワードを送信完了
2016-03-31 22:47:29,658 - soupinfo - DEBUG - ユーザ名とパスワードを送信完了
2016-03-31 22:47:31,603 - soupinfo - DEBUG - ログイン完了
2016-03-31 22:47:31,608 - soupinfo - DEBUG - ログイン完了
2016-03-31 22:47:31,614 - soupinfo - DEBUG - ログイン完了
2016-03-31 22:47:33,537 - del_deactive_cancel - DEBUG - 古いデータを削除
2016-03-31 22:47:33,537 - run - DEBUG - [ End GetCancelThread ]
2016-03-31 22:47:33,636 - add_news - DEBUG - News: 2016.3.30 平成28� … [既存]
2016-03-31 22:47:33,644 - add_info - DEBUG - 授業名: 物理化学Ⅰma … [既存]
2016-03-31 22:47:33,676 - add_news - DEBUG - News: 2016.3.30 [重要] � … [既存]
2016-03-31 22:47:33,701 - add_info - DEBUG - 授業名: 数学演習Ⅱpb … [既存]
2016-03-31 22:47:33,707 - add_news - DEBUG - News: 2016.3.30 平成27� … [既存]
2016-03-31 22:47:33,735 - add_info - DEBUG - 授業名: 基礎解析Ⅱpb … [既存]
2016-03-31 22:47:33,740 - add_news - DEBUG - News: 2016.3.29 【学部� … [既存]
2016-03-31 22:47:33,769 - add_info - DEBUG - 授業名: 数学演習Ⅰpb … [既存]
2016-03-31 22:47:33,776 - add_news - DEBUG - News: 2016.3.28 博士前� … [既存]
2016-03-31 22:47:33,801 - add_info - DEBUG - 授業名: 基礎解析Ⅰpb … [既存]
2016-03-31 22:47:33,807 - add_news - DEBUG - News: 2016.3.28 [重要] � … [既存]
2016-03-31 22:47:33,836 - add_info - DEBUG - 授業名: 高分子構造学 … [既存]
2016-03-31 22:47:33,843 - add_news - DEBUG - News: 2016.3.25 【大学� … [既存]
2016-03-31 22:47:33,868 - add_info - DEBUG - 授業名: 高分子機能工学実験Ⅰ … [既存]
2016-03-31 22:47:33,873 - add_news - DEBUG - News: 2016.3.25 2016年度 … [既存]
2016-03-31 22:47:33,900 - add_news - DEBUG - News: 2016.3.24 平成28� … [既存]
2016-03-31 22:47:33,908 - add_info - DEBUG - 授業名: 認知的インタラクションデザイン学 … [既存]
2016-03-31 22:47:33,934 - add_news - DEBUG - News: 2016.3.23 【至急� … [既存]
2016-03-31 22:47:33,942 - add_info - DEBUG - 授業名: 学術国際情報mf … [既存]
2016-03-31 22:47:33,959 - add_news - DEBUG - News: 2016.3.14 [重要] � … [既存]
2016-03-31 22:47:33,975 - add_info - DEBUG - 授業名: 生物機能学実験Ⅱ … [既存]
2016-03-31 22:47:33,981 - add_news - DEBUG - News: 2016.3.4 証明書� … [既存]
2016-03-31 22:47:34,010 - add_info - DEBUG - 授業名: 学術国際情報md … [既存]
2016-03-31 22:47:34,017 - add_news - DEBUG - News: 2016.3.1 平成２� … [既存]
2016-03-31 22:47:34,043 - add_info - DEBUG - 授業名: 学術国際情報mc … [既存]
2016-03-31 22:47:34,049 - add_news - DEBUG - News: 2016.3.1 平成２� … [既存]
2016-03-31 22:47:34,078 - add_info - DEBUG - 授業名: 物理学基礎実験Ａma … [既存]
2016-03-31 22:47:34,085 - add_news - DEBUG - News: 2016.2.24 自然再� … [既存]
2016-03-31 22:47:34,110 - add_info - DEBUG - 授業名: ジェロントロジー入門（超高齢社会のユニバーサルデザイン） … [既存]
2016-03-31 22:47:34,120 - add_news - DEBUG - News: 2016.2.15 平成28� … [既存]
2016-03-31 22:47:34,143 - add_info - DEBUG - 授業名: 生体分子機能化学 … [既存]
2016-03-31 22:47:34,149 - add_news - DEBUG - News: 2016.2.1 平成28� … [既存]
2016-03-31 22:47:34,177 - add_info - DEBUG - 授業名: 化学基礎実験ma … [既存]
2016-03-31 22:47:34,196 - add_news - DEBUG - News: 2016.2.1 平成27 � … [既存]
2016-03-31 22:47:34,216 - add_info - DEBUG - 授業名: 都市史Ⅰ … [既存]
2016-03-31 22:47:34,224 - add_news - DEBUG - News: 2016.1.28 中世に� … [既存]
2016-03-31 22:47:34,258 - add_info - DEBUG - 授業名: 分析化学mb … [既存]
2016-03-31 22:47:34,265 - add_news - DEBUG - News: 2016.1.25 平成28� … [既存]
2016-03-31 22:47:34,301 - add_info - DEBUG - 授業名: 有機化学演習(生) … [既存]
2016-03-31 22:47:34,308 - add_news - DEBUG - News: 2016.1.14 平成28� … [既存]
2016-03-31 22:47:34,332 - del_deactive_info - DEBUG - 古いデータを削除
2016-03-31 22:47:34,332 - run - DEBUG - [ End GetInfoThread ]
2016-03-31 22:47:34,349 - add_news - DEBUG - News: 2016.1.13 平成27� … [既存]
2016-03-31 22:47:34,381 - add_news - DEBUG - News: 2016.1.4 技術検� … [既存]
2016-03-31 22:47:34,435 - add_news - DEBUG - News: 2016.1.4 技術検� … [既存]
2016-03-31 22:47:34,466 - add_news - DEBUG - News: 2015.12.22 平成27� … [既存]
2016-03-31 22:47:34,492 - add_news - DEBUG - News: 2015.12.3 平成27� … [既存]
2016-03-31 22:47:34,518 - add_news - DEBUG - News: 2015.10.15 平成28� … [既存]
2016-03-31 22:47:34,542 - add_news - DEBUG - News: 2015.4.13 学生定� … [既存]
2016-03-31 22:47:34,556 - run - DEBUG - [ End GetNewsThread ]
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

* ストリームがたまに落ちて復帰してこない時がある
* 実行が遅い(もう限界？)
* 連続してツイートする際の遅延をもうちょっとインテリジェンスに
* サーバの維持費(お金欲しい)


##作者
[@pudding_info](https://twitter.com/pudding_info)
ホームページ及びブログは以下
[poyo.info](https://www.poyo.info)
