#!/usr/bin/env python

import operator
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import os
import Image

# plt.rcParams['axes.linewidth'] = 2
# plt.rcParams['lines.linewidth'] = 50
# plt.rcParams.update({'font.size': 15})

##########################################

ndcg_at_idx = []
optimal_ndcg_at = []
initial_ndcg_at = []
cmp_initial_ndcg_at = []

cmp_optimal_ndcg_at = []

ndcg_at_whole = open('./NDCG_at.txt').readlines()

ndcg_at_length = 30
for i in range(0,ndcg_at_length):
	ndcg_at_idx.append(int(float(ndcg_at_whole[0].strip('\r\n').split(' ')[i])))
	optimal_ndcg_at.append(float(ndcg_at_whole[1].strip('\r\n').split(' ')[i]))
	initial_ndcg_at.append(float(ndcg_at_whole[2].strip('\r\n').split(' ')[i]))
	cmp_optimal_ndcg_at.append(float(ndcg_at_whole[3].strip('\r\n').split(' ')[i]))
	cmp_initial_ndcg_at.append(float(ndcg_at_whole[4].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)

ax_left.plot(ndcg_at_idx, cmp_initial_ndcg_at, '.r', label = 'Initial', LineWidth = 8)
ax_left.plot(ndcg_at_idx, initial_ndcg_at, ':b', label = 'Stage one', LineWidth = 8)
ax_left.plot(ndcg_at_idx, cmp_optimal_ndcg_at, '--k', label = 'Stage two (direct)', LineWidth = 4)
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '-c', label = 'Stage two (whole)', LineWidth = 4)
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=1)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,30)")
ax_left.set_ylabel("NDCG@m")
ax_left.set_title("NDCG@m", fontsize='x-large') 

plt.ylim([0,1])
plt.xlim([1,30])
ax_left.xaxis.get_label().set_size('x-large')
ax_left.yaxis.get_label().set_size('x-large')
for label in ax_left.xaxis.get_ticklabels():
    label.set_fontsize(18)
for label in ax_left.yaxis.get_ticklabels():
    label.set_fontsize(18) 
leg = ax_left.get_legend()
if(leg):
    ltext  = leg.get_texts()  # all the text.Text instance in the legend      
    plt.setp(ltext, fontsize='x-large')

plt.legend(loc='upper center', bbox_to_anchor=(0.6,0.99),ncol=2,fancybox=True,shadow=True)

plt.savefig('./NDCG_at.png', bbox_inches='tight')
plt.close('all')

##########################################

top_k_idx = []
top_k_optimal = []
top_k_initial = []
cmp_top_k_initial = []

cmp_top_k_optimal = []

top_k_posi_num_whole = open('./top_k_posi_num.txt').readlines()

for i in range(0,ndcg_at_length):
	top_k_idx.append(int(float(top_k_posi_num_whole[0].strip('\r\n').split(' ')[i])))
	top_k_optimal.append(float(top_k_posi_num_whole[1].strip('\r\n').split(' ')[i]))
	top_k_initial.append(float(top_k_posi_num_whole[2].strip('\r\n').split(' ')[i]))
	cmp_top_k_optimal.append(float(top_k_posi_num_whole[3].strip('\r\n').split(' ')[i]))
	cmp_top_k_initial.append(float(top_k_posi_num_whole[4].strip('\r\n').split(' ')[i]))

fig = plt.figure()
ax_left = fig.add_subplot(111)

ax_left.plot(top_k_idx, cmp_top_k_initial, '.r', label = 'Initial', LineWidth = 8)
ax_left.plot(top_k_idx, top_k_initial, ':b', label = 'Stage one', LineWidth = 8)
ax_left.plot(top_k_idx, cmp_top_k_optimal, '--k', label = 'Stage two (direct)', LineWidth = 4)
ax_left.plot(top_k_idx, top_k_optimal, '-c', label = 'Stage two (whole)', LineWidth = 4)
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=1)
ax_left.grid()
ax_left.set_xlabel("k = (1,2,...,30)")
ax_left.set_ylabel("posivie outfit number")
ax_left.set_title("Top-k positive outfit number", fontsize='x-large')

plt.ylim([0,30])
plt.xlim([1,30])
ax_left.xaxis.get_label().set_size('x-large')
ax_left.yaxis.get_label().set_size('x-large')
for label in ax_left.xaxis.get_ticklabels():
    label.set_fontsize(18)
for label in ax_left.yaxis.get_ticklabels():
    label.set_fontsize(18) 
leg = ax_left.get_legend()
if(leg):
    ltext  = leg.get_texts()  # all the text.Text instance in the legend      
    plt.setp(ltext, fontsize='x-large')

plt.legend(loc='upper center', bbox_to_anchor=(0.6,0.99),ncol=2,fancybox=True,shadow=True)

plt.savefig('./top_k_posi_num.png', bbox_inches='tight')
plt.close('all')
