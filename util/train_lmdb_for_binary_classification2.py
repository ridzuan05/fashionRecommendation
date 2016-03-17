#!/usr/bin/env python

#Remaining Issues:
#1. shuffle: YES
#2. (posi, neg) rate: 1-10

print("\nget training tuples\n")
train_tuple_single = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_posi.txt").readlines()
neg_train_tuple_single = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_neg.txt").readlines()

import random

train_tuple = []
random.shuffle(train_tuple_single)
for x in xrange(0,10):
    train_tuple.extend(train_tuple_single)
random.shuffle(train_tuple)

neg_train_tuple = []
random.shuffle(neg_train_tuple_single)
for x in xrange(0,2):
    neg_train_tuple.extend(neg_train_tuple_single)
random.shuffle(neg_train_tuple)

length = (min(len(train_tuple),len(neg_train_tuple)))
print("\ntraining data tuple num: %d\n"%(length))

import re
import Image
import numpy as np

top_train = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/top_ind_train.txt").readlines()
bot_train = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/bottom_ind_train.txt").readlines()
sho_train = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/shoe_ind_train.txt").readlines()
top_path = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_top.txt").readlines()
bot_path = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_bottom.txt").readlines()
sho_path = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_shoe.txt").readlines()

size = 224, 224

#zero mean normalization
caffe_root = '/local2/home/tong/caffe-master/' 
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
blob = caffe.proto.caffe_pb2.BlobProto()
data = open('/local2/home/tong/fashionRecommendation/data/VGG_mean.binaryproto', 'rb' ).read()
blob.ParseFromString(data)
VGG_mean = np.array( caffe.io.blobproto_to_array(blob) )
VGG_mean.astype(np.uint8)

#label 1-score_posi > score_neg
label = np.array([1])

#initilization for speed up
data = np.zeros((108000,18,size[0],size[1]),np.uint8)
labels = np.zeros((108000,1),np.int64)

count = 0

#make lmdb
for x in range(0, length):
    count = count + 1
    if count % 100 == 0:
        print("%d/%d training tuples ready......"%(count, length))
    #inter idx posi & neg
    top_posi_idx1 = re.findall(r'\d+',train_tuple[x])[1]
    bot_posi_idx1 = re.findall(r'\d+',train_tuple[x])[2]
    sho_posi_idx1 = re.findall(r'\d+',train_tuple[x])[3]
    top_nega_idx1 = re.findall(r'\d+',neg_train_tuple[x])[1]
    bot_nega_idx1 = re.findall(r'\d+',neg_train_tuple[x])[2]
    sho_nega_idx1 = re.findall(r'\d+',neg_train_tuple[x])[3]
    #final idx posi & neg
    top_posi_idx2 = top_train[int(top_posi_idx1)]
    bot_posi_idx2 = bot_train[int(bot_posi_idx1)]
    sho_posi_idx2 = sho_train[int(sho_posi_idx1)]
    top_nega_idx2 = top_train[int(top_nega_idx1)]
    bot_nega_idx2 = bot_train[int(bot_nega_idx1)]
    sho_nega_idx2 = sho_train[int(sho_nega_idx1)]
    #image path posi & neg
    top_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_posi_idx2)].strip('\r\n')
    bot_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_posi_idx2)].strip('\r\n')
    sho_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_posi_idx2)].strip('\r\n')
    top_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_nega_idx2)].strip('\r\n')
    bot_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_nega_idx2)].strip('\r\n')
    sho_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_nega_idx2)].strip('\r\n')
    #read images posi & neg
    im_top_posi = Image.open(top_posi_img)
    im_bot_posi = Image.open(bot_posi_img)
    im_sho_posi = Image.open(sho_posi_img)
    im_top_nega = Image.open(top_nega_img)
    im_bot_nega = Image.open(bot_nega_img)
    im_sho_nega = Image.open(sho_nega_img)  
    #resize to the same size posi & neg
    im_top_posi = im_top_posi.resize(size, Image.ANTIALIAS)
    im_bot_posi = im_bot_posi.resize(size, Image.ANTIALIAS)
    im_sho_posi = im_sho_posi.resize(size, Image.ANTIALIAS)
    im_top_nega = im_top_nega.resize(size, Image.ANTIALIAS)
    im_bot_nega = im_bot_nega.resize(size, Image.ANTIALIAS)
    im_sho_nega = im_sho_nega.resize(size, Image.ANTIALIAS)
    #image to nparray
    im_top_posi = np.array(im_top_posi)
    im_bot_posi = np.array(im_bot_posi)
    im_sho_posi = np.array(im_sho_posi)
    im_top_nega = np.array(im_top_nega)
    im_bot_nega = np.array(im_bot_nega)
    im_sho_nega = np.array(im_sho_nega)
    #change type to np.int64, np.uint8 (lmdb)
    label.astype(np.int64)
    im_top_posi.astype(np.uint8)
    im_bot_posi.astype(np.uint8)
    im_sho_posi.astype(np.uint8)
    im_top_nega.astype(np.uint8)
    im_bot_nega.astype(np.uint8)
    im_sho_nega.astype(np.uint8)
    #from (height,width,channel) to (channel,height,width)
    im_top_posi = np.rollaxis(im_top_posi,2,0)
    im_bot_posi = np.rollaxis(im_bot_posi,2,0)
    im_sho_posi = np.rollaxis(im_sho_posi,2,0)
    im_top_nega = np.rollaxis(im_top_nega,2,0)
    im_bot_nega = np.rollaxis(im_bot_nega,2,0)
    im_sho_nega = np.rollaxis(im_sho_nega,2,0)
    #from RGB to BGR
    im_top_posi = np.array([im_top_posi[2,],im_top_posi[1,],im_top_posi[0,]])
    im_bot_posi = np.array([im_bot_posi[2,],im_bot_posi[1,],im_bot_posi[0,]])
    im_sho_posi = np.array([im_sho_posi[2,],im_sho_posi[1,],im_sho_posi[0,]]) 
    im_top_nega = np.array([im_top_nega[2,],im_top_nega[1,],im_top_nega[0,]])
    im_bot_nega = np.array([im_bot_nega[2,],im_bot_nega[1,],im_bot_nega[0,]])
    im_sho_nega = np.array([im_sho_nega[2,],im_sho_nega[1,],im_sho_nega[0,]]) 
    #zero mean normalization
    im_top_posi = im_top_posi - VGG_mean[0,:,:,:]
    im_bot_posi = im_bot_posi - VGG_mean[0,:,:,:]
    im_sho_posi = im_sho_posi - VGG_mean[0,:,:,:]
    im_top_nega = im_top_nega - VGG_mean[0,:,:,:]
    im_bot_nega = im_bot_nega - VGG_mean[0,:,:,:]
    im_sho_nega = im_sho_nega - VGG_mean[0,:,:,:]
    #stack over "channel"
    data[count-1,0:3,:,:] = im_top_posi
    data[count-1,3:6,:,:] = im_bot_posi
    data[count-1,6:9,:,:] = im_sho_posi
    data[count-1,9:12,:,:] = im_top_nega
    data[count-1,12:15,:,:] = im_bot_nega
    data[count-1,15:18,:,:] = im_sho_nega
    labels[count-1,:] = label[0]
    
print("\ntraining tuples num (data):")
print(data.shape)
print("\ntraining tuples num (label):")
print(labels.shape)

print("\nwrite to train LMDB.........\n")
import lmdb
map_size = data.nbytes * 10
env = lmdb.open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/train_tuples_lmdb2', map_size=map_size)
with env.begin(write=True) as txn:     
    # txn is a Transaction object
    for i in range(labels.shape[0]):
        datum = caffe.proto.caffe_pb2.Datum()
        datum.channels = data.shape[1]
        datum.height = data.shape[2]
        datum.width = data.shape[3]
        datum.data = data[i].tobytes()
            
        datum.label = int(labels[i])
        str_id = '{:08}'.format(i)

        txn.put(str_id.encode('ascii'), datum.SerializeToString())
print("\ntrain LMDB finished\n")

################################################

print("\nget testing tuples\n")
test_tuple_single = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_posi.txt").readlines()
neg_test_tuple = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_neg.txt").readlines()

test_tuple = []
random.shuffle(test_tuple_single)
for x in xrange(0,10):
    test_tuple.extend(test_tuple_single)
random.shuffle(test_tuple)

random.shuffle(neg_test_tuple)

length = (min(len(test_tuple),len(neg_test_tuple)))
print("\ntesting data tuple num: %d\n"%(length))

top_test = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/top_ind_test.txt").readlines() 
bot_test = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/bottom_ind_test.txt").readlines()
sho_test = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/shoe_ind_test.txt").readlines()

#initilization for speed up
data = np.zeros((length,18,size[0],size[1]),np.uint8)
labels = np.zeros((length,1),np.int64)

count = 0

#make lmdb
for x in range(0, length):
    count = count + 1
    if count % 100 == 0:
        print("%d/%d testing tuples ready......"%(count, length))
    #inter idx posi & neg
    top_posi_idx1 = re.findall(r'\d+',test_tuple[x])[1]
    bot_posi_idx1 = re.findall(r'\d+',test_tuple[x])[2]
    sho_posi_idx1 = re.findall(r'\d+',test_tuple[x])[3]
    top_nega_idx1 = re.findall(r'\d+',neg_test_tuple[x])[1]
    bot_nega_idx1 = re.findall(r'\d+',neg_test_tuple[x])[2]
    sho_nega_idx1 = re.findall(r'\d+',neg_test_tuple[x])[3]
    #final idx posi & neg
    top_posi_idx2 = top_test[int(top_posi_idx1)]
    bot_posi_idx2 = bot_test[int(bot_posi_idx1)]
    sho_posi_idx2 = sho_test[int(sho_posi_idx1)]
    top_nega_idx2 = top_test[int(top_nega_idx1)]
    bot_nega_idx2 = bot_test[int(bot_nega_idx1)]
    sho_nega_idx2 = sho_test[int(sho_nega_idx1)]
    #image path posi & neg
    top_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_posi_idx2)].strip('\r\n')
    bot_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_posi_idx2)].strip('\r\n')
    sho_posi_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_posi_idx2)].strip('\r\n')
    top_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_nega_idx2)].strip('\r\n')
    bot_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_nega_idx2)].strip('\r\n')
    sho_nega_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_nega_idx2)].strip('\r\n')
    #read images posi & neg
    im_top_posi = Image.open(top_posi_img)
    im_bot_posi = Image.open(bot_posi_img)
    im_sho_posi = Image.open(sho_posi_img)
    im_top_nega = Image.open(top_nega_img)
    im_bot_nega = Image.open(bot_nega_img)
    im_sho_nega = Image.open(sho_nega_img)  
    #resize to the same size posi & neg
    im_top_posi = im_top_posi.resize(size, Image.ANTIALIAS)
    im_bot_posi = im_bot_posi.resize(size, Image.ANTIALIAS)
    im_sho_posi = im_sho_posi.resize(size, Image.ANTIALIAS)
    im_top_nega = im_top_nega.resize(size, Image.ANTIALIAS)
    im_bot_nega = im_bot_nega.resize(size, Image.ANTIALIAS)
    im_sho_nega = im_sho_nega.resize(size, Image.ANTIALIAS)
    #image to nparray
    im_top_posi = np.array(im_top_posi)
    im_bot_posi = np.array(im_bot_posi)
    im_sho_posi = np.array(im_sho_posi)
    im_top_nega = np.array(im_top_nega)
    im_bot_nega = np.array(im_bot_nega)
    im_sho_nega = np.array(im_sho_nega)
    #change type to np.int64, np.uint8 (lmdb)
    label.astype(np.int64)
    im_top_posi.astype(np.uint8)
    im_bot_posi.astype(np.uint8)
    im_sho_posi.astype(np.uint8)
    im_top_nega.astype(np.uint8)
    im_bot_nega.astype(np.uint8)
    im_sho_nega.astype(np.uint8)
    #from RGB to BGR
    im_top_posi = np.array([im_top_posi[2,],im_top_posi[1,],im_top_posi[0,]])
    im_bot_posi = np.array([im_bot_posi[2,],im_bot_posi[1,],im_bot_posi[0,]])
    im_sho_posi = np.array([im_sho_posi[2,],im_sho_posi[1,],im_sho_posi[0,]]) 
    im_top_nega = np.array([im_top_nega[2,],im_top_nega[1,],im_top_nega[0,]])
    im_bot_nega = np.array([im_bot_nega[2,],im_bot_nega[1,],im_bot_nega[0,]])
    im_sho_nega = np.array([im_sho_nega[2,],im_sho_nega[1,],im_sho_nega[0,]]) 
    #from (height,width,channel) to (channel,height,width)
    im_top_posi = np.rollaxis(im_top_posi,2,0)
    im_bot_posi = np.rollaxis(im_bot_posi,2,0)
    im_sho_posi = np.rollaxis(im_sho_posi,2,0)
    im_top_nega = np.rollaxis(im_top_nega,2,0)
    im_bot_nega = np.rollaxis(im_bot_nega,2,0)
    im_sho_nega = np.rollaxis(im_sho_nega,2,0)
    #zero mean normalization
    im_top_posi = im_top_posi - VGG_mean[0,:,:,:]
    im_bot_posi = im_bot_posi - VGG_mean[0,:,:,:]
    im_sho_posi = im_sho_posi - VGG_mean[0,:,:,:]
    im_top_nega = im_top_nega - VGG_mean[0,:,:,:]
    im_bot_nega = im_bot_nega - VGG_mean[0,:,:,:]
    im_sho_nega = im_sho_nega - VGG_mean[0,:,:,:]
    #stack over "channel"
    data[count-1,0:3,:,:] = im_top_posi
    data[count-1,3:6,:,:] = im_bot_posi
    data[count-1,6:9,:,:] = im_sho_posi
    data[count-1,9:12,:,:] = im_top_nega
    data[count-1,12:15,:,:] = im_bot_nega
    data[count-1,15:18,:,:] = im_sho_nega
    labels[count-1,:] = label[0]
    
print("\ntesting tuples num (data):")
print(data.shape)
print("\ntesting tuples num (label):")
print(labels.shape)

print("\nwrite to test LMDB.........\n")
map_size = data.nbytes * 10
env2 = lmdb.open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/test_tuples_lmdb2', map_size=map_size)
with env2.begin(write=True) as txn:     
    # txn is a Transaction object
    for i in range(labels.shape[0]):
        datum = caffe.proto.caffe_pb2.Datum()
        datum.channels = data.shape[1]
        datum.height = data.shape[2]
        datum.width = data.shape[3]
        datum.data = data[i].tobytes()
            
        datum.label = int(labels[i])
        str_id = '{:08}'.format(i)

        txn.put(str_id.encode('ascii'), datum.SerializeToString())
print("\ntest LMDB finished\n")