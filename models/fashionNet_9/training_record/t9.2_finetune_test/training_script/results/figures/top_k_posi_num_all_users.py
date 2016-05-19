#!/usr/bin/env python

import operator
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import os
import Image

userNum = 800

root1 = '/local2/home/tong/fashionRecommendation/models/fashionNet_9/training_record/t9.1_finetune_test/training_script/results/data/U_'
root2 = '/home/dell/fashionRecommendation/models/fashionNet_9/training_record/t9.2_finetune_test/training_script/results/data/U_'

new = 1

##############################################################

if (new == 0):

	initial_top5 = ''
	initial_top10 = ''
	stage_one_top5 = ''
	stage_one_top10 = ''
	stage_two_whole_top5 = ''
	stage_two_whole_top10 = ''

	large_figure_data_fp = open('./large_figure_data.txt','w')
	large_figure_data_fp.close()

	for u in range(0,userNum):

		initial_top5_temp = 0
		initial_top10_temp = 0
		stage_one_top5_temp = 0
		stage_one_top10_temp = 0
		stage_two_whole_top5_temp = 0
		stage_two_whole_top10_temp = 0

		f1 = open(root1+str(u)+'/cmp_ndcg_mean_label_at_imgIdx.txt').readlines()
		f2 = open(root1+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines()

		initial = f1[1].strip('\r\n').split(' ')
		stage_one = f2[1].strip('\r\n').split(' ')
		stage_two_whole = f2[-3].strip('\r\n').split(' ')

		for i in range(0,10):

			if (i < 5):
				if (float(initial[i+1]) == 1.0):
					initial_top5_temp += 1
				if (float(stage_one[i+1]) == 1.0):
					stage_one_top5_temp += 1
				if (float(stage_two_whole[i+1]) == 1.0):
					stage_two_whole_top5_temp += 1			

			if (float(initial[i+1]) == 1.0):
				initial_top10_temp += 1
			if (float(stage_one[i+1]) == 1.0):
				stage_one_top10_temp += 1
			if (float(stage_two_whole[i+1]) == 1.0):
				stage_two_whole_top10_temp += 1		

		initial_top5 += str(initial_top5_temp)+' '
		initial_top10 += str(initial_top10_temp)+' '
		stage_one_top5 += str(stage_one_top5_temp)+' '
		stage_one_top10 += str(stage_one_top10_temp)+' '
		stage_two_whole_top5 += str(stage_two_whole_top5_temp)+' '
		stage_two_whole_top10 += str(stage_two_whole_top10_temp)+' '

		large_figure_data_fp = open('./large_figure_data.txt','a')
		large_figure_data_fp.write(f1[1])
		large_figure_data_fp.write(f1[3])
		large_figure_data_fp.write(f2[1])
		large_figure_data_fp.write(f2[3])
		large_figure_data_fp.write(f2[-3])
		large_figure_data_fp.write(f2[-1])
		large_figure_data_fp.close()

	top_k_posi_num_all_users_fp = open('./top_k_posi_num_all_users.txt','w')
	top_k_posi_num_all_users_fp.write(initial_top5+'\r\n')
	top_k_posi_num_all_users_fp.write(initial_top10+'\r\n')
	top_k_posi_num_all_users_fp.write(stage_one_top5+'\r\n')
	top_k_posi_num_all_users_fp.write(stage_one_top10+'\r\n')
	top_k_posi_num_all_users_fp.write(stage_two_whole_top5+'\r\n')
	top_k_posi_num_all_users_fp.write(stage_two_whole_top10+'\r\n')
	top_k_posi_num_all_users_fp.close()

##############################################################

elif (new == 1):

	stage_two_partial_top5 = ''
	stage_two_partial_top10 = ''

	large_figure_data_partial_fp = open('./large_figure_data_partial.txt','w')
	large_figure_data_partial_fp.close()
	
	for u in range(0,userNum):

		stage_two_partial_top5_temp = 0
		stage_two_partial_top10_temp = 0

		f3 = open(root2+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines()

		stage_two_partial = f3[1].strip('\r\n').split(' ')

		for i in range(0,10):

			if (i < 5):
				if (float(stage_two_partial[i+1]) == 1.0):
					stage_two_partial_top5_temp += 1		

			if (float(stage_two_partial[i+1]) == 1.0):
				stage_two_partial_top10_temp += 1

		stage_two_partial_top5 += str(stage_two_partial_top5_temp)+' '
		stage_two_partial_top10 += str(stage_two_partial_top10_temp)+' '

		large_figure_data_partial_fp = open('./large_figure_data_partial.txt','a')
		large_figure_data_partial_fp.write(f3[1])
		large_figure_data_partial_fp.write(f3[3])
		large_figure_data_partial_fp.close()

	top_k_posi_num_all_users_fp = open('./top_k_posi_num_all_users_partiall.txt','w')
	top_k_posi_num_all_users_fp.write(stage_two_partial_top5+'\r\n')
	top_k_posi_num_all_users_fp.write(stage_two_partial_top10+'\r\n')
	top_k_posi_num_all_users_fp.close()
