from itertools import izip
import re
import random

g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_7/data_prep/general_list/'
l_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_7/data_prep/lmdb_list/'

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
	posi_mid = open(g_root+'tuples_'+data_type[i]+'_posi_mid.txt')
	nega = open(g_root+'tuples_'+data_type[i]+'_neg.txt')

	top = []
	bot = []
	sho = []
	top = open(g_root+'top_ind_'+data_type[i]+'.txt').readlines()
	bot = open(g_root+'bottom_ind_'+data_type[i]+'.txt').readlines()
	sho = open(g_root+'shoe_ind_'+data_type[i]+'.txt').readlines()

	p_top = open(l_root+data_type[i]+'_ll_top.txt','w')
	p_bot = open(l_root+data_type[i]+'_ll_bot.txt','w')
	p_sho = open(l_root+data_type[i]+'_ll_sho.txt','w')
	p_top_mid = open(l_root+data_type[i]+'_mm_top.txt','w')
	p_bot_mid = open(l_root+data_type[i]+'_mm_bot.txt','w')
	p_sho_mid = open(l_root+data_type[i]+'_mm_sho.txt','w')
	n_top = open(l_root+data_type[i]+'_rr_top.txt','w')
	n_bot = open(l_root+data_type[i]+'_rr_bot.txt','w')
	n_sho = open(l_root+data_type[i]+'_rr_sho.txt','w')

	posi_nega = []
	for line_p, line_p_mid, line_n in izip(posi, posi_mid, nega):
		posi_nega.append(line_p.strip('\r\n')+' '+line_p_mid.strip('\r\n')+' '+line_n)

	random.shuffle(posi_nega)
	random.shuffle(posi_nega)
	random.shuffle(posi_nega)

	#divide to txt: p_top/p_bot/p_sho/n_top/n_bot/n_sho
	for i in range(0, len(posi_nega)):
		#read inter idx
		top_p = posi_nega[i].strip('\r\n').split(' ')[1]
		bot_p = posi_nega[i].strip('\r\n').split(' ')[2]
		sho_p = posi_nega[i].strip('\r\n').split(' ')[3]
		top_p_mid = posi_nega[i].strip('\r\n').split(' ')[5]
		bot_p_mid = posi_nega[i].strip('\r\n').split(' ')[6]
		sho_p_mid = posi_nega[i].strip('\r\n').split(' ')[7]
		top_n = posi_nega[i].strip('\r\n').split(' ')[9]
		bot_n = posi_nega[i].strip('\r\n').split(' ')[10]
		sho_n = posi_nega[i].strip('\r\n').split(' ')[11]
		#read final idx
		top_p = top[int(top_p)]
		bot_p = bot[int(bot_p)]
		sho_p = sho[int(sho_p)]
		top_p_mid = top[int(top_p_mid)]
		bot_p_mid = bot[int(bot_p_mid)]
		sho_p_mid = sho[int(sho_p_mid)]
		top_n = top[int(top_n)]
		bot_n = bot[int(bot_n)]
		sho_n = sho[int(sho_n)]
		#read image path
		top_p = pa_top[int(top_p)].strip('\r\n')+' 1'+'\r\n'
		bot_p = pa_bot[int(bot_p)].strip('\r\n')+' 1'+'\r\n'
		sho_p = pa_sho[int(sho_p)].strip('\r\n')+' 1'+'\r\n'
		top_p_mid = pa_top[int(top_p_mid)].strip('\r\n')+' 1'+'\r\n'
		bot_p_mid = pa_bot[int(bot_p_mid)].strip('\r\n')+' 1'+'\r\n'
		sho_p_mid = pa_sho[int(sho_p_mid)].strip('\r\n')+' 1'+'\r\n'
		top_n = pa_top[int(top_n)].strip('\r\n')+' 0'+'\r\n'
		bot_n = pa_bot[int(bot_n)].strip('\r\n')+' 0'+'\r\n'
		sho_n = pa_sho[int(sho_n)].strip('\r\n')+' 0'+'\r\n'
		#write to txt: l_top/l_bot/l_sho/r_top/r_bot/r_sho
		p_top.write(top_p)
		p_bot.write(bot_p)
		p_sho.write(sho_p)
		p_top_mid.write(top_p_mid)
		p_bot_mid.write(bot_p_mid)
		p_sho_mid.write(sho_p_mid)
		n_top.write(top_n)
		n_bot.write(bot_n)
		n_sho.write(sho_n)

	posi.close()
	nega.close()
	p_top.close()
	p_bot.close()
	p_sho.close()
	p_top_mid.close()
	p_bot_mid.close()
	p_sho_mid.close()
	n_top.close()
	n_bot.close()
	n_sho.close()
#####################################################
