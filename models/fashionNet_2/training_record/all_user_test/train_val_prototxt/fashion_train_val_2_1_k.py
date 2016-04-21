#!/usr/bin/env python

# source fashion_train_val_2_1.prototxt for modification
s_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user_test/train_val_prototxt/'

# open source train_val.prototxt
s_fp = open(s_root+'fashion_train_val_2_1.prototxt').readlines()

# user_number
size_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user_test/'
all_train_size = open(size_root+'data_size/all_train_size.txt').readlines()
user_num = len(all_train_size)

# generate fashion_train_val_2_1_k.prototxt for each user
for u in range(0,user_num):
	# open k_fp
	k_fp = open(s_root+'fashion_train_val_2_1_'+str(u)+'.prototxt','w')
	# write fashion_train_val_2_1_k.prototxt
	for i in range(0,len(s_fp)):
	        temp = s_fp[i].split('!')
	        if(len(temp)==3):
	            temp[1] = str(u)
	            temp = temp[0]+temp[1]+temp[2]
	        else:
	            temp = temp[0]
	        k_fp.write(temp)
	k_fp.close()