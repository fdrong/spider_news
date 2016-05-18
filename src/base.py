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
from db_mongo import MongoDB
from logging.handlers import TimedRotatingFileHandler


class BaseSpider(object):
    def __init__(self, config):
        self.config = config
        self.logger = self.create_logger()     # 创建日志
        self.db = MongoDB(self.config.DbConn)  # 创建数据库链接

    def get_content(self, url):
        """
        requests the url content from web
        :param url:
        :return:
        """
        retry = 3
        while retry:
            try:
                time.sleep(random.randint(1, 20))
                r = requests.get(url)
                if r.status_code == 200:
                    return self.convert_code(r.content)
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

    def convert_code(self, content, chartCode=None):
        if isinstance(content, unicode):
            return content
        try:
            data = content.decode('utf-8')
        except Exception as e:
            # self.logger.error(u"转码utf-8失败, 原因:%s" % e)
            data = content.decode('gbk', "ignore")
        return data

    # 时间解析
    def parse_time(self, content):
        content = content.replace("\n", "").replace("\t", "").strip()
        if isinstance(content, unicode):
            content = content.replace(u'年', '-').replace(u'月', '-').replace(u'日 ', ' ').replace(u'日', ' ').replace(u"\xa0", "")
        else:
            content = content.replace('年', '-').replace('月', '-').replace('日 ', ' ').replace('日', ' ').replace("\xa0", "")
        time_regex_list = [
            "\d{0,4}[-/.]{0,1}\d{1,2}[-/.]\d{1,2}\s?\d{1,2}:\d{1,2}:\d{1,2}",
            "\d{0,4}[-/.]{0,1}\d{1,2}[-/.]\d{1,2}\s?\d{1,2}:\d{1,2}",
            "\d{0,4}[-/.]{0,1}\d{1,2}[-/.]\d{1,2}\s?\d{1,2}",
            "\d{0,4}[-/.]{0,1}\d{1,2}[-/.]\d{1,2}"]
        for time_regex in time_regex_list:
            pattern = re.compile(time_regex)
            time_filter_list = pattern.findall(content)
            if time_regex_list:
                return time_filter_list[0]
            else:
                continue
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 根据xpath进行解析
    def parse_xpath_content(self, url):
        result = dict()
        content = self.get_content(url)
        if not content:
            return result
        result["url"] = url
        result["md5"] = self.md5(url)
        result["creat_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree = HTML(content)
        for key in self.config.Xpath.keys():
            if not self.config.Xpath.get(key):
                continue
            elif isinstance(self.config.Xpath.get(key), dict):
                # 字符串截取
                if self.config.Xpath[key]['op'] == 'cut':
                    pos1 = content.find(self.config.Xpath[key]['start'])
                    if pos1 != -1:
                        pos2 = content[pos1:].find(self.config.Xpath[key]['end'])
                        result[key] = content[pos1+len(self.config.Xpath[key]['start']):pos1+pos2]
                    else:
                        result[key] = ""
            else:
                list_content = tree.xpath(self.config.Xpath[key].replace('tbody/', ''))
                if list_content:
                    result[key] = "".join(list_content)
                else:
                    result[key] = ""
        result['publish_time'] = self.parse_time(result['publish_time'])
        return result

    def parse_urls(self):
        content = self.get_content(self.config.Root)
        if content:
            tree = HTML(content)
            url_list = tree.xpath(u"//a/@href")
            pattern = re.compile(self.config.Regex)
            url_joined_list = [urlparse.urljoin(self.config.Root, url) for url in url_list]
            url_joined_list = list(set(url_joined_list))   # 去重
            return filter(pattern.match, url_joined_list)
        else:
            return []

    def run(self):
        self.logger.info(u"开始爬取新闻: %s" % self.config.Name)
        url_list = self.parse_urls()
        for url in url_list:
            self.logger.info(u"准备爬去新闻URL: %s" % url)
            if self.db.find_one(self.config.Name, {"md5": self.md5(url)}):
                self.logger.info(u"来源[%s], URL[%s]已存在." % (self.config.Name, url))
                continue
            dict_value = self.parse_xpath_content(url)
            self.db.insert(self.config.Name, dict_value)

    def create_logger(self):
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
        file_handler.suffix = "{}-%Y-%m-%d.log".format(self.config.Name)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)        # 设置文件日志打印级别

        console_handler = logging.StreamHandler()  # 设置终端日志打印
        console_handler.setLevel(logging.DEBUG)    # 设置终端日志打印级别
        console_handler.setFormatter(formatter)    # 设置终端日志打印格式

        logger = logging.getLogger(self.config.Name)     # 获取名为log_name的logger
        logger.addHandler(file_handler)            # 添加Handler
        logger.addHandler(console_handler)         # 添加Handler
        logger.setLevel(logging.INFO)              # 设置日志级别为DEBUG(级别最低)

        return logger