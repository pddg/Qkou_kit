# coding: utf-8
import logging.config
import logging
import datetime

# シボレス認証
shibboleth_user = "b4111018"
shibboleth_pass = "(Shoma7712)"

# MySQL
mysql_user = "root"
mysql_pass = "shoma7712"
mysql_host = "192.168.10.3"
DBname = "kyukou"

# twitter
CK = "k2jdQpOffeGRUYvvIEaLDurTK"
CS = "ZFJGnGMWgd2l1SolnoZG7nYiShXlyD4BRgVnxPy7kNJDYOxHyO"
AT = "1900517250-TSEJoW0QKSiv22YY5WNbOBFgN8DEmWxXZmNZJ8c"
AS = "cdvEBgA0X8j8I1CEjb5Q0hu4rNQdCaGKBl5LA0nzaTSKa"
tw_id = "pudding_info"

# config
logging.config.fileConfig('./log/log.conf')
log = logging.getLogger('getlog')

# URL
urls = ["?c=lecture_information", "?c=lecture_cancellation", "?c=news"]

# 現在時刻
now = datetime.datetime.now()