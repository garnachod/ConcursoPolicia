# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from APITextos import APITextos 

if __name__ == '__main__':
	print APITextos.getUsersSimilar_user_all_topic(11688082, "ar", 100, 1)