#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_util import getWid, cutCaption, clearUrl
import yaml
from telegram.ext import Updater

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @contribute_bot
debug_group = tele.bot.get_chat(-1001198682178)

def _test():
	# print(getWid('https://www.weibo.com/1897681455/IAnf30RPr?type=comment'))
	# print(getWid('http://weibointl.api.weibo.cn/share/138804312.html?weibo_id=4492279152896775&from=groupmessage&isappinstalled=0'))
	url ='http://mp.weixin.qq.com/s?src=11&timestamp=1589392736&ver=2336&signature=L-einWnP9vn2e6HZydd0c3DQA7oJzX9Auk43ShkRhHPfMq1SicmZwORHVA1AK9ADSOyi9DPJCaCLj44S*WoVkvltzPPnl2MqRWskqYMLPNmnfsfdXUyQVIlqPwf2mfEQ&new=1'
	s = '[source](%s)' % url
	m = cutCaption('', s, 100)
	print(cutCaption('', s, 100))
	debug_group.send_message('1 ' + s, parse_mode='markdown')
	debug_group.send_message('3 ' + m, parse_mode='markdown')

def test2():
	for url in ['https://www.lgbtqnation.com/2020/07/trump-administration-memo-explains-spot-transgender-woman/#.Xxhk4Z7ztRQ.wechat', 
		'http://mp.weixin.qq.com/s?__biz=MzUxMzAzMzk5Ng==&mid=2247484807&idx=1&sn=101bde2cf3bfbee2dcbd1e842475e06a&chksm=f95a17e4ce2d9ef27a9dbdd6c59c831b45caa8658ac566cc2d3681216c83b0f9e28a7ed0dc3f&mpshare=1&scene=1&srcid=0723RKjQqOqqKU0gQFh4vs4S&sharer_sharetime=1595435039677&sharer_shareid=f467668849c8544e583567bf8a259f31#rd',
		None]:
		print(clearUrl(url))

if __name__=='__main__':
	# _test()
	test2()