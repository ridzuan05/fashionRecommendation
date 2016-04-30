#!/usr/bin/env python

import os

l_root = "/home/dell/fashionRecommendation/models/fashionNet_3_dell/data_prep/"

if 'tvt_pn_tbs_k_txt' not in os.listdir(l_root+'imgdata_list'):
    os.system('mkdir '+l_root+"imgdata_list/tvt_pn_tbs_k_txt")

data_type = ['train_', 'val_', 'test_']
data_attr = ['p_', 'n_']
item_type = ['top_', 'bot_', 'sho_']

user_num = 800
for u in range(0,user_num):
	for i in range(0,len(data_type)):
		for a in range(0, len(data_attr)):
			for k in range(0,len(item_type)):

				imgData_source = open(l_root+'lmdb_list/tvt_pn_tbs_k_txt/'+data_type[i]+data_attr[a]+item_type[k]+str(u)+'.txt')
				imgData_target = open(l_root+'imgdata_list/tvt_pn_tbs_k_txt/'+data_type[i]+data_attr[a]+item_type[k]+str(u)+'.txt','w')

				for line in imgData_source:
					line_temp = line.split('/')
					new_line = "/ssd_data/dell/fashion/"+line_temp[9]+"/"+line_temp[12]
					imgData_target.write(new_line)

				imgData_source.close()
				imgData_target.close()
