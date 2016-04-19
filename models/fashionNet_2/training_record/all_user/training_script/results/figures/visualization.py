#!/usr/bin/env python

import operator

import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

# user_number
root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/'
all_train_size = open(root+'data_size/all_train_size.txt').readlines()
user_num = len(all_train_size)

last_mean_ndcg = 0
optimal_mean_ndcg = 0
first_mean_ndcg = 0
count_l = 0
count_o = 0
count_f = 0

# initialization to zero
last_ndcg_at = [0.0] * 100
optimal_ndcg_at = [0.0] * 100
first_ndcg_at = [0.0] * 100
count_last_ndcg_at = [0.0] * 100
count_optimal_ndcg_at = [0.0] * 100
count_first_ndcg_at = [0.0] * 100

for u in range(0,user_num):
	# read ndcg_mean_label_at_imgIdx.txt
	ndcg = open(root+'training_script/results/data/t2.2.'+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines()
	
	# last mean_ndcg
	temp_l = float(ndcg[-4].strip('\r\n').split(' ')[1])
	last_mean_ndcg += temp_l
	count_l += 1.0
	# optimal mean_ndcg, including initial caffemodel (namely, the general caffemodel)
	mean_ndcg_list = []
	if (len(ndcg)==28):
		mean_ndcg_list.append(float(ndcg[0].strip('\r\n').split(' ')[1]))
	else:
		mean_ndcg_list.append(0.0)
	for l in range(1,7):
		mean_ndcg_list.append(float(ndcg[-4*l].strip('\r\n').split(' ')[1]))
	optimal_idx, temp_o = max(enumerate(mean_ndcg_list), key=operator.itemgetter(1))
	optimal_mean_ndcg += temp_o
	count_o += 1.0
	# first mean_ndcg
	if (len(ndcg)==28):
		temp_f = float(ndcg[0].strip('\r\n').split(' ')[1])
		first_mean_ndcg += temp_f
		count_f += 1.0

	# last ndcg_at@(1~100)
	ndcg_size = len(ndcg[-2].strip('\r\n').split(' '))-1
	for n in range(0,ndcg_size):
		last_ndcg_at[n] += float(ndcg[-2].strip('\r\n').split(' ')[n+1])
		count_last_ndcg_at[n] += 1.0
	# optimal ndcg_at@(1~100)
	# optimal_idx += 1
	optimal_idx *= -4
	optimal_idx += 2
	o_ndcg_size = len(ndcg[optimal_idx].strip('\r\n').split(' '))-1
	for n in range(0,o_ndcg_size):
		optimal_ndcg_at[n] += float(ndcg[optimal_idx].strip('\r\n').split(' ')[n+1])
		count_optimal_ndcg_at[n] += 1.0
	# first ndcg_at@(1~100)
	if (len(ndcg)==28):
		f_ndcg_size = len(ndcg[2].strip('\r\n').split(' '))-1
		for n in range(0,f_ndcg_size):
			first_ndcg_at[n] += float(ndcg[2].strip('\r\n').split(' ')[n+1])
			count_first_ndcg_at[n] += 1.0

last_mean_ndcg /= count_l
optimal_mean_ndcg /= count_o
first_mean_ndcg /= count_f

last_optimal_first_mean_ndcg = open(root+'training_script/results/figures/last_optimal_first_mean_ndcg.txt','w')
last_optimal_first_mean_ndcg.write(str(last_mean_ndcg)+' '+str(optimal_mean_ndcg)+' '+str(first_mean_ndcg))
last_optimal_first_mean_ndcg.close

ndcg_at_idx = []
for n in range(0,100):
	last_ndcg_at[n] /= count_last_ndcg_at[n]
	optimal_ndcg_at[n] /= count_optimal_ndcg_at[n]
	first_ndcg_at[n] /= count_first_ndcg_at[n]
	ndcg_at_idx.append(n+1)

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(ndcg_at_idx, last_ndcg_at, '--r', label = 'L_NDCG@')
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '--g', label = 'O_NDCG@')
ax_left.plot(ndcg_at_idx, first_ndcg_at, '--b', label = 'F_NDCG@')
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,100)")
ax_left.set_ylabel("mean_NDCG@")
ax_left.set_title("mean_NDCG@m of [User_0, User_988]")
plt.savefig(root+'training_script/results/figures/NDCG_at.png', bbox_inches='tight')
plt.close('all')

