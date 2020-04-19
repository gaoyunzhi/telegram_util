#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_util import getWid, cutCaption

def _test():
	# print(getWid('https://www.weibo.com/1897681455/IAnf30RPr?type=comment'))
	# print(getWid('http://weibointl.api.weibo.cn/share/138804312.html?weibo_id=4492279152896775&from=groupmessage&isappinstalled=0'))
	s = '长佩：http://t.cn/AiuVSNPa'
	print(cutCaption(s, '', 100))

if __name__=='__main__':
	_test()