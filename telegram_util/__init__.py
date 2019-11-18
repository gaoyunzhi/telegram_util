#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback as tb
import urllib.request
import threading

name = 'telegram_util'

def log_on_fail(debug_group = None, error_to_ignore=[]):
	def decorate(f):
		def applicator(*args, **kwargs):
			try:
				f(*args,**kwargs)
			except Exception as e:
				if str(e) in error_to_ignore:
					return
				print(e)
				tb.print_exc()
				if debug_group:
					debug_group.send_message(text=str(e)) 
		return applicator
	return decorate

def getDisplayUser(user):
    result = ''
    if user.first_name:
        result += user.first_name
    if user.last_name:
        result += ' ' + user.last_name
    if user.username:
        result += ' (' + user.username + ')'
    return '[' + result + '](tg://user?id=' + str(user.id) + ')'

def splitCommand(text):
    pieces = text.split()
    if len(pieces) < 1:
        return '', ''
    command = pieces[0]
    return command.lower(), text[text.find(command) + len(command):].strip()

def tryDelete(msg):
    try:
        msg.delete()
    except:
        pass

def autoDestroy(msg, minutes=1):
    if msg.chat_id > 0:
        return
    threading.Timer(minutes * 60, lambda: tryDelete(msg)).start() 
    
def matchKey(t, keys):
	if not t:
		return False
	for k in keys:
		if k.lower() in t.lower():
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
	if 'bot_ignore' in message.text:
		return False
	return len(msg.text) > 10

def _getFile(msg):
	if msg.photo:
		file = msg.photo[-1]
	elif msg.video:
		file = msg.video
	if not file:
		return
	return file.get_file()

def getFilePath(msg):
	file = _getFile(msg)
	if file:
		return file.file_path

def getTmpFile(msg):
	file = _getFile(msg)
	if not file:
		return
	filename = 'tmp' + file.file_path.strip().split('/')[-1]
	file.download(filename)
	return filename

def addToQueue(update, queue, subscription):
	msg = update.effective_message 
	if not msg or not msg.chat:
		return
	if msg.chat.id not in subscription:
		return
	queue.append((msg.chat.id, msg.message_id))