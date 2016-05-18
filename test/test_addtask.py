#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/17'
"""
from src.task import spider_sina_news


def main():
    spider_sina_news.delay()


if __name__ == '__main__':
    main()