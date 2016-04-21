#!/usr/bin/env python

import os

# source control_k.py for modification
s_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user_test/training_script/'

# open source control_k.py
s_fp = open(s_root+'control_k.py').readlines()

# user_number
size_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user_test/'
all_train_size = open(size_root+'data_size/all_train_size.txt').readlines()
user_num = len(all_train_size)

# ^666^ to user_seq_idx[0~988]
# ^888^ to test_iter
test_iter = open(size_root+'train_test_params/test_iter.txt').readlines()

# generate control_k.py for each user
for u in range(0,user_num):
    # open k_fp
    k_fp = open(s_root+'control_'+str(u)+'.py','w')
    # write control_k.py
    for i in range(0,len(s_fp)):
        temp = s_fp[i].split('^')
        if(len(temp)==3):	        	
            if(temp[1]==str(666)):
	        temp[1] = str(u)
            elif(temp[1]==str(888)):
        	temp[1] = test_iter[u].strip('\r\n').split(' ')[0]
            temp = temp[0]+temp[1]+temp[2]
        else:
            temp = temp[0]
        k_fp.write(temp)
    k_fp.close()

os.system('chmod +x control_*')
