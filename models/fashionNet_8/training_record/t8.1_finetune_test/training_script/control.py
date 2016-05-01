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

# test User_idx
uID = '^666^'

# results folder
recordDir = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_test/training_script/results/'
recordDir_data = recordDir+'data/U_'+uID+'/'

if 'results' not in os.listdir('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_test/training_script/'):
    os.system('mkdir '+recordDir)

if 'data' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'data')

if 'figures' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'figures')

if 'U_^666^' not in os.listdir(recordDir+'data/'):
    os.system('mkdir '+recordDir_data)

# caffemodel_idx
cID = []
optimal_meanNDCG_row_id_value_whole = open(recordDir_data+'optimal_meanNDCG_row_id_value.txt').readlines()
cID.append('239168')
cID.append(optimal_meanNDCG_row_id_value_whole[0].strip('\r\n').split(' ')[1])
cID.append('0')
cID.append(optimal_meanNDCG_row_id_value_whole[1].strip('\r\n').split(' ')[1])

# set gpu idx
caffe.set_mode_gpu()
caffe.set_device(2)

def test_avg(test_iter, img_idx, test_tuple_num):
        
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

            # compute test_avg_accu/loss
            if (diff > 0):
                avg_accu += 1.0
            avg_loss += np.log(1+1.0/np.exp(diff))

            # for scores_pos & nr_tuples_pos[count_posi] & img_idx_pos
            if  ((img_idx%6==0) and (posi_pref_score<=false_posi_thresh)):
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
            img_idx %= test_tuple_num

            # stop when test_dataset has all been tested
            if (img_idx==0):
                if (i != (test_iter-1)):
                    # ERROR
                    while(1):
                        print("ERROR@U_^666^, i != (test_iter-1), ({},{})".format(i,test_iter))
                break

    avg_accu = float(float(avg_accu) / float(test_tuple_num))
    avg_loss = float(float(avg_loss) / float(test_tuple_num))
           
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

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','w')
ndcg_mean_label_at_imgIdx_f.close()

# cmp_ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'cmp_ndcg_mean_label_at_imgIdx.txt','w')
ndcg_mean_label_at_imgIdx_f.close()

# test_avg_accu_loss.txt
test_avg_accu_loss_f = open(recordDir_data+'test_avg_accu_loss.txt','w')
test_avg_accu_loss_f.close()

# solver
solver = caffe.SGDSolver('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_test/solver_prototxt/fashion_solver_8_k/fashion_solver_8_'+uID+'.prototxt')

test_iter = 8 # 1 test epoch

# test_tuple_num
test_tuple_num = 372

# user_number
user_num = 800

img_idx = 0

optimal_ndcg_at = []
optimal_ndcg_at_idx = []

first_ndcg_at = []
first_ndcg_at_idx = []

cmp_optimal_ndcg_at = []
cmp_optimal_ndcg_at_idx = []

cmp_first_ndcg_at = []
cmp_first_ndcg_at_idx = []

for c in range(0,len(cID)):

    # caffemodel
    if (c%2==0):
        caffemodel_path = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_train_val/fashion_params_8_'+cID[c]+'.caffemodel'
    else:
        caffemodel_path = recordDir_data+'cmp_fashion_params_8_'+cID[c]+'.caffemodel'
    solver.net.copy_from(caffemodel_path)
    solver.test_nets[0].copy_from(caffemodel_path)

    test_avg_accu = 0
    test_avg_loss = 0

    # validation
    test_avg_accu,test_avg_loss,\
    scores_pos,scores_neg,\
    nr_tuples_pos,nr_tuples_neg,\
    img_idx_pos,img_idx_neg \
    = test_avg(test_iter,img_idx,test_tuple_num)
    # test_avg_accu_loss.txt
    test_avg_accu_loss_f = open(recordDir_data+'test_avg_accu_loss.txt','a')
    # softmax test accu/loss
    test_avg_accu_loss_f.write(cID[c]+' '+str(test_avg_accu)+' '+str(test_avg_loss)+'\r\n')
    # test_avg_accu_loss_f.txt
    test_avg_accu_loss_f.close()
    print("\n{}~[U_{}/{}]Iters done:{}, test_avg_accu={}, test_avg_loss={}.\n".format(c,int(uID),user_num,cID[c],test_avg_accu,test_avg_loss))

    # ndcg computation
    mean_ndcg,ndcg_at,\
    ndcg_label,ndcg_imgIdx\
    = get_ndcg(scores_pos,scores_neg,\
               nr_tuples_pos,nr_tuples_neg,\
               img_idx_pos,img_idx_neg)

    # record mean_ndcg & ndcg_label & ndcg_at & ndcg_imgIdx
    if (c%2==0):
        ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','a')
    else:
        ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'cmp_ndcg_mean_label_at_imgIdx.txt','a')
    ndcg_mean_label_at_imgIdx_f.write(cID[c]+' '+str(mean_ndcg)+'\r\n') # mean_ndcg 
    temp = str(ndcg_at[0])
    temp0 = str(ndcg_label[0])
    temp1 = str(ndcg_imgIdx[0])
    for n in range(1,len(ndcg_at)):
        temp += ' '+str(ndcg_at[n])
        temp0 += ' '+str(ndcg_label[n])
        temp1 += ' '+str(ndcg_imgIdx[n])
    ndcg_mean_label_at_imgIdx_f.write(cID[c]+' '+temp0+'\r\n') # ndcg_label (0 or 1)
    ndcg_mean_label_at_imgIdx_f.write(cID[c]+' '+temp+'\r\n') # ndcg_at
    ndcg_mean_label_at_imgIdx_f.write(cID[c]+' '+temp1+'\r\n') # ndcg_imgIdx
    ndcg_mean_label_at_imgIdx_f.close()
    
    if (c==3):
        # NDCG_at.png
        ndcg = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt').readlines()

        # optimal ndcg_at@(1~30)
        o_ndcg_size = len(ndcg[-2].strip('\r\n').split(' '))-1
        for n in range(0,o_ndcg_size):
            optimal_ndcg_at_idx.append(n+1)
            optimal_ndcg_at.append(float(ndcg[-2].strip('\r\n').split(' ')[n+1]))

        # first ndcg_at@(1~30)
        f_ndcg_size = len(ndcg[2].strip('\r\n').split(' '))-1
        for n in range(0,f_ndcg_size):
            first_ndcg_at_idx.append(n+1)
            first_ndcg_at.append(float(ndcg[2].strip('\r\n').split(' ')[n+1]))    

        # NDCG_at.png
        ndcg = open(recordDir_data+'cmp_ndcg_mean_label_at_imgIdx.txt').readlines()

        # optimal ndcg_at@(1~30)
        o_ndcg_size = len(ndcg[-2].strip('\r\n').split(' '))-1
        for n in range(0,o_ndcg_size):
            cmp_optimal_ndcg_at_idx.append(n+1)
            cmp_optimal_ndcg_at.append(float(ndcg[-2].strip('\r\n').split(' ')[n+1]))

        # first ndcg_at@(1~30)
        f_ndcg_size = len(ndcg[2].strip('\r\n').split(' '))-1
        for n in range(0,f_ndcg_size):
            cmp_first_ndcg_at_idx.append(n+1)
            cmp_first_ndcg_at.append(float(ndcg[2].strip('\r\n').split(' ')[n+1]))

        fig = plt.figure()
        ax_left = fig.add_subplot(111)
        ax_left.plot(optimal_ndcg_at_idx, optimal_ndcg_at, '--g', label = 'Optimal_NDCG@')
        ax_left.plot(first_ndcg_at_idx, first_ndcg_at, '--b', label = 'Initial_NDCG@')
        ax_left.plot(cmp_optimal_ndcg_at_idx, cmp_optimal_ndcg_at, '-.g', label = 'Cmp_Optimal_NDCG@')
        ax_left.plot(cmp_first_ndcg_at_idx, cmp_first_ndcg_at, '-.b', label = 'Cmp_Initial_NDCG@')
        lines_left, labels_left = ax_left.get_legend_handles_labels()   
        ax_left.legend(lines_left, labels_left, loc=0)
        ax_left.grid()
        ax_left.set_xlabel("m = (1,2,...,30)")
        ax_left.set_ylabel("mean_NDCG@")
        ax_left.set_title("mean_NDCG@m of User_{}".format(uID))
        plt.savefig(recordDir_data+'NDCG_at.png', bbox_inches='tight')
        plt.close('all')

