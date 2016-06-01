#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/18'
"""
from src.base import BaseSpider
from src.config import SinaConfig
import time
import unittest


class SpiderTest(unittest.TestCase):
    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        self.assertFalse(False)

if __name__ == '__main__':
    unittest.main()


# def main():
#     start = time.time()
#     spider = BaseSpider(config=SinaConfig)
#     # url = 'http://news.163.com/16/0517/19/BN9QMN1G00014PRF.html'
#     # spider.parse_xpath_content(url)
#     spider.run()
#     end = time.time()
#     print "called_time:%d" % (end - start)
#
#
#
# if __name__ == '__main__':
#     main()