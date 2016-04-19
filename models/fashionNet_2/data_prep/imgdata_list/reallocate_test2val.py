#!/usr/bin/env python

import numpy as np

l_root = "/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/"

item_type = ['_top.txt', '_bot.txt', '_sho.txt']

g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/general_list/'
for_length = open(g_root+'tuples_test_posi.txt').readlines()
user_num = 1+int(for_length[-1].strip('\r\n').split(' ')[0])

for u in range(0,user_num):
	for k in range(0,len(item_type)):
		test_source = open(l_root+"imgdata_list/test_"+str(u)+item_type[k]).readlines()
		val_source = open(l_root+"imgdata_list/val_"+str(u)+item_type[k]).readlines()
		test_target = open(l_root+"imgdata_list/test_"+str(u)+item_type[k],'w') 
		val_target = open(l_root+"imgdata_list/val_"+str(u)+item_type[k],'w')

		half_length = int(np.floor(float(len(test_source)+len(val_source))/2.0))

		source = [' ']*(len(test_source)+len(val_source))
		source[:len(test_source)] = test_source[:]
		source[len(test_source):] = val_source[:]

		for i in range(0,half_length):
			test_target.write(source[i])
		for i in range(half_length,(len(test_source)+len(val_source))):
			val_target.write(source[i])

		test_target.close()
		val_target.close()