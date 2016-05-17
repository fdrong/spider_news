#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/16'
"""
import os
import re
import time
import logging
import requests
import urlparse
import hashlib
import random
from lxml.etree import HTML
from datetime import date, datetime
from logging.handlers import TimedRotatingFileHandler


class BaseSpider(object):
    def __init__(self, spidername):
        self.logger = self.create_logger(spidername)

    def get_content(self, url):
        """
        requests the url content from web
        :param url:
        :return:
        """
        retry = 3
        self.url = url
        while retry:
            try:
                time.sleep(random.randint(1, 20))
                r = requests.get(url)
                if r.status_code == 200:
                    return r.content
                else:
                    retry -= 1
            except Exception as e:
                self.logger.error("Request URL:%s Failed, Reason:{reason}".format(reason=e.message))
                retry -= 1
        return ""

    # MD5计算
    def md5(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    # 移除\r \t \n 特殊符号
    def remove_tags(self, content):
        return content.replace("\r", "").replace("\t", "").replace("\n", "").strip()

    # 根据xpath进行解析
    def parse_xpath_content(self, content, xpath_dict):
        tree = HTML(content)
        result = dict()
        for key in xpath_dict.keys():
            list_content = tree.xpath(xpath_dict[key].replace('tbody/', ''))
            if list_content:
                result[key] = "".join(list_content)
            else:
                result[key] = ""
        return result

    def parse_urls(self, content, regex='*.*'):
        tree = HTML(content)
        url_list = tree.xpath(u"//a/@href")
        pattern = re.compile(regex)
        url_joined_list = [urlparse.urljoin(self.url, url) for url in url_list]
        return filter(pattern.match, url_joined_list)

    def create_logger(self, spidername):
        """
        创建一个日志对象logger，同时打印文件日志和终端日志，其中Debug级别的日志只在终端打印
        :param spidername
        :return: logger object
        """
        LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                "logs", "{}.log".format(date.today()))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')   # 格式化日志
        file_handler = TimedRotatingFileHandler(LOG_FILE,'D', 1, 0)  # 实例化handler
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)        # 设置文件日志打印级别

        console_handler = logging.StreamHandler()  # 设置终端日志打印
        console_handler.setLevel(logging.DEBUG)    # 设置终端日志打印级别
        console_handler.setFormatter(formatter)    # 设置终端日志打印格式

        logger = logging.getLogger(spidername)     # 获取名为log_name的logger
        logger.addHandler(file_handler)            # 添加Handler
        logger.addHandler(console_handler)         # 添加Handler
        logger.setLevel(logging.INFO)              # 设置日志级别为DEBUG(级别最低)

        return logger


spider = BaseSpider("sina_news")
regex = "^http://news.163.com/%s/%s/\d{2}/\w+.html$" \
        % (str(datetime.now().year)[2:], "%02d%02d" % (datetime.now().month, datetime.now().day))
content = spider.get_content("http://www.163.com/")
url_list = spider.parse_urls(content, regex=regex)
for url in url_list:
    print url