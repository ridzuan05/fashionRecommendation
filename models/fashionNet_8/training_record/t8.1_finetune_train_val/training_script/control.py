#!/usr/bin/env python

# training_script for [U_0, U_799]

import operator

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

# valiation & confusion matix
from sklearn.metrics import confusion_matrix

def test_avg(test_iter, img_idx, val_tuple_num):
        
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
    
    false_posi_thresh = 1.0

    for i in range(0,test_iter):
        # one test_batch_size computation
        solver.test_nets[0].forward()
        # for each outfit input
        for j in range(0,len(solver.test_nets[0].blobs['top'].data)):

            posi_pref_score = solver.test_nets[0].blobs['like'].data[j][0]
            nega_pref_score = solver.test_nets[0].blobs['like_n'].data[j][0]

            diff = posi_pref_score - nega_pref_score

            # compute val_avg_accu/loss
            if (diff > 0):
                avg_accu += 1.0
            avg_loss += np.log(1+1.0/np.exp(diff))

            # for scores_pos & nr_tuples_pos[count_posi] & img_idx_pos
            if  ((j%6==0) and (posi_pref_score<=false_posi_thresh)):
                scores_pos.append(posi_pref_score)
                count_posi += 1
                img_idx_pos.append(img_idx)

            # for scores_neg & nr_tuples_neg[count_nega] & img_idx_neg
            if (nega_pref_score<=false_posi_thresh):
                scores_neg.append(nega_pref_score)
                count_nega += 1
                img_idx_neg.append(img_idx)

            # record test_top/bot/sho's img_idx
            img_idx += 1
            img_idx %= val_tuple_num

            # stop when test_dataset has all been tested
            if (img_idx==0):
                if (i != (test_iter-1)):
                    # ERROR
                    while(1):
                        print("ERROR@U_^666^, i != (test_iter-1), ({},{})".format(i,test_iter))
                break

    avg_accu = float(float(avg_accu) / float(val_tuple_num))
    avg_loss = float(float(avg_loss) / float(val_tuple_num))
           
    nr_tuples_pos.append(count_posi)
    nr_tuples_neg.append(count_nega)
    
    return avg_accu, avg_loss, \
           scores_pos, scores_neg, nr_tuples_pos, nr_tuples_neg, \
            img_idx_pos, img_idx_neg
           
def get_ndcg(scores_pos, scores_neg, nr_tuples_pos, nr_tuples_neg, img_idx_pos, img_idx_neg, fn_out='', tuples_pos=None, tuples_neg=None, nr_return=0):

    if fn_out != '':
        fid_out = open(fn_out, 'w')

    m = 30 # pre-determined ndcg size

    mean_ndcg = 0
    s_ind_pos = 0 # update posi outfit index for each user
    s_ind_neg = 0 # update neutral outfit index for each user
    nr_users = len(nr_tuples_pos) # user number

    ndcg_label = []
    ndcg_imgIdx = []
    
    single_ndcg_size = min(m, (nr_tuples_pos[0] + nr_tuples_neg[0]))
    ndcg_ct = np.zeros(single_ndcg_size)
    ndcg_at = np.zeros(single_ndcg_size)

    for ui in range(nr_users): # for each user
        count_q = nr_tuples_pos[ui] + nr_tuples_neg[ui] # total outfits (both posi & neutral) number of this user
        label = np.zeros(nr_tuples_pos[ui]+nr_tuples_neg[ui]) # labels for all outfits of this user, 1 for posi & 0 for neutral
        label[:nr_tuples_pos[ui]] = 1
        target = np.empty(nr_tuples_pos[ui]+nr_tuples_neg[ui]) # scores for all outfits (both posi & neutral)
        target[:nr_tuples_pos[ui]] = scores_pos[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]] # scores for posi outfits
        target[nr_tuples_pos[ui]:] = scores_neg[s_ind_neg:s_ind_neg+nr_tuples_neg[ui]] # scores for neutral outfits
        path = np.empty(nr_tuples_pos[ui]+nr_tuples_neg[ui])
        path[:nr_tuples_pos[ui]] = img_idx_pos[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]]
        path[nr_tuples_pos[ui]:] = img_idx_neg[s_ind_neg:s_ind_neg+nr_tuples_neg[ui]]
        if fn_out != '':
            tuples = np.hstack((tuples_pos[:,s_ind_pos:s_ind_pos+nr_tuples_pos[ui]],\
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
            ideal_dcg[i] = ideal_dcg[i-1]+(pow(2.0, label[order[i]]) - 1)*np.log(2.0)/np.log(i+1.0)
        order = np.argsort(-target) # sort scores for all outfits in descending order, returns the indices
        dcg[0] = pow(2.0, label[order[0]]) - 1 # compute dcg@m (m=1)
        for i in range(1, count_q): # compute dcg@m (m=2,...,M), M is total outfits number of this user
            dcg[i] = dcg[i-1]+(pow(2.0, label[order[i]]) - 1)*np.log(2.0)/np.log(i+1.0)
        for i in range(0, ndcg_size):
            ndcg_label.append(label[order[i]])
            ndcg_imgIdx.append(int(path[order[i]]))
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
  
#for saving caffemodel
net = caffe.Net('/local2/home/tong/fashionRecommendation/models/fashionNet_8/fashion_deploy_8.prototxt', caffe.TEST)

# solver
solver = caffe.SGDSolver('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/solver_prototxt/fashion_solver_8_k/fashion_solver_8_^666^.prototxt')

# caffemodel
caffemodel_path = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_train_val/fashion_params_8_^333^.caffemodel'
solver.net.copy_from(caffemodel_path)
solver.test_nets[0].copy_from(caffemodel_path)

# set gpu idx
caffe.set_mode_gpu()
caffe.set_device(0)

# results folder
recordDir = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/training_script/results/'
recordDir_data = recordDir+'data/U_^666^/'

if 'results' not in os.listdir('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/training_script/'):
    os.system('mkdir '+recordDir)

if 'data' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'data')

if 'figures' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'figures')

if 'U_^666^' not in os.listdir(recordDir+'data/'):
    os.system('mkdir '+recordDir_data)

k = 0
start_iter = 0
# U_^666^(next i=0)[***_****(0,1)] training epoch
end_iter = ^555^ # training epoch
test_interval = ^777^ # 1/5 train epoch
visual_interval = ^999^ # each train iter
test_iter = ^888^ # 1 test epoch
test_idx = []
test_idx.append(0)
test_num = 6
for i in range(0,test_num):
    temp = end_iter-(test_num-1-i)*test_interval
    test_idx.append(temp)

params = net.params.keys()

solver.net.forward()

train_accu = (start_iter+1)*0
train_los = (start_iter+1)*0

train_avg_accu = 0
train_avg_loss = 0

train_cur_accu = 0
train_cur_loss = 0

val_accu = 0
val_loss = 0

img_idx = 0

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','w')
# rankNet_val_accu_loss.txt
rankNet_val_accu_loss_f = open(recordDir_data+'rankNet_val_accu_loss.txt','w')

# val_tuple_num
val_tuple_num = 276

tr_avg_bat_accu_loss = open(recordDir_data+'train_avg_bat_accu_loss.txt','w')

# user_number
user_num = 800

# for saving caffemodel for optimal mean_ndcg
optimal_mean_ndcg = []
optimal_caffemodel = []

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
        print("\n[U_^666^/{}]Iters done:{}/{}, avg_accu={}, avg_loss={}.\n".format(user_num,i,end_iter,train_avg_accu,train_avg_loss))
        print("                                bat_accu={}, bat_loss={}.\n".format(train_cur_accu,train_cur_loss))

    # validation, save caffemodel, and stop criteria
    if i in test_idx:
        # validation
        val_accu,val_loss,\
        scores_pos,scores_neg,\
        nr_tuples_pos,nr_tuples_neg,\
        img_idx_pos,img_idx_neg \
        = test_avg(test_iter,img_idx,val_tuple_num)
        print("\n[U_^666^/{}]Iters done:{}/{}, VAL_accu={}, VAL_loss={}.\n".format(user_num,i,end_iter,val_accu,val_loss))
        # ndcg computation
        mean_ndcg,ndcg_at,\
        ndcg_label,ndcg_imgIdx\
        = get_ndcg(scores_pos,scores_neg,\
        	  	   nr_tuples_pos,nr_tuples_neg,\
        		   img_idx_pos,img_idx_neg)
        # softmax test accu/loss
        rankNet_val_accu_loss_f.write(str(i)+' '+str(val_accu)+' '+str(val_loss)+'\r\n')
        # record mean_ndcg & ndcg_label & ndcg_at & ndcg_imgIdx
        optimal_mean_ndcg.append(mean_ndcg)
        ndcg_mean_label_at_imgIdx_f.write(str(i)+' '+str(mean_ndcg)+'\r\n') # mean_ndcg 
        temp = str(ndcg_at[0])
        temp0 = str(ndcg_label[0])
        temp1 = str(ndcg_imgIdx[0])
        for n in range(1,len(ndcg_at)):
            temp += ' '+str(ndcg_at[n])
            temp0 += ' '+str(ndcg_label[n])
            temp1 += ' '+str(ndcg_imgIdx[n])
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
        if val_accu > 0.93:
            k += 1
            if (k > 10):
                print '\n\nTest accuracy: {} > 0.93 counted for 10 times\n\n'.format(val_accu)
                break

    # update parameters
    solver.step(1)

# save caffemodel for optimal mean_ndcg of this user
optimal_idx, max_mean_ndcg = max(enumerate(optimal_mean_ndcg), key=operator.itemgetter(1))
for i in range(0,len(test_idx)):
    if (optimal_idx != i):
        os.system('rm '+recordDir_data+'fashion_params_8_'+str(test_idx[i])+'.caffemodel')

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f.close()
# rankNet_val_accu_loss_f.txt
rankNet_val_accu_loss_f.close()
# tr_avg_bat_accu_loss.txt
tr_avg_bat_accu_loss.close()
