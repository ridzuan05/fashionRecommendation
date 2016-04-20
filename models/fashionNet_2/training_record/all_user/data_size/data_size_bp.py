#!/usr/bin/env python

data_type = ['train_', 'val_', 'test_']

l_root = "/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/"
g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/general_list/'
size_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/'

for_length = open(g_root+'tuples_test_posi.txt').readlines()
user_num = 1+int(for_length[-1].strip('\r\n').split(' ')[0])

for i in range(0,len(data_type)):
	all_user_tupleSize = open(size_root+'data_size/all_'+data_type[i]+'size.txt','w') # open all_train/val/test_size.txt
	for u in range(0,user_num):
		temp_data = open(l_root+"imgdata_list/"+data_type[i]+str(u)+'_top.txt').readlines()
		temp_size = len(temp_data)
		all_user_tupleSize.write(str(temp_size)+'\r\n')
	all_user_tupleSize.close()