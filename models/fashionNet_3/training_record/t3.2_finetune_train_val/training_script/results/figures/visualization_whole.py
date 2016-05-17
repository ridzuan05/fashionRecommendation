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
# cmp_initial_ndcg_at = []

new_optimal_ndcg_at = []

ndcg_at_whole = open('../../../../t3.1_finetune_train_val/training_script/results/figures/NDCG_at.txt').readlines()
new_ndcg_at_whole = open('./NDCG_at.txt').readlines()

ndcg_at_length = 30
for i in range(0,ndcg_at_length):
	ndcg_at_idx.append(int(float(ndcg_at_whole[0].strip('\r\n').split(' ')[i])))
	optimal_ndcg_at.append(float(ndcg_at_whole[1].strip('\r\n').split(' ')[i]))
	initial_ndcg_at.append(float(ndcg_at_whole[2].strip('\r\n').split(' ')[i]))
	# cmp_initial_ndcg_at.append(float(ndcg_at_whole[3].strip('\r\n').split(' ')[i]))

	new_optimal_ndcg_at.append(float(new_ndcg_at_whole[0].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '-r', label = 'tsf-1', LineWidth = 3)
ax_left.plot(ndcg_at_idx, new_optimal_ndcg_at, '--g', label = 'tsf-2', LineWidth = 3)
ax_left.plot(ndcg_at_idx, initial_ndcg_at, ':b', label = 'ugf', LineWidth = 3)
# ax_left.plot(ndcg_at_idx, cmp_initial_ndcg_at, '-dc', label = 'nf', LineWidth = 3)
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
# cmp_top_k_initial = []

new_top_k_optimal = []

top_k_posi_num_whole = open('../../../../t3.1_finetune_train_val/training_script/results/figures/top_k_posi_num.txt').readlines()
new_top_k_posi_num_whole = open('./top_k_posi_num.txt').readlines()

for i in range(0,ndcg_at_length):
	top_k_idx.append(int(float(top_k_posi_num_whole[0].strip('\r\n').split(' ')[i])))
	top_k_optimal.append(float(top_k_posi_num_whole[1].strip('\r\n').split(' ')[i]))
	top_k_initial.append(float(top_k_posi_num_whole[2].strip('\r\n').split(' ')[i]))
	# cmp_top_k_initial.append(float(top_k_posi_num_whole[3].strip('\r\n').split(' ')[i]))

	new_top_k_optimal.append(float(new_top_k_posi_num_whole[0].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(top_k_idx, top_k_optimal, '-r', label = 'tsf-1', LineWidth = 3)
ax_left.plot(top_k_idx, new_top_k_optimal, '--g', label = 'tsf-2', LineWidth = 3)
ax_left.plot(top_k_idx, top_k_initial, ':b', label = 'ugf', LineWidth = 3)
# ax_left.plot(top_k_idx, cmp_top_k_initial, '-dc', label = 'nf', LineWidth = 3)
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("k = (1,2,...,30)")
ax_left.set_ylabel("posivie outfit number")
ax_left.set_title("Top-k positive outfit number")
plt.savefig('./top_k_posi_num.png', bbox_inches='tight')
plt.close('all')