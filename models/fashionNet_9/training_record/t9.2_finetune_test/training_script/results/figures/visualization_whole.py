#!/usr/bin/env python

import operator
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import os
import Image

##########################################

ndcg_at_idx = []
optimal_ndcg_at = []
initial_ndcg_at = []
cmp_initial_ndcg_at = []

new_optimal_ndcg_at = []

ndcg_at_whole = open('../../../../t9.1_finetune_test/training_script/results/figures/NDCG_at.txt').readlines()
new_ndcg_at_whole = open('./NDCG_at.txt').readlines()

ndcg_at_length = 30
for i in range(0,ndcg_at_length):
	ndcg_at_idx.append(int(float(ndcg_at_whole[0].strip('\r\n').split(' ')[i])))
	optimal_ndcg_at.append(float(ndcg_at_whole[1].strip('\r\n').split(' ')[i]))
	initial_ndcg_at.append(float(ndcg_at_whole[2].strip('\r\n').split(' ')[i]))
	cmp_initial_ndcg_at.append(float(ndcg_at_whole[3].strip('\r\n').split(' ')[i]))

	new_optimal_ndcg_at.append(float(new_ndcg_at_whole[0].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)
plt.ylim([0,1])
plt.xlim([1,30])
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '-r', label = 'two-stage (whole)', LineWidth = 3)
ax_left.plot(ndcg_at_idx, new_optimal_ndcg_at, '--g', label = 'two-stage (partial)', LineWidth = 3)
ax_left.plot(ndcg_at_idx, initial_ndcg_at, ':b', label = 'the first stage', LineWidth = 3)
ax_left.plot(ndcg_at_idx, cmp_initial_ndcg_at, '.c', label = 'no training', LineWidth = 3)
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,30)")
ax_left.set_ylabel("NDCG@m")
ax_left.set_title("NDCG@m")
plt.savefig('./NDCG_at_whole.png', bbox_inches='tight')
plt.close('all')

##########################################

top_k_idx = []
top_k_optimal = []
top_k_initial = []
cmp_top_k_initial = []

new_top_k_optimal = []

top_k_posi_num_whole = open('../../../../t9.1_finetune_test/training_script/results/figures/top_k_posi_num.txt').readlines()
new_top_k_posi_num_whole = open('./top_k_posi_num.txt').readlines()

for i in range(0,ndcg_at_length):
	top_k_idx.append(int(float(top_k_posi_num_whole[0].strip('\r\n').split(' ')[i])))
	top_k_optimal.append(float(top_k_posi_num_whole[1].strip('\r\n').split(' ')[i]))
	top_k_initial.append(float(top_k_posi_num_whole[2].strip('\r\n').split(' ')[i]))
	cmp_top_k_initial.append(float(top_k_posi_num_whole[3].strip('\r\n').split(' ')[i]))

	new_top_k_optimal.append(float(new_top_k_posi_num_whole[0].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)
plt.ylim([0,30])
plt.xlim([1,30])
ax_left.plot(top_k_idx, top_k_optimal, '-r', label = 'two-stage (whole)', LineWidth = 3)
ax_left.plot(top_k_idx, new_top_k_optimal, '--g', label = 'two-stage (partial)', LineWidth = 3)
ax_left.plot(top_k_idx, top_k_initial, ':b', label = 'the first stage', LineWidth = 3)
ax_left.plot(top_k_idx, cmp_top_k_initial, '.c', label = 'no training', LineWidth = 3)
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("k = (1,2,...,30)")
ax_left.set_ylabel("posivie outfit number")
ax_left.set_title("Top-k positive outfit number")
plt.savefig('./top_k_posi_num.png', bbox_inches='tight')
plt.close('all')

##########################################

path_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/data_prep/imgdata_list/tvt_pn_tbs_k_txt/test_'

f1 = open('./top_k_posi_num_all_users.txt').readlines()
f2 = open('./top_k_posi_num_all_users_partiall.txt').readlines()

initial_top5 = f1[0].strip('\r\n').split(' ')
initial_top10 = f1[1].strip('\r\n').split(' ')
stage_one_top5 = f1[2].strip('\r\n').split(' ')
stage_one_top10 = f1[3].strip('\r\n').split(' ')
stage_two_whole_top5 = f1[4].strip('\r\n').split(' ')
stage_two_whole_top10 = f1[5].strip('\r\n').split(' ')

stage_two_partial_top5 = f2[0].strip('\r\n').split(' ')
stage_two_partial_top10 = f2[1].strip('\r\n').split(' ')

large_figure_data = open('./large_figure_data.txt').readlines()
large_figure_data_partial = open('./large_figure_data_partial.txt').readlines()

userNum = 800

######### U_0

for u in range(0,userNum):
	if ((int(initial_top5[u]) >= 0) and (int(initial_top5[u]) <= 0)):
		if ((int(initial_top10[u]) >= 1) and (int(initial_top10[u]) <= 1)):
			if ((int(stage_one_top5[u]) >= 1) and (int(stage_one_top5[u]) <= 2)):
				if ((int(stage_one_top10[u]) >= 4) and (int(stage_one_top10[u]) <= 6)):
					if ((int(stage_two_partial_top5[u]) >= 4) and (int(stage_two_partial_top5[u]) <= 5)):
						if ((int(stage_two_partial_top10[u]) >= 8) and (int(stage_two_partial_top10[u]) <= 10)):
							if ((int(stage_two_whole_top5[u]) >= 4) and (int(stage_two_whole_top5[u]) <= 5)):
								if ((int(stage_two_whole_top10[u]) >= 8) and (int(stage_two_whole_top10[u]) <= 10)):
									break

targetUser0 = u

p_top_paths = open(path_root+'p_top_'+str(targetUser0)+'.txt').readlines()
p_bot_paths = open(path_root+'p_bot_'+str(targetUser0)+'.txt').readlines()
p_sho_paths = open(path_root+'p_sho_'+str(targetUser0)+'.txt').readlines()
n_top_paths = open(path_root+'n_top_'+str(targetUser0)+'.txt').readlines()
n_bot_paths = open(path_root+'n_bot_'+str(targetUser0)+'.txt').readlines()
n_sho_paths = open(path_root+'n_sho_'+str(targetUser0)+'.txt').readlines()

initial_labels = large_figure_data[targetUser0*6+0].strip('\r\n').split(' ')
stage_one_labels = large_figure_data[targetUser0*6+2].strip('\r\n').split(' ')
stage_two_partial_labels = large_figure_data_partial[targetUser0*2+0].strip('\r\n').split(' ')
stage_two_whole_labels =  large_figure_data[targetUser0*6+4].strip('\r\n').split(' ')

initial_imgIdxs = large_figure_data[targetUser0*6+1].strip('\r\n').split(' ')
stage_one_imgIdxs = large_figure_data[targetUser0*6+3].strip('\r\n').split(' ')
stage_two_partial_imgIdxs = large_figure_data_partial[targetUser0*2+1].strip('\r\n').split(' ')
stage_two_whole_imgIdxs =  large_figure_data[targetUser0*6+5].strip('\r\n').split(' ')

blank_image = Image.new("RGB", (224*10, 224*12))

for i in range(0,10):

	initial_label = int(float(initial_labels[i+1]))
	stage_one_label = int(float(stage_one_labels[i+1]))
	stage_two_partial_label = int(float(stage_two_partial_labels[i+1]))
	stage_two_whole_label = int(float(stage_two_whole_labels[i+1]))

	initial_imgIdx = int(float(initial_imgIdxs[i+1]))
	stage_one_imgIdx = int(float(stage_one_imgIdxs[i+1]))
	stage_two_partial_imgIdx = int(float(stage_two_partial_imgIdxs[i+1]))
	stage_two_whole_imgIdx = int(float(stage_two_whole_imgIdxs[i+1]))

	if (initial_label == 1):
		top_path = p_top_paths[initial_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = p_bot_paths[initial_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = p_sho_paths[initial_imgIdx].strip('\r\n').split(' ')[0]
	elif (initial_label == 0):	
		top_path = n_top_paths[initial_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = n_bot_paths[initial_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = n_sho_paths[initial_imgIdx].strip('\r\n').split(' ')[0]

	top_img = Image.open(top_path)
	blank_image.paste(top_img,(i*224,224*0))
	bot_img = Image.open(bot_path)
	blank_image.paste(bot_img,(i*224,224*1))
	sho_img = Image.open(sho_path)
	blank_image.paste(sho_img,(i*224,224*2))

	if (stage_one_label == 1):
		top_path = p_top_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = p_bot_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = p_sho_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]
	elif (stage_one_label == 0):	
		top_path = n_top_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = n_bot_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = n_sho_paths[stage_one_imgIdx].strip('\r\n').split(' ')[0]

	top_img = Image.open(top_path)
	blank_image.paste(top_img,(i*224,224*3))
	bot_img = Image.open(bot_path)
	blank_image.paste(bot_img,(i*224,224*4))
	sho_img = Image.open(sho_path)
	blank_image.paste(sho_img,(i*224,224*5))

	if (stage_two_partial_label == 1):
		top_path = p_top_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = p_bot_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = p_sho_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]
	elif (stage_two_partial_label == 0):	
		top_path = n_top_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = n_bot_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = n_sho_paths[stage_two_partial_imgIdx].strip('\r\n').split(' ')[0]

	top_img = Image.open(top_path)
	blank_image.paste(top_img,(i*224,224*6))
	bot_img = Image.open(bot_path)
	blank_image.paste(bot_img,(i*224,224*7))
	sho_img = Image.open(sho_path)
	blank_image.paste(sho_img,(i*224,224*8))

	if (stage_two_whole_label == 1):
		top_path = p_top_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = p_bot_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = p_sho_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]
	elif (stage_two_whole_label == 0):	
		top_path = n_top_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]
		bot_path = n_bot_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]
		sho_path = n_sho_paths[stage_two_whole_imgIdx].strip('\r\n').split(' ')[0]

	top_img = Image.open(top_path)
	blank_image.paste(top_img,(i*224,224*9))
	bot_img = Image.open(bot_path)
	blank_image.paste(bot_img,(i*224,224*10))
	sho_img = Image.open(sho_path)
	blank_image.paste(sho_img,(i*224,224*11))

blank_image.save('./U_'+str(targetUser0)+'.png')