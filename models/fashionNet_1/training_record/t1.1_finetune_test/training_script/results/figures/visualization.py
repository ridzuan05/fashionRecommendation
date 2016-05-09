#!/usr/bin/env python

import operator
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import os
import Image

root = '/local2/home/tong/fashionRecommendation/models/fashionNet_1/training_record/t1.1_finetune_test/'

# user_number
user_num = 800

optimal_mean_ndcg = 0.0
initial_mean_ndcg = 0.0
# cmp_optimal_mean_ndcg = 0.0
# cmp_initial_mean_ndcg = 0.0

count_o = 0.0
count_i = 0.0
# cmp_count_o = 0.0
# cmp_count_i = 0.0

optimal_initial_idx = []
optimal_initial_mean_ndcg = []
# cmp_optimal_initial_idx = []
# cmp_optimal_initial_mean_ndcg = []

# initialization to zero
optimal_ndcg_at = [0.0] * 30
initial_ndcg_at = [0.0] * 30
# cmp_optimal_ndcg_at = [0.0] * 30
# cmp_initial_ndcg_at = [0.0] * 30

count_optimal_ndcg_at = [0.0] * 30
count_initial_ndcg_at = [0.0] * 30
# cmp_count_optimal_ndcg_at = [0.0] * 30
# cmp_count_initial_ndcg_at = [0.0] * 30

posi_num_length = 10
optimal_top10_posi_num = 0.0
initial_top10_posi_num = 0.0
# cmp_optimal_top10_posi_num = 0.0
# cmp_initial_top10_posi_num = 0.0

if 'charts' not in os.listdir(root+'training_script/results/figures/'):
    os.system('mkdir '+root+'training_script/results/figures/charts/')

if 'best' not in os.listdir(root+'training_script/results/figures/charts/'):
	os.system('mkdir '+root+'training_script/results/figures/charts/best/')

if 'worst' not in os.listdir(root+'training_script/results/figures/charts/'):
	os.system('mkdir '+root+'training_script/results/figures/charts/worst/')

# for drawing retrieval images
whole_ndcg_label = []
whole_ndcg_imgIdx = []
whole_top_10_pos_num = []

for u in range(0,user_num):
	# read ndcg_mean_label_at_imgIdx.txt
	ndcg = open(root+'training_script/results/data/U_'+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines()
	# cmp_ndcg = open(root+'training_script/results/data/U_'+str(u)+'/cmp_ndcg_mean_label_at_imgIdx.txt').readlines()
	
	optimal_idx = -2
	temp_o = float(ndcg[-4].strip('\r\n').split(' ')[1])

	# cmp_optimal_idx = -2
	# cmp_temp_o = float(cmp_ndcg[-4].strip('\r\n').split(' ')[1])
	
	optimal_mean_ndcg += temp_o
	count_o += 1.0
	# cmp_optimal_mean_ndcg += cmp_temp_o
	# cmp_count_o += 1.0

	optimal_top10_posi_num_temp = 0.0

	for i in range(0,posi_num_length):
		if (1==int(float(ndcg[-3].strip('\r\n').split(' ')[i+1]))):
			optimal_top10_posi_num_temp += 1.0
		if (1==int(float(ndcg[1].strip('\r\n').split(' ')[i+1]))):
			initial_top10_posi_num += 1.0
		# if (1==int(float(cmp_ndcg[-3].strip('\r\n').split(' ')[i+1]))):
		# 	cmp_optimal_top10_posi_num += 1.0
		# if (1==int(float(cmp_ndcg[1].strip('\r\n').split(' ')[i+1]))):
		# 	cmp_initial_top10_posi_num += 1.0
	optimal_top10_posi_num += optimal_top10_posi_num_temp

	# initial mean_ndcg
	temp_i = float(ndcg[0].strip('\r\n').split(' ')[1])
	initial_mean_ndcg += temp_i
	count_i += 1.0
	# cmp_temp_i = float(cmp_ndcg[0].strip('\r\n').split(' ')[1])
	# cmp_initial_mean_ndcg += cmp_temp_i
	# cmp_count_i += 1.0

	# (optimal_mean_ndcg / initial_mean_ndcg)
	optimal_initial_mean_ndcg.append(float(temp_o/temp_i))
	optimal_initial_idx.append(u)
	# cmp_optimal_initial_mean_ndcg.append(float(cmp_temp_o/cmp_temp_i))
	# cmp_optimal_initial_idx.append(u)

	# optimal ndcg_at@(1~30)
	o_ndcg_size = len(ndcg[optimal_idx].strip('\r\n').split(' '))-1
	for n in range(0,o_ndcg_size):
		optimal_ndcg_at[n] += float(ndcg[optimal_idx].strip('\r\n').split(' ')[n+1])
		count_optimal_ndcg_at[n] += 1.0
	# cmp_o_ndcg_size = len(cmp_ndcg[cmp_optimal_idx].strip('\r\n').split(' '))-1
	# for n in range(0,cmp_o_ndcg_size):
	# 	cmp_optimal_ndcg_at[n] += float(cmp_ndcg[cmp_optimal_idx].strip('\r\n').split(' ')[n+1])
	# 	cmp_count_optimal_ndcg_at[n] += 1.0

	# initial ndcg_at@(1~30)
	i_ndcg_size = len(ndcg[2].strip('\r\n').split(' '))-1
	for n in range(0,i_ndcg_size):
		initial_ndcg_at[n] += float(ndcg[2].strip('\r\n').split(' ')[n+1])
		count_initial_ndcg_at[n] += 1.0
	# cmp_i_ndcg_size = len(cmp_ndcg[2].strip('\r\n').split(' '))-1
	# for n in range(0,cmp_i_ndcg_size):
	# 	cmp_initial_ndcg_at[n] += float(cmp_ndcg[2].strip('\r\n').split(' ')[n+1])
	# 	cmp_count_initial_ndcg_at[n] += 1.0

	# whole_ndcg_label
	whole_ndcg_label.append(ndcg[optimal_idx-1])
	# whole_ndcg_imgIdx
	whole_ndcg_imgIdx.append(ndcg[optimal_idx+1])

	# whole_top_10_pos_num
	whole_top_10_pos_num.append(int(optimal_top10_posi_num_temp))

optimal_mean_ndcg /= count_o
initial_mean_ndcg /= count_i
optimal_top10_posi_num /= count_o
initial_top10_posi_num /= count_i
gain = optimal_mean_ndcg/initial_mean_ndcg
if (initial_top10_posi_num==0):
	num_gain = 999
else:
	num_gain = optimal_top10_posi_num/initial_top10_posi_num

# cmp_optimal_mean_ndcg /= cmp_count_o
# cmp_initial_mean_ndcg /= cmp_count_i
# cmp_optimal_top10_posi_num /= cmp_count_o
# cmp_initial_top10_posi_num /= cmp_count_i
# cmp_gain = cmp_optimal_mean_ndcg/cmp_initial_mean_ndcg
# if (cmp_initial_top10_posi_num==0):
# 	cmp_num_gain = 999
# else:
# 	cmp_num_gain = cmp_optimal_top10_posi_num/cmp_initial_top10_posi_num

optimal_initial_mean_ndcg_fp = open(root+'training_script/results/figures/optimal_initial_mean_ndcg.txt','w')
optimal_initial_mean_ndcg_fp.write(str(optimal_mean_ndcg)+' '+str(initial_mean_ndcg)+' '+str(gain)+'\r\n')
# optimal_initial_mean_ndcg_fp.write(str(cmp_optimal_mean_ndcg)+' '+str(cmp_initial_mean_ndcg)+' '+str(cmp_gain)+'\r\n')
optimal_initial_mean_ndcg_fp.close

top10_posi_num_fp = open(root+'training_script/results/figures/top10_posi_num.txt','w')
top10_posi_num_fp.write(str(optimal_top10_posi_num)+' '+str(initial_top10_posi_num)+' '+str(num_gain)+'\r\n')
# top10_posi_num_fp.write(str(cmp_optimal_top10_posi_num)+' '+str(cmp_initial_top10_posi_num)+' '+str(cmp_num_gain)+'\r\n')
top10_posi_num_fp.close()

ndcg_at_length = 30
ndcg_at_idx = []
for n in range(0,ndcg_at_length):
	optimal_ndcg_at[n] /= count_optimal_ndcg_at[n]
	# cmp_optimal_ndcg_at[n] /= cmp_count_optimal_ndcg_at[n]
	initial_ndcg_at[n] /= count_initial_ndcg_at[n]
	# cmp_initial_ndcg_at[n] /= cmp_count_initial_ndcg_at[n]
	ndcg_at_idx.append(n+1)

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '--g', label = 'Optimal_NDCG@')
ax_left.plot(ndcg_at_idx, initial_ndcg_at, '--b', label = 'Initial_NDCG@')
# ax_left.plot(ndcg_at_idx, cmp_optimal_ndcg_at, '-.g', label = 'Cmp_Optimal_NDCG@')
# ax_left.plot(ndcg_at_idx, cmp_initial_ndcg_at, '-.b', label = 'Cmp_Initial_NDCG@')
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,30)")
ax_left.set_ylabel("mean_NDCG@")
ax_left.set_title("mean_NDCG@m of [User_0, User_799]")
plt.savefig(root+'training_script/results/figures/NDCG_at.png', bbox_inches='tight')
plt.close('all')

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(optimal_initial_idx, optimal_initial_mean_ndcg, '--g', label = 'Finetune')
# ax_left.plot(cmp_optimal_initial_idx, cmp_optimal_initial_mean_ndcg, '--b', label = 'Direct')
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("u = (0,1,...,799)")
ax_left.set_ylabel("mean_NDCG_gain")
ax_left.set_title("Optimal/Initial_mean_NDCG_gain of [User_0, User_799]")
plt.savefig(root+'training_script/results/figures/mean_NDCG_gain.png', bbox_inches='tight')
plt.close('all')

#=======================================================
# to visualize a big chart with top10 retrieved outfits
#=======================================================
max_top_10_pos_num = max(whole_top_10_pos_num)
min_top_10_pos_num = min(whole_top_10_pos_num)
print("max_top_10_pos_num = {}, min_top_10_pos_num = {}".format(max_top_10_pos_num,min_top_10_pos_num))

path_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/data_prep/imgdata_list/tvt_pn_tbs_k_txt/val_'

# retrieve best top_10 outfits for 4 users
best_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_1/training_record/t1.1_finetune_test/training_script/results/figures/charts/best/'
best_u_count = 0
flag_n = 0
for n in range(max_top_10_pos_num,min_top_10_pos_num-1,-1):
	max_index = [i for i, x in enumerate(whole_top_10_pos_num) if x == n]
	for j in range(0,len(max_index)):
		single_max_index = max_index[j]
		single_ndcg_label = whole_ndcg_label[single_max_index].strip('\r\n').split(' ')
		for k in range(0,5):
			if (0 == int(float(single_ndcg_label[0]))):
				break
			else:
				if (0 == int(float(single_ndcg_label[k+1]))):
					break
				# top-5 are all positive tuples
				if (k == 4):
					print("Best_{}: top_10_pos_num = {}".format(best_u_count, n))
					# U_k = 'U_'+str(single_max_index)
					U_k = 'U_'+str(best_u_count)
					if U_k not in os.listdir(best_root):
					    os.system('mkdir '+best_root+U_k)
					p_top_paths = open(path_root+'p_top_'+str(single_max_index)+'.txt').readlines()
					p_bot_paths = open(path_root+'p_bot_'+str(single_max_index)+'.txt').readlines()
					p_sho_paths = open(path_root+'p_sho_'+str(single_max_index)+'.txt').readlines()
					n_top_paths = open(path_root+'n_top_'+str(single_max_index)+'.txt').readlines()
					n_bot_paths = open(path_root+'n_bot_'+str(single_max_index)+'.txt').readlines()
					n_sho_paths = open(path_root+'n_sho_'+str(single_max_index)+'.txt').readlines()
					single_ndcg_imgIdx = whole_ndcg_imgIdx[single_max_index].strip('\r\n').split(' ')[1:11]
					blank_image = Image.new("RGB", (224*10, 224*3))
					for p in range(0,10):
						temp_imgIdx = int(float(single_ndcg_imgIdx[p]))
						if (1 == int(float(single_ndcg_label[p+1]))):
							# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
							top_path = p_top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
							bot_path = p_bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
							sho_path = p_sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						elif (0 == int(float(single_ndcg_label[p+1]))):
							# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
							top_path = n_top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
							bot_path = n_bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
							sho_path = n_sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]

						# save_path = best_root+U_k+'/top_'+str(p)+'.png'
						top_img = Image.open(top_path)
						blank_image.paste(top_img,(p*224,224*0))
						# save_path = best_root+U_k+'/bot_'+str(p)+'.png'
						bot_img = Image.open(bot_path)
						blank_image.paste(bot_img,(p*224,224*1))
						# save_path = best_root+U_k+'/sho_'+str(p)+'.png'
						sho_img = Image.open(sho_path)
						blank_image.paste(sho_img,(p*224,224*2))
					
					# save ./chars/best/U_k(best_u_count)/outfits_10.png
					blank_image.save(best_root+U_k+'/outfits_10.png')

					# write ./charts/best/U_k(best_u_count)/labels_10.txt
					single_ndcg_label_fp = open(best_root+U_k+'/labels_30.txt','w')
					single_ndcg_label_fp.write(whole_ndcg_label[single_max_index])
					single_ndcg_label_fp.write('U_'+str(single_max_index)+'\r\n')
					single_ndcg_label_fp.close()
					best_u_count += 1

		if (best_u_count == 4):
			flag_n = 1
			break
	if (flag_n == 1):
		break

# retrieve worst top_10 outfits for 4 users
worst_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_1/training_record/t1.1_finetune_test/training_script/results/figures/charts/worst/'
worst_u_count = 0
flag_n = 0
for n in range(min_top_10_pos_num,max_top_10_pos_num+1):
	min_index = [i for i, x in enumerate(whole_top_10_pos_num) if x == n]
	for j in range(0,len(min_index)):
		single_min_index = min_index[j]
		single_ndcg_label = whole_ndcg_label[single_min_index].strip('\r\n').split(' ')
		for k in range(0,5):
			if (0 == int(float(single_ndcg_label[0]))):
				break
			else:
				if (0 == int(float(single_ndcg_label[k+1]))):
					break
				# top-5 are all positive tuples
				if (k == 4):
					print("Worst_{}: top_10_pos_num = {}".format(worst_u_count, n))
					# U_k = 'U_'+str(single_min_index)
					U_k = 'U_'+str(worst_u_count)
					if U_k not in os.listdir(worst_root):
					    os.system('mkdir '+worst_root+U_k)
					p_top_paths = open(path_root+'p_top_'+str(single_max_index)+'.txt').readlines()
					p_bot_paths = open(path_root+'p_bot_'+str(single_max_index)+'.txt').readlines()
					p_sho_paths = open(path_root+'p_sho_'+str(single_max_index)+'.txt').readlines()
					n_top_paths = open(path_root+'n_top_'+str(single_max_index)+'.txt').readlines()
					n_bot_paths = open(path_root+'n_bot_'+str(single_max_index)+'.txt').readlines()
					n_sho_paths = open(path_root+'n_sho_'+str(single_max_index)+'.txt').readlines()
					single_ndcg_imgIdx = whole_ndcg_imgIdx[single_min_index].strip('\r\n').split(' ')[1:11]
					blank_image = Image.new("RGB", (224*10, 224*3))
					for p in range(0,10):
						temp_imgIdx = int(float(single_ndcg_imgIdx[p]))
						if (1 == int(float(single_ndcg_label[p+1]))):
							# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
							top_path = p_top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
							bot_path = p_bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
							sho_path = p_sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						elif (0 == int(float(single_ndcg_label[p+1]))):
							# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
							top_path = n_top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
							bot_path = n_bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
							# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
							sho_path = n_sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]

						# save_path = best_root+U_k+'/top_'+str(p)+'.png'
						top_img = Image.open(top_path)
						blank_image.paste(top_img,(p*224,224*0))
						# save_path = best_root+U_k+'/bot_'+str(p)+'.png'
						bot_img = Image.open(bot_path)
						blank_image.paste(bot_img,(p*224,224*1))
						# save_path = best_root+U_k+'/sho_'+str(p)+'.png'
						sho_img = Image.open(sho_path)
						blank_image.paste(sho_img,(p*224,224*2))
					
					# save ./chars/best/U_k(best_u_count)/outfits_10.png
					blank_image.save(worst_root+U_k+'/outfits_10.png')

					# write ./charts/best/U_k(best_u_count)/labels_10.txt
					single_ndcg_label_fp = open(worst_root+U_k+'/labels_30.txt','w')
					single_ndcg_label_fp.write(whole_ndcg_label[single_min_index])
					single_ndcg_label_fp.write('U_'+str(single_min_index)+'\r\n')
					single_ndcg_label_fp.close()
					worst_u_count += 1

		if (worst_u_count == 4):
			flag_n = 1
			break	
	if (flag_n == 1):
		break