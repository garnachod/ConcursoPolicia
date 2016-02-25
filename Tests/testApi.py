# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from APITextos import APITextos 

if __name__ == '__main__':
	"""
	users = APITextos.getUsersSimilar_user_all_topic("Taxigate", "ar", 100, 1)
	for user in users:
		print user.screen_name + "\t"+ user.location

	users = APITextos.getUsersSimilar_user_all_topic("abosofyan7", "ar", 100, 1)
	for user in users:
		print user.screen_name + "\t"+ user.location

	print ""
	print ""
	users = APITextos.getUsersSimilar_user_all_topic("nightwalker_109", "ar", 100, 1)
	for user in users:
		print user.screen_name + "\t"+ user.location
	"""
	users = APITextos.getUsersSimilar_user_all_topic("a_ortigosa", "es", 100, 1)
	if users != False:
		for user in users:
			print user.screen_name + "\t"+ user.location
	