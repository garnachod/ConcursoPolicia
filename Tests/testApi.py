# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from APITextos import APITextos 

if __name__ == '__main__':
	users = APITextos.getUsersSimilar_user_all_topic("Taxigate", "ar", 100, 1)
	for user in users:
		print user.screen_name + "\t"+ user.location

	users = APITextos.getUsersSimilar_user_all_topic("abosofyan7", "ar", 100, 1)
	for user in users:
		print user.screen_name + "\t"+ user.location