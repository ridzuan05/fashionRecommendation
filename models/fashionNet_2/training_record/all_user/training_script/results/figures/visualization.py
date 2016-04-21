#!/usr/bin/env python

import operator

import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

import os

import Image

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
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '--g', label = 'Optimal_NDCG@')
ax_left.plot(ndcg_at_idx, first_ndcg_at, '--b', label = 'Initial_NDCG@')
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,100)")
ax_left.set_ylabel("mean_NDCG@")
ax_left.set_title("mean_NDCG@m of [User_0, User_988]")
plt.savefig(root+'training_script/results/figures/NDCG_at.png', bbox_inches='tight')
plt.close('all')

fig = plt.figure()
ax_left = fig.add_subplot(111)
ax_left.plot(ndcg_at_idx, last_ndcg_at, '--r', label = 'L_NDCG@')
ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '--g', label = 'O_NDCG@')
ax_left.plot(ndcg_at_idx, first_ndcg_at, '--b', label = 'I_NDCG@')
lines_left, labels_left = ax_left.get_legend_handles_labels()   
ax_left.legend(lines_left, labels_left, loc=0)
ax_left.grid()
ax_left.set_xlabel("m = (1,2,...,100)")
ax_left.set_ylabel("mean_NDCG@")
ax_left.set_title("mean_NDCG@m of [User_0, User_988]")
plt.savefig(root+'training_script/results/figures/NDCG_at_temp.png', bbox_inches='tight')
plt.close('all')

#=======================================================

if 'charts' not in os.listdir(root+'training_script/results/figures/'):
    os.system('mkdir '+root+'training_script/results/figures/charts/')

if 'best' not in os.listdir(root+'training_script/results/figures/charts/'):
	os.system('mkdir '+root+'training_script/results/figures/charts/best/')

if 'worst' not in os.listdir(root+'training_script/results/figures/charts/'):
	os.system('mkdir '+root+'training_script/results/figures/charts/worst/')

# drawing retrieval images
whole_ndcg_label = []
whole_ndcg_imgIdx = []
whole_top_10_pos_num = []
for u in range(0,user_num):
	# read ndcg_mean_label_at_imgIdx.txt
	ndcg = open(root+'training_script/results/data/t2.2.'+str(u)+'/ndcg_mean_label_at_imgIdx.txt').readlines()

	# optimal idx
	mean_ndcg_list = []
	mean_ndcg_list.append(float(ndcg[0].strip('\r\n').split(' ')[1]))
	for l in range(1,7):
		mean_ndcg_list.append(float(ndcg[-4*l].strip('\r\n').split(' ')[1]))
	optimal_idx, temp_o = max(enumerate(mean_ndcg_list), key=operator.itemgetter(1))
	optimal_idx *= -4
	optimal_idx += 2

	# whole_ndcg_label
	whole_ndcg_label.append(ndcg[optimal_idx-1])
	# whole_ndcg_imgIdx
	whole_ndcg_imgIdx.append(ndcg[optimal_idx+1])

	# top-10 positive tuple number
	top_10_pos_num = 0
	for t in range(0,10):
		if (1==int(float(whole_ndcg_label[-1].strip('\r\n').split(' ')[t+1]))):
			top_10_pos_num += 1

	# whole_top_10_pos_num
	whole_top_10_pos_num.append(top_10_pos_num)

max_top_10_pos_num = max(whole_top_10_pos_num)
min_top_10_pos_num = min(whole_top_10_pos_num)
print("max_top_10_pos_num = {}, min_top_10_pos_num = {}".format(max_top_10_pos_num,min_top_10_pos_num))

path_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/imgdata_list/val_'
# !666!_top.txt

# retrieve best top_10 outfits for 4 users
best_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/training_script/results/figures/charts/best/'
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
					top_paths = open(path_root+str(single_max_index)+'_top.txt').readlines()
					bot_paths = open(path_root+str(single_max_index)+'_bot.txt').readlines()
					sho_paths = open(path_root+str(single_max_index)+'_sho.txt').readlines()
					single_ndcg_imgIdx = whole_ndcg_imgIdx[single_max_index].strip('\r\n').split(' ')[1:11]
					blank_image = Image.new("RGB", (224*10, 224*3))
					for p in range(0,10):
						temp_imgIdx = int(float(single_ndcg_imgIdx[p]))

						# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
						top_path = top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/top_'+str(p)+'.png'
						top_img = Image.open(top_path)
						blank_image.paste(top_img,(p*224,224*0))
						
						# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
						bot_path = bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/bot_'+str(p)+'.png'
						bot_img = Image.open(bot_path)
						blank_image.paste(bot_img,(p*224,224*1))

						# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
						sho_path = sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/sho_'+str(p)+'.png'
						sho_img = Image.open(sho_path)
						blank_image.paste(sho_img,(p*224,224*2))
					
					# save ./chars/best/U_k(best_u_count)/outfits_10.png
					blank_image.save(best_root+U_k+'/outfits_10.png')

					# write ./charts/best/U_k(best_u_count)/labels_10.txt
					single_ndcg_label_fp = open(best_root+U_k+'/labels_100.txt','w')
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
worst_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/training_script/results/figures/charts/worst/'
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
					top_paths = open(path_root+str(single_min_index)+'_top.txt').readlines()
					bot_paths = open(path_root+str(single_min_index)+'_bot.txt').readlines()
					sho_paths = open(path_root+str(single_min_index)+'_sho.txt').readlines()
					single_ndcg_imgIdx = whole_ndcg_imgIdx[single_min_index].strip('\r\n').split(' ')[1:11]
					blank_image = Image.new("RGB", (224*10, 224*3))
					for p in range(0,10):
						temp_imgIdx = int(float(single_ndcg_imgIdx[p]))

						# read & save ./charts/best/U_k(best_u_count)/top_k(p).png
						top_path = top_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/top_'+str(p)+'.png'
						top_img = Image.open(top_path)
						blank_image.paste(top_img,(p*224,224*0))
						
						# read & save ./charts/best/U_k(best_u_count)/bot_k(p).png
						bot_path = bot_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/bot_'+str(p)+'.png'
						bot_img = Image.open(bot_path)
						blank_image.paste(bot_img,(p*224,224*1))

						# read & save ./charts/best/U_k(best_u_count)/sho_k(p).png
						sho_path = sho_paths[temp_imgIdx].strip('\r\n').split(' ')[0]
						# save_path = best_root+U_k+'/sho_'+str(p)+'.png'
						sho_img = Image.open(sho_path)
						blank_image.paste(sho_img,(p*224,224*2))
					
					# save ./chars/best/U_k(best_u_count)/outfits_10.png
					blank_image.save(worst_root+U_k+'/outfits_10.png')

					# write ./charts/best/U_k(best_u_count)/labels_10.txt
					single_ndcg_label_fp = open(worst_root+U_k+'/labels_100.txt','w')
					single_ndcg_label_fp.write(whole_ndcg_label[single_min_index])
					single_ndcg_label_fp.write('U_'+str(single_min_index)+'\r\n')
					single_ndcg_label_fp.close()
					worst_u_count += 1

		if (worst_u_count == 4):
			flag_n = 1
			break	
	if (flag_n == 1):
		break