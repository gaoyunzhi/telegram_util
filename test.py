#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_util import getWid

def _test():
	print(getWid('http://weibointl.api.weibo.cn/share/138804312.html?weibo_id=4492279152896775&from=groupmessage&isappinstalled=0'))

if __name__=='__main__':
	_test()