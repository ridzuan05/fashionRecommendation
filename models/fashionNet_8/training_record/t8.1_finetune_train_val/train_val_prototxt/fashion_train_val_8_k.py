#!/usr/bin/env python

import os

# source fashion_train_val_8.prototxt for modification
s_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/train_val_prototxt/'

# open source fashion_train_val_8.prototxt
s_fp = open(s_root+'fashion_train_val_8.prototxt').readlines()

# user_number
user_num = 800

if 'fashion_train_val_8_k' not in os.listdir(s_root):
    os.system('mkdir '+s_root+'fashion_train_val_8_k')

# generate fashion_train_val_8_k.prototxt for each user
for u in range(0,user_num):
	# open k_fp
	k_fp = open(s_root+'fashion_train_val_8_k/fashion_train_val_8_'+str(u)+'.prototxt','w')
	# write fashion_train_val_8_k.prototxt
	for i in range(0,len(s_fp)):
	        temp = s_fp[i].split('^')
	        if(len(temp)==3):
	            temp[1] = str(u)
	            temp = temp[0]+temp[1]+temp[2]
	        else:
	            temp = temp[0]
	        k_fp.write(temp)
	k_fp.close()