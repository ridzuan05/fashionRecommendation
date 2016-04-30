#!/usr/bin/env python

from itertools import izip
import re
import random
import os

g_root = '/home/dell/fashionRecommendation/models/fashionNet_3_dell/data_prep/general_list/'
l_root = '/home/dell/fashionRecommendation/models/fashionNet_3_dell/data_prep/lmdb_list/tvt_pn_tbs_k_txt/'

check = '/home/dell/fashionRecommendation/models/fashionNet_3_dell/data_prep/lmdb_list/'
if 'tvt_pn_tbs_k_txt' not in os.listdir(check):
    os.system('mkdir '+l_root)

pa_top = []
pa_bot = []
pa_sho = []
pa_top = open(g_root+'img_list_top.txt').readlines()
pa_bot = open(g_root+'img_list_bottom.txt').readlines()
pa_sho = open(g_root+'img_list_shoe.txt').readlines()

data_type = ['train', 'val', 'test']

data_size = [1212, 276, 372]

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
		posi_nega.append(line_p.strip('\r\n')+' '+line_n)
	
	if (i==0):
		for k in range(0,3):
			random.shuffle(posi_nega)
	
	user_num = 800
	for u in range(0,user_num):
		p_k_top = open(l_root+data_type[i]+'_p_top_'+str(u)+'.txt','w')
		p_k_bot = open(l_root+data_type[i]+'_p_bot_'+str(u)+'.txt','w')
		p_k_sho = open(l_root+data_type[i]+'_p_sho_'+str(u)+'.txt','w')
		n_k_top = open(l_root+data_type[i]+'_n_top_'+str(u)+'.txt','w')
		n_k_bot = open(l_root+data_type[i]+'_n_bot_'+str(u)+'.txt','w')
		n_k_sho = open(l_root+data_type[i]+'_n_sho_'+str(u)+'.txt','w')

		if (i==0):
			start_idx = 0
			end_idx = len(posi_nega)
		else:
			start_idx = u*data_size[i]
			end_idx = (u+1)*data_size[i]

		for k in range(start_idx,end_idx):
			#read user idx
			user_idx_temp = int(posi_nega[k].strip('\r\n').split(' ')[0])
			if (user_idx_temp == u):
				#read inter idx
				top_p = posi_nega[k].strip('\r\n').split(' ')[1]
				bot_p = posi_nega[k].strip('\r\n').split(' ')[2]
				sho_p = posi_nega[k].strip('\r\n').split(' ')[3]
				top_n = posi_nega[k].strip('\r\n').split(' ')[5]
				bot_n = posi_nega[k].strip('\r\n').split(' ')[6]
				sho_n = posi_nega[k].strip('\r\n').split(' ')[7]
				#read final idx
				top_p = top[int(top_p)]
				bot_p = bot[int(bot_p)]
				sho_p = sho[int(sho_p)]
				top_n = top[int(top_n)]
				bot_n = bot[int(bot_n)]
				sho_n = sho[int(sho_n)]
				#read image path
				top_p = pa_top[int(top_p)].strip('\r\n')+' 1'+'\r\n'
				bot_p = pa_bot[int(bot_p)].strip('\r\n')+' 1'+'\r\n'
				sho_p = pa_sho[int(sho_p)].strip('\r\n')+' 1'+'\r\n'
				top_n = pa_top[int(top_n)].strip('\r\n')+' 0'+'\r\n'
				bot_n = pa_bot[int(bot_n)].strip('\r\n')+' 0'+'\r\n'
				sho_n = pa_sho[int(sho_n)].strip('\r\n')+' 0'+'\r\n'
				#write to txt: train/val/test_p/n_top/bot/sho_k.txt
				p_k_top.write(top_p)
				p_k_bot.write(bot_p)
				p_k_sho.write(sho_p)
				n_k_top.write(top_n)
				n_k_bot.write(bot_n)
				n_k_sho.write(sho_n)
		p_k_top.close()
		p_k_bot.close()
		p_k_sho.close()
		n_k_top.close()
		n_k_bot.close()
		n_k_sho.close()

	posi.close()
	nega.close()
#####################################################
