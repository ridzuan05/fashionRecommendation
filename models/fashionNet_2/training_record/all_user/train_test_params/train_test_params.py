#!/usr/bin/env python

import numpy as np

# .txt saved for parametes
param_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/train_test_params/'
recordDir = open(param_root+'recordDir.txt','w') # recordDir
test_iter = open(param_root+'test_iter.txt','w') # test_iter
test_interval = open(param_root+'test_interval.txt','w') # test_interval
visual_interval = open(param_root+'visual_interval.txt','w') # visual_interval
end_iter = open(param_root+'end_iter.txt','w') # end_iter

# load outfit num for train/val/test datasets
size_root = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/'
all_train_size = open(size_root+'data_size/all_train_size.txt').readlines()
all_val_size = open(size_root+'data_size/all_val_size.txt').readlines()
all_test_size = open(size_root+'data_size/all_test_size.txt').readlines()

# train bathc size
train_batch_size = 80
# test batch size
test_batch_size = 50

# user number
user_num = len(all_train_size)

# set parameters for each user
for u in range(0,user_num):
	user_idx = all_train_size[u].split(' ')[0]+' '
	# set recordDir
	recordDir_temp = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/t2.2.'+str(u)+'/'+'\r\n'
	recordDir.write(recordDir_temp)
	# set test_iter
	temp = int(np.ceil(float(all_test_size[u].strip('\r\n').split(' ')[1])/float(test_batch_size)))
	test_iter_temp = user_idx+str(temp)+'\r\n'
	test_iter.write(test_iter_temp)
	# set test_interval
	temp = int(np.floor(np.ceil(float(all_train_size[u].strip('\r\n').split(' ')[1])/float(train_batch_size))/5.0))
	test_interval_temp = user_idx+str(temp)+'\r\n'
	test_interval.write(test_interval_temp)
	# set visual_interval
	temp = 1
	visual_interval_temp = user_idx+str(temp)+'\r\n'
	visual_interval.write(visual_interval_temp)
	# set end_iter
	temp = int(np.ceil(float(all_train_size[u].strip('\r\n').split(' ')[1])/float(train_batch_size))*5)
	end_iter_temp = user_idx+str(temp)+'\r\n'
	end_iter.write(end_iter_temp)

recordDir.close()
test_iter.close()
test_interval.close()
visual_interval.close()
end_iter.close()
