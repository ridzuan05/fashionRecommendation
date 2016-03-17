#!/usr/bin/env python

print("\nprepare 'tuples_train_shuffled.txt\n")
import re
train_tuple = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_posi.txt")
neg_train_tuple = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_neg.txt")
train_tuple_content = train_tuple.readlines()
neg_train_tuple_content = neg_train_tuple.readlines()

print("\nto make num_posi = num_neg\n")
for i in range(len(train_tuple_content)):
    train_tuple_content[i] = train_tuple_content[i].strip('\r\n') + ' 1\r\n'
    train_tuple_content.append(neg_train_tuple_content[i].strip('\r\n') + ' 0\r\n')

print("\nshuffle tuples\n")
import random
random.shuffle(train_tuple_content)

print("\nstore shuffled training tuples\n")
train_tuple_shuffled = open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_shuffled.txt','w')
for i in range(len(train_tuple_content)):
    train_tuple_shuffled.write(train_tuple_content[i])
train_tuple.close()
neg_train_tuple.close()
train_tuple_shuffled.close()

print("\nprepare 'tuples_test_shuffled.txt'\n")
test_tuple = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_posi.txt")
neg_test_tuple = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_neg.txt")
test_tuple_content = test_tuple.readlines()
neg_test_tuple_content = neg_test_tuple.readlines()

print("\nto make num_posi = num_neg\n")
for i in range(len(test_tuple_content)):
    test_tuple_content[i] = test_tuple_content[i].strip('\r\n') + ' 1\r\n'
    test_tuple_content.append(neg_test_tuple_content[i].strip('\r\n') + ' 0\r\n')

print("\nshuffle tuples\n")
random.shuffle(test_tuple_content)

print("\nstore shuffled testing tuples\n")
test_tuple_shuffled = open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_shuffled.txt','w')
for i in range(len(test_tuple_content)):
    test_tuple_shuffled.write(test_tuple_content[i])    
test_tuple.close()
neg_test_tuple.close()
test_tuple_shuffled.close()

print("\nprepare lmdb (& hdf5) for training data\n")
import re
tuples_train_count = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_shuffled.txt")
tuples_train = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_train_shuffled.txt")
top_train_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/top_ind_train.txt")
bot_train_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/bottom_ind_train.txt")
sho_train_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/shoe_ind_train.txt")
top_path_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_top.txt")
bot_path_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_bottom.txt")
sho_path_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/img_list/img_list_shoe.txt")
top_train = top_train_f.readlines()
bot_train = bot_train_f.readlines()
sho_train = sho_train_f.readlines()
top_path = top_path_f.readlines()
bot_path = bot_path_f.readlines()
sho_path = sho_path_f.readlines()
top_train_f.close()
bot_train_f.close()
sho_train_f.close()
top_path_f.close()
bot_path_f.close()
sho_path_f.close()
#train tuples num
for i, l in enumerate(tuples_train_count):
            pass
tuples_train_count.close()
print("\ntraining data tuple num: %d\n"%(i+1))
print("\nstack images over channels\n")

import Image
import numpy as np

#zero mean normalization
caffe_root = '/local2/home/tong/caffe-master/'  # this file is expected to be in {caffe_root}/examples/siamese
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
blob = caffe.proto.caffe_pb2.BlobProto()
data = open('/local2/home/tong/fashionRecommendation/data/VGG_mean.binaryproto', 'rb' ).read()
blob.ParseFromString(data)
VGG_mean = np.array( caffe.io.blobproto_to_array(blob) )
VGG_mean.astype(np.uint8)

size = 224, 224
k = 0
count = 0
#initilization for speed up
data = np.zeros((i+1,9,size[0],size[1]),np.uint8)
labels = np.zeros((i+1,1),np.int64)
for line in tuples_train:
    count = count + 1
    if count % 100 == 0:
        print("%d/%d training tuples ready......"%(count, i+1))
    #label 1-posi, 0-neg
    label = np.array([int(re.findall(r'\d+',line)[4])])
    #inter idx
    top_idx1 = re.findall(r'\d+',line)[1]
    bot_idx1 = re.findall(r'\d+',line)[2]
    sho_idx1 = re.findall(r'\d+',line)[3]
    #final idx
    top_idx2 = top_train[int(top_idx1)]
    bot_idx2 = bot_train[int(bot_idx1)]
    sho_idx2 = sho_train[int(sho_idx1)]
    #image path
    top_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_idx2)].strip('\r\n')
    bot_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_idx2)].strip('\r\n')
    sho_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_idx2)].strip('\r\n')
    #read images
    im_top = Image.open(top_img)
    im_bot = Image.open(bot_img)
    im_sho = Image.open(sho_img)
    #resize to the same size
    im_top = im_top.resize(size, Image.ANTIALIAS)
    im_bot = im_bot.resize(size, Image.ANTIALIAS)
    im_sho = im_sho.resize(size, Image.ANTIALIAS)
    #image to nparray
    im_top = np.array(im_top)
    im_bot = np.array(im_bot)
    im_sho = np.array(im_sho)
    #change type to np.int64, np.uint8 (lmdb)
    label.astype(np.int64)
    im_top.astype(np.uint8)
    im_bot.astype(np.uint8)
    im_sho.astype(np.uint8)
    #change type to np.float32 (hdf5)
    #label.astype(np.float32)
    #im_top.astype(np.float32)
    #im_bot.astype(np.float32)
    #im_sho.astype(np.float32)
    #from RGB to BGR
    im_top = np.array([im_top[2,],im_top[1,],im_top[0,]])
    im_bot = np.array([im_bot[2,],im_bot[1,],im_bot[0,]])
    im_sho = np.array([im_sho[2,],im_sho[1,],im_sho[0,]])
    #from (height,width,channel) to (channel,height,width)
    im_top = np.rollaxis(im_top,2,0)
    im_bot = np.rollaxis(im_bot,2,0)
    im_sho = np.rollaxis(im_sho,2,0)
    #zero mean normalization
    im_top = im_top - VGG_mean[0,:,:,:]
    im_bot = im_bot - VGG_mean[0,:,:,:]
    im_sho = im_sho - VGG_mean[0,:,:,:]
    #stack over "channel"
    #im_outfit = np.concatenate((im_top, im_bot, im_sho),axis = 0)
    data[count-1,0:3,:,:] = im_top
    data[count-1,3:6,:,:] = im_bot
    data[count-1,6:9,:,:] = im_sho
    labels[count-1,:] = label[0]
    #from (channel,height,width) to (1,channel,height,width)
    #label = label[np.newaxis, :]
    #im_outfit = im_outfit[np.newaxis, :]
    #for stacking over num
    #if k == 0:
    #    k = 1
    #    data = im_outfit
    #    labels = label
    #else:
    #    data = np.concatenate((data, im_outfit),axis = 0)
    #    labels = np.concatenate((labels, label),axis = 0)
    #count = count + 1

tuples_train.close()

print("\ntraining tuples num (data):")
print(data.shape)
print("\ntraining tuples num (label):")
print(labels.shape)

print("\nwrite to LMDB\n")
import lmdb
map_size = data.nbytes * 10
env = lmdb.open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/train_tuples_lmdb', map_size=map_size)
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

print("\nprepare lmdb (& hdf5) for testing data\n")
tuples_test_count = open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_shuffled.txt')
tuples_test = open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/tuples_test_shuffled.txt')
top_test_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/top_ind_test.txt") 
bot_test_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/bottom_ind_test.txt")
sho_test_f = open("/local2/home/tong/fashionRecommendation/data/Polyvore_small/Exp1c/tuple_180/shoe_ind_test.txt")
top_test = top_test_f.readlines()
bot_test = bot_test_f.readlines()
sho_test = sho_test_f.readlines()
top_test_f.close()
bot_test_f.close()
sho_test_f.close()
#train tuples num
for i, l in enumerate(tuples_test_count):
            pass
tuples_test_count.close()
print("\ntesting data tuple num: %d\n"%(i+1))
print("\nstack images over channels\n")
k = 0
count = 0
#initilization for speed up
data = np.zeros((i+1,9,size[0],size[1]),np.uint8)
labels = np.zeros((i+1,1),np.int64)
for line in tuples_test:
    count = count + 1
    if count % 100 == 0:
        print("%d/%d testing tuples ready......"%(count, i+1))
    #label 1-posi, 0-neg
    label = np.array([int(re.findall(r'\d+',line)[4])])
    #inter idx
    top_idx1 = re.findall(r'\d+',line)[1]
    bot_idx1 = re.findall(r'\d+',line)[2]
    sho_idx1 = re.findall(r'\d+',line)[3]
    #final idx
    top_idx2 = top_test[int(top_idx1)]
    bot_idx2 = bot_test[int(bot_idx1)]
    sho_idx2 = sho_test[int(sho_idx1)]
    #image path
    top_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/top/' + top_path[int(top_idx2)].strip('\r\n')
    bot_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/bottom/' + bot_path[int(bot_idx2)].strip('\r\n')
    sho_img = '/local2/home/tong/fashionRecommendation/data/Polyvore_small/Images/shoe/' + sho_path[int(sho_idx2)].strip('\r\n')
    #read images
    im_top = Image.open(top_img)
    im_bot = Image.open(bot_img)
    im_sho = Image.open(sho_img)
    #resize to the same size
    im_top = im_top.resize(size, Image.ANTIALIAS)
    im_bot = im_bot.resize(size, Image.ANTIALIAS)
    im_sho = im_sho.resize(size, Image.ANTIALIAS)
    #image to nparray
    im_top = np.array(im_top)
    im_bot = np.array(im_bot)
    im_sho = np.array(im_sho)
    #change type to np.int64, np.uint8 (lmdb)
    label.astype(np.int64)
    im_top.astype(np.uint8)
    im_bot.astype(np.uint8)
    im_sho.astype(np.uint8)
    #change type to np.float32 (hdf5)
    #label.astype(np.float32)
    #im_top.astype(np.float32)
    #im_bot.astype(np.float32)
    #im_sho.astype(np.float32)
    #from RGB to BGR
    im_top = np.array([im_top[2,],im_top[1,],im_top[0,]])
    im_bot = np.array([im_bot[2,],im_bot[1,],im_bot[0,]])
    im_sho = np.array([im_sho[2,],im_sho[1,],im_sho[0,]])  
    #from (height,width,channel) to (channel,height,width)
    im_top = np.rollaxis(im_top,2,0)
    im_bot = np.rollaxis(im_bot,2,0)
    im_sho = np.rollaxis(im_sho,2,0)
    #zero mean normalization
    im_top = im_top - VGG_mean[0,:,:,:]
    im_bot = im_bot - VGG_mean[0,:,:,:]
    im_sho = im_sho - VGG_mean[0,:,:,:]
    #stack over "channel"
    #im_outfit = np.concatenate((im_top, im_bot, im_sho),axis = 0)
    data[count-1,0:3,:,:] = im_top
    data[count-1,3:6,:,:] = im_bot
    data[count-1,6:9,:,:] = im_sho
    labels[count-1,:] = label[0]
    #from (channel,height,width) to (1,channel,height,width)
    #label = label[np.newaxis, :]
    #im_outfit = im_outfit[np.newaxis, :]
    #for stacking over num
    #if k == 0:
    #    k = 1
    #    data = im_outfit
    #    labels = label
    #else:
    #   data = np.concatenate((data, im_outfit),axis = 0)
    #   labels = np.concatenate((labels, label),axis = 0)
    #count = count + 1

tuples_test.close()

print("\ntesting tuples num (data):")
print(data.shape)
print("\ntesting tuples num (label):")
print(labels.shape)

print("\nwrite to LMDB\n")
map_size = data.nbytes * 10
env2 = lmdb.open('/local2/home/tong/fashionRecommendation/data/Polyvore_small/test_tuples_lmdb', map_size=map_size)
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

print("FINISHED: (usage) chmod +x file.py")
