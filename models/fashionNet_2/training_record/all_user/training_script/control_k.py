#!/usr/bin/env python

# training_script for all users (0~988)
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

import numpy as np
import sys
sys.path.insert(0,'/local2/home/tong/caffe-master/python')
import caffe

import os
from matplotlib import rc
rc('mathtext', default='regular')

caffe.set_mode_gpu()
caffe.set_device(0)

# solver
solver = caffe.SGDSolver('/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/solver_prototxt/fashion_solver_2_^666^.prototxt')
solver.net.copy_from('/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/t2.1/fashion_params_2_124200.caffemodel')
solver.test_nets[0].copy_from('/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/t2.1/fashion_params_2_124200.caffemodel')

#for saving caffemodel
net = caffe.Net('/local2/home/tong/fashionRecommendation/models/fashionNet_2/fashion_deploy_2.prototxt', caffe.TEST)

# valiation & confusion matix
from sklearn.metrics import confusion_matrix

def test_avg(test_iter, img_idx, test_tuple_num):
    
    y_true = []
    y_pred = []
    
    avg_accu = 0
    avg_loss = 0

    count_posi = 0
    count_nega = 0
    nr_tuples_pos = []
    nr_tuples_neg = []

    scores_pos = []
    scores_neg = []
    	
    img_idx_pos = []
    img_idx_neg = []
    
    for i in range(0,test_iter):
        # one test_batch_size computation
        solver.test_nets[0].forward()
        # for each outfit input
        for j in range(0,len(solver.test_nets[0].blobs['label_top'].data)):
            if (solver.test_nets[0].blobs['metric_fc3_softmax'].data[j][1]<=0.999):
                y_pred.append(0 if solver.test_nets[0].blobs['metric_fc3'].data[j][0]>solver.test_nets[0].blobs['metric_fc3'].data[j][1] else 1)
                y_true.append(int(solver.test_nets[0].blobs['label_top'].data[j]))
                # compute avg_accuracy
                if (y_true[-1]==y_pred[-1]):
                	avg_accu += 1.0
                if(y_true[-1]==0):    
                    # record neg img idx in imgdata.txt
                    img_idx_neg.append(img_idx)
                    # count neg tuple number
                    count_nega = count_nega + 1
                    # record pre_score for this nega outfit
                    scores_neg.append(solver.test_nets[0].blobs['metric_fc3_softmax'].data[j][1])
                    # compute avg_loss
                    avg_loss += (-1*np.log(scores_neg[-1]))
                elif(y_true[-1]==1):
                    # record pos img idx in imgdata.txt
                    img_idx_pos.append(img_idx)
                    # count posi tuple number
                    count_posi = count_posi + 1
                    # record pre_score for this posi outfit
                    scores_pos.append(solver.test_nets[0].blobs['metric_fc3_softmax'].data[j][1])
                    # compute avg_loss
                    avg_loss += (-1*np.log(scores_pos[-1]))
            # record test_top/bot/sho's img_idx
            img_idx += 1
            img_idx %= test_tuple_num

    avg_accu = float(float(avg_accu) / float(len(y_true)))
    avg_loss = float(float(avg_loss) / float(len(y_true)))
           
    cMat = confusion_matrix(y_true, y_pred)
    
    nr_tuples_pos.append(count_posi)
    nr_tuples_neg.append(count_nega)
    
    return avg_accu, avg_loss, cMat, \
           scores_pos, scores_neg, nr_tuples_pos, nr_tuples_neg, \
            img_idx_pos, img_idx_neg
           
def get_ndcg(scores_pos, scores_neg, nr_tuples_pos, nr_tuples_neg,\
			 img_idx_pos, img_idx_neg,\
			 fn_out='', tuples_pos=None, tuples_neg=None, nr_return=0):

	if fn_out != '':
            fid_out = open(fn_out, 'w')

	m = 100 # pre-determined ndcg size
	ndcg_ct = np.zeros(m)
	ndcg_at = np.zeros(m)
	mean_ndcg = 0
	s_ind_pos = 0 # update posi outfit index for each user
	s_ind_neg = 0 # update neutral outfit index for each user
	nr_users = len(nr_tuples_pos) # user number
    
	ndcg_label = []
	ndcg_imgIdx = []
    
	for ui in range(nr_users): # for each user
		count_q = nr_tuples_pos[ui] + nr_tuples_neg[ui] # total outfits (both posi & neutral) number of this user
		label = np.zeros(nr_tuples_pos[ui]+nr_tuples_neg[ui]) # labels for all outfits of this user, 1 for posi & 0 for neutral
		label[:nr_tuples_pos[ui]] = 1
		target = np.empty(nr_tuples_pos[ui]+nr_tuples_neg[ui]) # scores for all outfits (both posi & neutral)
		target[:nr_tuples_pos[ui]] = scores_pos[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]] # scores for posi outfits
		target[nr_tuples_pos[ui]:] = scores_neg[s_ind_neg:s_ind_neg+nr_tuples_neg[ui]] # scores for neutral outfits
        path = np.empty(nr_tuples_pos[ui]+nr_tuples_neg[ui])
        path[:nr_tuples_pos[ui]] = img_idx_pos[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]]
        path[nr_tuples_pos[ui]:] = img_idx_neg[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]]
		if fn_out != '':
			tuples = np.hstack((tuples_pos[:,s_ind_pos:s_ind_pos+nr_tuples_pos[ui]],
								tuples_neg[:,s_ind_neg:s_ind_neg+nr_tuples_neg[ui]]))
		s_ind_pos += nr_tuples_pos[ui]
		s_ind_neg += nr_tuples_neg[ui]

		ndcg_size = min(m, count_q) # actual ndcg size
		ideal_dcg = np.empty(count_q) # for computing ideal ndcg value
		dcg = np.empty(count_q) # for computing dcg (without normalization by N_m yet)
		ndcg = 0
		order = np.argsort(-label) # sort label in descending order, returns the sequential indices of label 
		ideal_dcg[0] = pow(2.0, label[order[0]]) - 1 # compute ideal_ndcg@m (m=1)
		for i in range(1, count_q): # compute ideal_ndcg@m (m=2,...,M), M is total outfits number of this user
			ideal_dcg[i] = ideal_dcg[i-1]+(pow(2.0, label[order[i]])
										   - 1)*np.log(2.0)/np.log(i+1.0)
		order = np.argsort(-target) # sort scores for all outfits in descending order, returns the indices
		dcg[0] = pow(2.0, label[order[0]]) - 1 # compute dcg@m (m=1)
		for i in range(1, count_q): # compute dcg@m (m=2,...,M), M is total outfits number of this user
			dcg[i] = dcg[i-1]+(pow(2.0, label[order[i]])
							   - 1)*np.log(2.0)/np.log(i+1.0)
        for i in range(0, ndcg_size):
            ndcg_label.append(label[order[i]])
            ndcg_imgIdx.append(path[order[i]])
		if ideal_dcg[0] > 0: # at least there should be one posi outfit for this user, or else somehting is wrong here
			for i in range(count_q): # for each @m (m=1,...,M)
				ndcg += dcg[i] / ideal_dcg[i] # add up all ndcg@m (m=1,..,M) for this user
			for i in range(ndcg_size): # compute top 10 ndcg for all users
				ndcg_ct[i] += 1 # record outfits num at each place, among top 10
				ndcg_at[i] += dcg[i] / ideal_dcg[i] # add up ndcg value at each place, among top 10
		else: # if we only have no posi outfit for this user
			ndcg = 0 # ndcg is 0 for this user, because there is not point of ranking anymore for him/here
		m_ndcg = ndcg / count_q # mean ndcg for this user
		mean_ndcg += m_ndcg # add up mean ndcg for all users

		if fn_out != '':
			fid_out.write('%f\n' % m_ndcg)
			n_out = min(count_q, nr_return)
			for i in range(n_out):
				fid_out.write('%d ' % label[order[i]])
				for jj in range(tuples.shape[0]):
					fid_out.write('%d ' % tuples[jj, order[i]])
				fid_out.write('\n')

	mean_ndcg /= nr_users # mean ndcg for all users as a whole
	for i in range(ndcg_size): # top 10 mean ndcg for all users as a whole
		ndcg_at[i] /= ndcg_ct[i]

	if fn_out != '':
		fid_out.close()

	return (mean_ndcg, ndcg_at, ndcg_label, ndcg_imgIdx)
    
#training solver.net
recordDir = '/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/training_script/results/'
recordDir_data = recordDir+'data/t2.2.^666^/'

if 'results' not in os.listdir('/local2/home/tong/fashionRecommendation/models/fashionNet_2/training_record/all_user/training_script/'):
    os.system('mkdir '+recordDir)
    
if 'data' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'data')
    
if 'figures' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'figures')

if 't2.2.^666^' not in os.listdir(recordDir+'data/'):
    os.system('mkdir '+recordDir_data)

k = 0
start_iter = 0
# t2.2.^666^(next i=0)[5_0.05*(0,1)] training epoch
end_iter = ^555^ # training epoch
test_interval = ^777^ # 1/5 train epoch
visual_interval = ^999^ # each train iter
test_iter = ^888^ # 1 test epoch
test_idx = []
caffemodel_num = 6
for i in range(0,caffemodel_num):
    temp = end_iter-i*test_interval
    test_idx.append(temp)

params = net.params.keys()

solver.net.forward()

train_accu = (start_iter+1)*0
train_los = (start_iter+1)*0
train_avg_accu = 0
train_avg_loss = 0
train_cur_accu = 0
train_cur_loss = 0

test_accu = 0
test_loss = 0

img_idx = 0

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','w')
# softmax_test_accu_loss.txt
softmax_test_accu_loss_f = open(recordDir_data+'softmax_test_accu_loss.txt','w')
# conf_mat.txt
conf_mat_f = open(recordDir_data+'conf_mat.txt','w')

# test_tuple_num
test_tuple_num = open('/local2/home/tong/fashionRecommendation/models/fashionNet_2/data_prep/imgdata_list/test_^666^_top.txt').readlines()
test_tuple_num = len(test_tuple_num)

tr_avg_bat_accu_loss = open(recordDir_data+'train_avg_bat_accu_loss.txt','w')
tr_bat_accu_loss = open(recordDir_data+'train_bat_accu_loss.txt','w')

for i in range (start_iter,end_iter+1):
    # save train data (just for reference, not using threshold_fp=0.999)
    train_cur_accu = solver.net.blobs['accuracy'].data
    train_cur_loss = solver.net.blobs['loss'].data
    train_accu = train_accu + train_cur_accu
    train_los = train_los + train_cur_loss
    train_avg_accu = train_accu/(i+1)
    train_avg_loss = train_los/(i+1)
    tr_avg_bat_accu_loss.write(str(i)+' '+str(train_avg_accu)+' '+str(train_avg_loss)+' '+str(train_cur_accu)+' '+str(train_cur_loss)+'\r\n')
    if(i%visual_interval==0):
        print("\n[U_^666^]Iters done:{}/{}, avg_accu={}, avg_loss={}.\n".format(i,end_iter,train_avg_accu,train_avg_loss))
        print("                             bat_accu={}, bat_loss={}.\n".format(train_cur_accu,train_cur_loss))

    # validation, save caffemodel, and stop criteria
    if i in test_idx:
        # validation
        test_accu,test_loss,\
        cMat,\
        scores_pos,scores_neg,\
        nr_tuples_pos,nr_tuples_neg,\
        img_idx_pos,img_idx_neg \
        = test_avg(test_iter,img_idx,test_tuple_num)
        print("\n[U_^666^]Iters done:{}/{}, VAL_accu={}, VAL_loss={}.\n".format(i,end_iter,test_accu,test_loss))
        # ndcg computation
        mean_ndcg,ndcg_at,\
        ndcg_label,ndcg_imgIdx\
        = get_ndcg(scores_pos,scores_neg,\
        	  	   nr_tuples_pos,nr_tuples_neg,\
        		   img_idx_pos,img_idx_neg)
        # softmax test accu/loss
        softmax_test_accu_loss_f.write(str(i)+' '+str(test_accu)+' '+str(test_loss)+'\r\n')
        # confusion matrix (d2d,d2l,l2d,l2l)
        conf_mat_f.write(str(i)+' '+str(cMat[0][0])+' '+str(cMat[0][1])+' '+str(cMat[1][0])+' '+str(cMat[1][1])+'\r\n')
        # record mean_ndcg & ndcg_label & ndcg_at & ndcg_imgIdx
        ndcg_mean_label_at_imgIdx_f.write(str(i)+' '+str(mean_ndcg)+'\r\n') # mean_ndcg 
        temp = str(ndcg_at[0])
        temp0 = str(ndcg_label[0])
        temp1 = str(ndcg_imgIdx[0])
        for n in range(1,len(ndcg_at)):
            temp = ' '+str(ndcg_at[n])
            temp0 = ' '+str(ndcg_label[n])
            temp1 = ' '+str(ndcg_imgIdx[n])
        ndcg_mean_label_at_imgIdx_f.write(str(i)+' '+temp0+'\r\n') # ndcg_label (0 or 1)
        ndcg_mean_label_at_imgIdx_f.write(str(i)+' '+temp+'\r\n') # ndcg_at
        ndcg_mean_label_at_imgIdx_f.write(str(i)+' '+temp1+'\r\n') # ndcg_imgIdx
        
        # save caffemodel
        source_params = {pr: (solver.net.params[pr][0].data,solver.net.params[pr][1].data) for pr in params}
        target_params = {pr: (net.params[pr][0].data,net.params[pr][1].data) for pr in params}
        for pr in params:
            target_params[pr][0][...] = source_params[pr][0] #weights
            target_params[pr][1][...] = source_params[pr][1] #bias
        net.save(recordDir_data+'fashion_params_2_'+str(i)+'.caffemodel') 
        
        # stop criteria
        if test_accu > 0.93:
            k += 1
            if (k > 10):
                print '\n\nTest accuracy: {} > 0.93 counted for 10 times\n\n'.format(test_accu)
                break

    # update parameters
    solver.step(1)

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f.close()
# softmax_test_accu_loss_f.txt
softmax_test_accu_loss_f.close()
# conf_mat.txt
conf_mat_f.close()
# tr_avg_bat_accu_loss.txt
tr_avg_bat_accu_loss.close()