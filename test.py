#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_util import getWid, cutCaption, clearUrl
import yaml
from telegram.ext import Updater
import web_2_album

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
		'https://mp.weixin.qq.com/s?__biz=MzA5MDM1MTcyNQ==&amp;mid=2657277726&amp;idx=1&amp;sn=613c0be79aebcd1ba714cbbbae64f66c&amp;chksm=8b9a861cbced0f0af93ef107a5e6fc885431024ff0316948f75cc6738276f33cc3e92dd25661&amp;mpshare=1&amp;scene=1&amp;srcid=0722lacFTcoG3jda9bA9JOoK&amp;sharer_sharetime=1595402746390&amp;sharer_shareid=a468f7684ed03b370e7298eb88d56e49#rd',
		'https://mp.weixin.qq.com/s/DzSn0oX7nctjnsHRM1DpKQ?url=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FDzSn0oX7nctjnsHRM1DpKQ&share_menu=1&sinainternalbrowser=topnav&mid=4532409046147275&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%90%86%E8%AE%BA&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FDzSn0oX7nctjnsHRM1DpKQ',
		None]:
		print(clearUrl(url))

def testAlbum():
	url = 'https://www.pride.com/art/2018/5/10/photographer-empowering-trans-youth-through-art?fbclid=IwAR1WM82jyIovZRmLQwgJtBTExGGy-_py6SnOirDb2_IEjEAxxzqyKCjqLxY#media-gallery-media-1'
	print(web_2_album.get(url))

if __name__=='__main__':
	# _test()
	# test2()
	testAlbum()