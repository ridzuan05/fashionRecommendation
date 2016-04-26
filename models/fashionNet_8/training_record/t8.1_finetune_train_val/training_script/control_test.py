#!/usr/bin/env python

# training_script for [U_0, U_799]

# test User_idx
tUID = '0'
# caffemodel_idx
cID = '239168'
# U_k(next i=0)[15_0.0001*(0,1)] training epoch
end_iter = 1230 # 30 training epoch
# set gpu idx
caffe.set_mode_gpu()
caffe.set_device(0)

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

def test_avg(val_iter, img_idx, val_tuple_num):
        
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

    for i in range(0,val_iter):
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
                if (i != (val_iter-1)):
                    # ERROR
                    while(1):
                        print("ERROR@U_^666^, i != (val_iter-1), ({},{})".format(i,val_iter))
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
solver = caffe.SGDSolver('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/solver_prototxt/fashion_solver_8_k/fashion_solver_8_'+tUID+'.prototxt')

# caffemodel
caffemodel_path = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_train_val/fashion_params_8_'+cID+'.caffemodel'
solver.net.copy_from(caffemodel_path)
solver.test_nets[0].copy_from(caffemodel_path)

# results folder
recordDir = '/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/training_script/results/'
recordDir_data = recordDir+'data/U_test/'

if 'results' not in os.listdir('/local2/home/tong/fashionRecommendation/models/fashionNet_8/training_record/t8.1_finetune_train_val/training_script/'):
    os.system('mkdir '+recordDir)

if 'data' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'data')

if 'figures' not in os.listdir(recordDir):
    os.system('mkdir '+recordDir+'figures')

if ('U_test') not in os.listdir(recordDir+'data/'):
    os.system('mkdir '+recordDir_data)

k = 0
start_iter = 0
val_interval = 8 # 1/5 training epoch
visual_interval = 4 # 1/10 training epoch
val_iter = 6 # 1 test epoch

params = net.params.keys()

solver.net.forward()

train_sum_accu = (start_iter+1)*0
train_sum_loss = (start_iter+1)*0

train_avg_accu = 0
train_avg_loss = 0

train_bat_accu = 0
train_bat_loss = 0

val_avg_accu = 0
val_avg_loss = 0

img_idx = 0

# ndcg_mean_label_at_imgIdx.txt
ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','w')
ndcg_mean_label_at_imgIdx_f.close()

# train_avg_bat_accu_loss.txt
tr_avg_bat_accu_loss = open(recordDir_data+'train_avg_bat_accu_loss.txt','w')
tr_avg_bat_accu_loss.close()

# val_avg_accu_loss.txt
val_avg_accu_loss_f = open(recordDir_data+'val_avg_accu_loss.txt','w')
val_avg_accu_loss_f.close()

# val_tuple_num
val_tuple_num = 276

# user_number
user_num = 800

# for saving caffemodel for optimal mean_ndcg
optimal_mean_ndcg = []

for i in range (start_iter,end_iter+1):
    # save train data (just for reference, not using threshold_fp=0.999)
    train_bat_accu = solver.net.blobs['accuracy'].data
    train_bat_loss = solver.net.blobs['rank_loss'].data
    train_sum_accu = train_sum_accu + train_bat_accu
    train_sum_loss = train_sum_loss + train_bat_loss
    train_avg_accu = train_sum_accu/(i+1)
    train_avg_loss = train_sum_loss/(i+1)
    tr_avg_bat_accu_loss = open(recordDir_data+'train_avg_bat_accu_loss.txt','a')
    tr_avg_bat_accu_loss.write(str(i)+' '+str(train_avg_accu)+' '+str(train_avg_loss)+' '+str(train_bat_accu)+' '+str(train_bat_loss)+'\r\n')
    tr_avg_bat_accu_loss.close()
    if(i%visual_interval==0):
        print("\n[U_{}/{}]Iters done:{}/{}, train_avg_accu={}, train_avg_loss={}.\n".format(int(tUID),user_num,i,end_iter,train_avg_accu,train_avg_loss))
        print("                              train_bat_accu={}, train_bat_loss={}.\n".format(train_bat_accu,train_bat_loss))

    # validation, save caffemodel, and stop criteria
    if ((i%val_interval==0) or (i==end_iter)):

        # validation
        val_avg_accu,val_avg_loss,\
        scores_pos,scores_neg,\
        nr_tuples_pos,nr_tuples_neg,\
        img_idx_pos,img_idx_neg \
        = test_avg(val_iter,img_idx,val_tuple_num)
        # val_avg_accu_loss.txt
        val_avg_accu_loss_f = open(recordDir_data+'val_avg_accu_loss.txt','a')
        # softmax test accu/loss
        val_avg_accu_loss_f.write(str(i)+' '+str(val_avg_accu)+' '+str(val_avg_loss)+'\r\n')
        # val_avg_accu_loss_f.txt
        val_avg_accu_loss_f.close()
        print("\n[U_0/{}]Iters done:{}/{}, val_avg_accu={}, val_avg_loss={}.\n".format(user_num,i,end_iter,val_avg_accu,val_avg_loss))
        
        # ndcg computation
        mean_ndcg,ndcg_at,\
        ndcg_label,ndcg_imgIdx\
        = get_ndcg(scores_pos,scores_neg,\
        	  	   nr_tuples_pos,nr_tuples_neg,\
        		   img_idx_pos,img_idx_neg)
        # record mean_ndcg & ndcg_label & ndcg_at & ndcg_imgIdx
        optimal_mean_ndcg.append(mean_ndcg)
        ndcg_mean_label_at_imgIdx_f = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt','a')
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
        ndcg_mean_label_at_imgIdx_f.close()

        # avg_bat_record.png
        train_avg_bat_accu_loss_whole = []
        val_avg_accu_loss_whole = []
        train_avg_bat_accu_loss_whole = open(recordDir_data+'train_avg_bat_accu_loss.txt').readlines() 
        val_avg_accu_loss_whole = open(recordDir_data+'val_avg_accu_loss.txt').readlines()
        train_iter_idx = []
        train_loss = []
        train_accuracy = []
        val_iter_idx = []
        val_loss = []
        val_accuracy = []
        for i in range(0, len(train_avg_bat_accu_loss_whole)):
            if i % visual_interval == 0: # 1/10 training epoch
                train_iter_idx.append(int(train_avg_bat_accu_loss_whole[i].strip('\r\n').split(' ')[0]))
                train_loss.append(float(train_avg_bat_accu_loss_whole[i].strip('\r\n').split(' ')[1]))
                train_accuracy.append(float(train_avg_bat_accu_loss_whole[i].strip('\r\n').split(' ')[2]))
        for i in range(0, len(val_avg_accu_loss_whole)):
            val_iter_idx.append(int(val_avg_accu_loss_whole[i].strip('\r\n').split(' ')[0]))
            val_loss.append(float(val_avg_accu_loss_whole[i].strip('\r\n').split(' ')[1]))
            val_accuracy.append(float(val_avg_accu_loss_whole[i].strip('\r\n').split(' ')[2]))
        fig = plt.figure()
        ax_left = fig.add_subplot(111)
        ax_left.plot(train_iter_idx, train_loss, '--rp', label = 'Avg_T_Loss')
        ax_left.plot(val_iter_idx, val_loss, '--gp', label = 'Avg_V_Loss')
        ax_right = ax_left.twinx()
        ax_right.plot(train_iter_idx, train_accuracy, '-bp', label = 'Avg_T_Accuracy')
        ax_right.plot(val_iter_idx, val_accuracy, '-yp', label = 'Avg_V_Accuracy')
        lines_left, labels_left = ax_left.get_legend_handles_labels()
        lines_right, labels_right = ax_right.get_legend_handles_labels()
        ax_right.legend(lines_left + lines_right, labels_left + labels_right, loc=0)
        ax_left.grid()
        ax_left.set_xlabel("Training Iterations Done(n)")
        ax_left.set_ylabel("Loss")
        ax_right.set_ylabel("Accuracy")
        ax_right.set_title("HVA@({:.3f},{}), LVL@({:.3f},{})".format(max(val_accuracy),val_iter_idx[val_accuracy.index(max(val_accuracy))],min(val_loss),val_iter_idx[val_loss.index(min(val_loss))]))
        plt.savefig(recordDir_data+'avg_bat_record.png', bbox_inches='tight')
        plt.close('all')

        # bat_bat_record.png
        train_loss = []
        train_accuracy = []
        for i in range(0, len(train_avg_bat_accu_loss_whole)):
            if i % visual_interval == 0: # 1/10 training epoch
                train_loss.append(float(train_avg_bat_accu_loss_whole[i].strip('\r\n').split(' ')[3]))
                train_accuracy.append(float(train_avg_bat_accu_loss_whole[i].strip('\r\n').split(' ')[4]))
        fig = plt.figure()
        ax_left = fig.add_subplot(111)
        ax_left.plot(train_iter_idx, train_loss, '--rp', label = 'Bat_T_Loss')
        ax_left.plot(val_iter_idx, val_loss, '--gp', label = 'Avg_V_Loss')
        ax_right = ax_left.twinx()
        ax_right.plot(train_iter_idx, train_accuracy, '-bp', label = 'Bat_T_Accuracy')
        ax_right.plot(val_iter_idx, val_accuracy, '-yp', label = 'Avg_V_Accuracy')
        lines_left, labels_left = ax_left.get_legend_handles_labels()
        lines_right, labels_right = ax_right.get_legend_handles_labels()
        ax_right.legend(lines_left + lines_right, labels_left + labels_right, loc=0)
        ax_left.grid()
        ax_left.set_xlabel("Training Iterations Done(n)")
        ax_left.set_ylabel("Loss")
        ax_right.set_ylabel("Accuracy")
        ax_right.set_title("HVA@({:.3f},{}), LVL@({:.3f},{})".format(max(val_accuracy),val_iter_idx[val_accuracy.index(max(val_accuracy))],min(val_loss),val_iter_idx[val_loss.index(min(val_loss))]))
        plt.savefig(recordDir_data+'bat_bat_record.png', bbox_inches='tight')
        plt.close('all')

        # initial/optimal/last_ndcg_at.png
        ndcg = open(recordDir_data+'ndcg_mean_label_at_imgIdx.txt').readlines()
        ndcg_size = len(ndcg[-2].strip('\r\n').split(' '))-1        
        # last ndcg_at@(1~30)
        last_ndcg_at = []
        for n in range(0,ndcg_size):
            last_ndcg_at.append(float(ndcg[-2].strip('\r\n').split(' ')[n+1]))
        # optimal ndcg_at@(1~30)
        optimal_idx, max_mean_ndcg = max(enumerate(optimal_mean_ndcg), key=operator.itemgetter(1))
        optimal_idx *= val_interval
        optimal_idx += 2
        o_ndcg_size = len(ndcg[optimal_idx].strip('\r\n').split(' '))-1
        optimal_ndcg_at = []
        for n in range(0,o_ndcg_size):
            optimal_ndcg_at.append(float(ndcg[optimal_idx].strip('\r\n').split(' ')[n+1]))
        # first ndcg_at@(1~30)
        f_ndcg_size = len(ndcg[2].strip('\r\n').split(' '))-1
        first_ndcg_at = []
        for n in range(0,f_ndcg_size):
            first_ndcg_at.append(float(ndcg[2].strip('\r\n').split(' ')[n+1]))       
        fig = plt.figure()
        ax_left = fig.add_subplot(111)
        ax_left.plot(ndcg_at_idx, last_ndcg_at, '--r', label = 'L_NDCG@')
        ax_left.plot(ndcg_at_idx, optimal_ndcg_at, '--g', label = 'O_NDCG@')
        ax_left.plot(ndcg_at_idx, first_ndcg_at, '--b', label = 'I_NDCG@')
        lines_left, labels_left = ax_left.get_legend_handles_labels()   
        ax_left.legend(lines_left, labels_left, loc=0)
        ax_left.grid()
        ax_left.set_xlabel("m = (1,2,...,30)")
        ax_left.set_ylabel("mean_NDCG@")
        ax_left.set_title("mean_NDCG@m of User_{}".format(tUID))
        plt.savefig(recordDir_data+'NDCG_at_temp.png', bbox_inches='tight')
        plt.close('all')

        if (i==end_iter):
            initial_mNDCG = float(ndcg[0].strip('\r\n').split(' ')[0]) 
            optimal_mNDCG = max_mean_ndcg
            last_mNDCG = float(ndcg[-4].strip('\r\n').split(' ')[0])
            print("meanNDCG: Initial({}), Optimal({}), Last({})" \
                  .format(initial_mNDCG,optimal_mNDCG,last_mNDCG))

        # stop criteria
        if val_avg_accu > 0.93:
            k += 1
            if (k > 10):
                print '\n\nTest accuracy: {} > 0.93 counted for 10 times\n\n'.format(val_avg_accu)
                break

    # update parameters
    solver.step(1)
