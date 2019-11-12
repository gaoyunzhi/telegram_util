#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback as tb

name = 'telegram_util'

debug_group = -1001198682178

def log_on_fail(error_to_ignore=[]):
	def decorate(f):
		def applicator(*args, **kwargs):
			try:
				f(*args,**kwargs)
			except Exception as e:
				if str(e) in error_to_ignore:
					return
				print(e)
				tb.print_exc()
				updater.bot.send_message(chat_id=debug_group, text=str(e)) 
		return applicator
	return decorate


def matchKey(t, keys):
	if not t:
		return False
	for k in keys:
		if k in t:
			return True
	return False

def isUrl(t):
	for key in ['telegra.ph', 'com/', 'org/', '.st/', 'http', 't.co/']:
		if key in t:
			return True
	return False

def parseUrl(t):
	r = t
	for x in t.split():
		if not isUrl(x):
			continue
		if '://' in x:
			x = x[x.find('://') + 3:]
		else:
			r = r.replace(x, 'https://'+ x)
		for s in x.split('/'):
			if '?' in s:
				continue
			r = r.replace(s, urllib.request.pathname2url(s))
	return r

def isMeaningful(msg):
	if msg.media_group_id:
		return False
	if msg.photo:
		return True
	if not msg.text:
		return False
	if msg.text[0] == '/':
		return False
	return len(msg.text) > 10

def getTmpFile(msg):
	filename = 'tmp' + msg.photo[-1].get_file().file_path.strip().split('/')[-1]
	msg.photo[-1].get_file().download(filename)
	return filename
