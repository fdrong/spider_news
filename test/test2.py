#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/17'
"""
from src.task import test21


def main():
    data = {"abc":"abc"}
    test21.delay(data)


if __name__ == '__main__':
    main()