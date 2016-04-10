from itertools import izip
import re
import random

g_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/general_list/'
l_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/lmdb_list/'

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
	for m in range(0, len(posi_nega)):
		#read user idx
		user_idx_temp = int(posi_nega[m].strip('\r\n').split(' ')[0])
		user_idx[user_idx_temp] += 1

	random.shuffle(posi_nega)
	random.shuffle(posi_nega)
	random.shuffle(posi_nega)

	#sort user_idx according to their tuples num
	user_idx_sorted = sorted(range(len(user_idx)), key=lambda k: user_idx[k],reverse=True)
	#save imgdata_k_list for Top-10 users
	user_num = 10 # user_num for fine-tuning & ndcg test
	for u in range(0,user_num):
		p_n_k_top = open(l_root+data_type[i]+'_'+str(u)+'_top.txt','w')
		p_n_k_bot = open(l_root+data_type[i]+'_'+str(u)+'_bot.txt','w')
		p_n_k_sho = open(l_root+data_type[i]+'_'+str(u)+'_sho.txt','w')
		for k in range(0,len(posi_nega)):
			#read user idx
			user_idx_temp = int(posi_nega[k].strip('\r\n').split(' ')[0])
			if (user_idx_temp == user_idx_sorted[u]):
				#read label
				label_p_n = int(posi_nega[k].strip('\r\n').split(' ')[4])
				#read inter idx
				top_p_n = posi_nega[k].strip('\r\n').split(' ')[1]
				bot_p_n = posi_nega[k].strip('\r\n').split(' ')[2]
				sho_p_n = posi_nega[k].strip('\r\n').split(' ')[3]
				#read final idx
				top_p_n = top[int(top_p_n)]
				bot_p_n = bot[int(bot_p_n)]
				sho_p_n = sho[int(sho_p_n)]
				#read image path
				if label_p_n == 1:
					top_p_n = pa_top[int(top_p_n)].strip('\r\n')+' 1'+'\r\n'
					bot_p_n = pa_bot[int(bot_p_n)].strip('\r\n')+' 1'+'\r\n'
					sho_p_n = pa_sho[int(sho_p_n)].strip('\r\n')+' 1'+'\r\n'			
				elif label_p_n == 0:
					top_p_n = pa_top[int(top_p_n)].strip('\r\n')+' 0'+'\r\n'
					bot_p_n = pa_bot[int(bot_p_n)].strip('\r\n')+' 0'+'\r\n'
					sho_p_n = pa_sho[int(sho_p_n)].strip('\r\n')+' 0'+'\r\n'
				#write to txt: _top/_bot/_sho
				p_n_k_top.write(top_p_n)
				p_n_k_bot.write(bot_p_n)
				p_n_k_sho.write(sho_p_n)
		p_n_k_top.close()
		p_n_k_bot.close()
		p_n_k_sho.close()

	posi.close()
	nega.close()
#####################################################
