#!/usr/bin/env python

from itertools import izip
import re
import random

g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/general_list/'
l_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/lmdb_list/'
size_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/'

pa_top = []
pa_bot = []
pa_sho = []
pa_top = open(g_root+'img_list_top.txt').readlines()
pa_bot = open(g_root+'img_list_bottom.txt').readlines()
pa_sho = open(g_root+'img_list_shoe.txt').readlines()

data_type = ['train', 'val', 'test']

for i in range(0,len(data_type)):
	#####################################################
	#load tuples_posi.txt & tuples_neg.txt
	posi = open(g_root+'tuples_'+data_type[i]+'_posi.txt')
	nega = open(g_root+'tuples_'+data_type[i]+'_neg.txt')

	top = []
	bot = []
	sho = []
	top = open(g_root+'top_ind_'+data_type[i]+'.txt').readlines()
	bot = open(g_root+'bottom_ind_'+data_type[i]+'.txt').readlines()
	sho = open(g_root+'shoe_ind_'+data_type[i]+'.txt').readlines()

	posi_nega = []
	for line_p, line_n in izip(posi, nega):
		posi_nega.append(line_p.strip('\r\n')+' 1\r\n')
		posi_nega.append(line_n.strip('\r\n')+' 0\r\n')

	#divide to txt: p_top/p_bot/p_sho/n_top/n_bot/n_sho
	user_idx = [0]*(1+int(posi_nega[-1].strip('\r\n').split(' ')[0]))
	for m in range(0, len(posi_nega)): # check each tuple
		#read user idx
		user_idx_temp = int(posi_nega[m].strip('\r\n').split(' ')[0]) # read user idx (0,988)
		user_idx[user_idx_temp] += 1 # user_idx is what I want to save, according to data_type

	random.shuffle(posi_nega)
	random.shuffle(posi_nega)
	random.shuffle(posi_nega)

	#sort user_idx according to their tuples num
	user_idx_sorted = sorted(range(len(user_idx)), key=lambda k: user_idx[k],reverse=True)

	# save all_train/val/test_size.txt
	all_user_tupleSize = open(size_root+'data_size/all_'+data_type[i]+'_size.txt','w') # open all_train/val/test_size.txt 
	for n in range(0, len(user_idx)): # check each user
		tuple_num = str(user_idx_sorted[n])+' '+str(user_idx[user_idx_sorted[n]])+'\r\n' # (user_idx, tuple num) in descending order
		all_user_tupleSize.write(tuple_num)
	all_user_tupleSize.close()

	posi.close()
	nega.close()
#####################################################
