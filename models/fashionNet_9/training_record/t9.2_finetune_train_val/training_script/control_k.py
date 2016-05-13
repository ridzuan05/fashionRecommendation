#!/usr/bin/env python

import os

# source control_k.py for modification
s_root = '/home/dell/fashionRecommendation/models/fashionNet_9/training_record/t9.2_finetune_train_val/training_script/'

# open source control.py
s_fp = open(s_root+'control.py').readlines()

# user_number
user_num = 800

if 'control_k' not in os.listdir(s_root):
    os.system('mkdir '+s_root+'control_k')

# generate control_k.py for each user
for u in range(0,user_num):
    # open k_fp
    k_fp = open(s_root+'control_k/control_'+str(u)+'.py','w')
    # write control_k.py
    for i in range(0,len(s_fp)):
        temp = s_fp[i].split('^')
        if(len(temp)==3):	        	
            if(temp[1]==str(666)):
	        temp[1] = str(u)
            temp = temp[0]+temp[1]+temp[2]
        else:
            temp = temp[0]
        k_fp.write(temp)
    k_fp.close()

os.system('chmod +x ./control_k/*')
