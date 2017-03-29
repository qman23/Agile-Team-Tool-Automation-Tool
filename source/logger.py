#!/usr/bin/env python
#_*_coding:utf-8_*_
# Filename: logger.py

import logging
import time
import os

def getLogger():
	# ��һ��������һ��logger
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)    # Log�ȼ��ܿ���

	timeTsp = time.strftime("%Y%m%d%H%M%S",time.localtime())
	# �ڶ���������һ��handler������д����־�ļ�
	if os.path.exists('log') == False:
		
		os.mkdir('log')
	logfile = 'log/log_'+timeTsp+'.txt'
	fh = logging.FileHandler(logfile, mode='w')
	fh.setLevel(logging.DEBUG)   # �����file��log�ȼ��Ŀ���

	# ���������ٴ���һ��handler���������������̨
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)   # �����console��log�ȼ��Ŀ���

	# ���Ĳ�������handler�������ʽ
	formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)

	# ���岽����logger��ӵ�handler����
	logger.addHandler(fh)
	logger.addHandler(ch)
	return logger
#get logger
log = getLogger()