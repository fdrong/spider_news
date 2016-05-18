# -*- coding: utf-8 -*-
from datetime import datetime

# celery 配置信息
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TIMEZONE = 'Asia/Shanghai'


class MongodbConn(object):
    Host = '127.0.0.1'
    DbName = 'news'
    Port = 27017
    User = None
    PassWd = None
    slave_oKay = True


# 新浪新闻的配置
class SinaConfig(object):
    Name = "sina_news"
    Root = "http://www.163.com"
    Regex = "^http://news.163.com/%s/%s/\d{2}/\w+.html$" \
        % (str(datetime.now().year)[2:], "%02d%02d" % (datetime.now().month, datetime.now().day))

    Xpath = {
        'title': '//div[@id="epContentLeft"]/h1//text()',            # 标题
        'content': '//div[@id="endText"]//p//text()',                # 正文
        'source': '//a[@id="ne_article_source"]//text()',            # 来源
        'keyword': '//*[@id="ne_wrap"]/head/meta[2]/@content',       # 关键词
        'publish_time': '//*[@id="epContentLeft"]/div[1]//text()',   # 发表时间
        'author': {
            "op": "cut",
            "path": '//*[@id="endText"]/div[2]/span[1]/text()',
            "start": u"作者：",
            "end": u"</span>"
        },                                                            # 作者
        'editor': '//*[@id="endText"]/div[2]/span[1]/a/img/@alt',     # 责任编辑
        'comments': '//*[@id="epContentLeft"]/div[2]/div[1]/div[2]/a[2]//text()',  # 评论数
    }
    DbConn = MongodbConn()



