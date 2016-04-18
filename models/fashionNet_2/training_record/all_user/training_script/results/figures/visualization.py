#!/usr/bin/env python

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

for u in range(0,user_num):
	# read ndcg_mean_label_at_imgIdx.txt
	ndcg = open(root+'training_script/results/data/t2.2.'+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines
	# last mean_ndcg
	temp_l = float(ndcg[-4].strip('\r\n').split(' ')[1])
	last_mean_ndcg += temp_l
	count_l += 1.0
	# optimal mean_ndcg
	temp_o = max(float(ndcg[-24].strip('\r\n').split(' ')[1]),\
				 float(ndcg[-20].strip('\r\n').split(' ')[1]),\
				 float(ndcg[-16].strip('\r\n').split(' ')[1]),\
				 float(ndcg[-12].strip('\r\n').split(' ')[1]),\
				 float(ndcg[-8].strip('\r\n').split(' ')[1]),\
				 float(ndcg[-4].strip('\r\n').split(' ')[1]))
	optimal_mean_ndcg += temp_o
	count_o += 1.0
	# first mean_ndcg
	if (len(ndcg)==28):
		temp_f = float(ndcg[0].strip('\r\n').split(' ')[1])
		first_mean_ndcg += temp_f
		count_f += 1.0

last_mean_ndcg /= count_l
optimal_mean_ndcg /= count_o
first_mean_ndcg /= count_f

last_optimal_first_mean_ndcg = open(root+'training_script/figures/last_optimal_first_mean_ndcg.txt','w')
last_optimal_first_mean_ndcg.write(str(last_mean_ndcg)+' '+str(optimal_mean_ndcg)+' '+str(first_mean_ndcg))
last_optimal_first_mean_ndcg.close