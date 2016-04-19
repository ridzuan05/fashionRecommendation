#!/usr/bin/env python

import numpy as np
# import os

tuples_test_posi = open("./tuples_test_posi.txt").readlines()
tuples_val_posi = open("./tuples_val_posi.txt").readlines()
tuples_test_neg = open("./tuples_test_neg.txt").readlines()
tuples_val_neg = open("./tuples_val_neg.txt").readlines()

# os.system('rm ./tuples_test_posi.txt')
# os.system('rm ./tuples_val_posi.txt')

tuples_test_posi_fp = open("./tuples_test_posi.txt",'w')
tuples_val_posi_fp = open("./tuples_val_posi.txt",'w')
tuples_test_neg_fp = open("./tuples_test_neg.txt",'w')
tuples_val_neg_fp = open("./tuples_val_neg.txt",'w')

mini_user_idx = 0
maxi_user_idx = 988

for i in range(0,989):
	test_val_posi = []
	for j in range(0,len(tuples_test_posi)):
		if (i==int(tuples_test_posi[j].strip('\r\n').split(' ')[0])):
			test_val_posi.append(tuples_test_posi[j])
	for k in range(0,len(tuples_val_posi)):
		if (i==int(tuples_val_posi[k].strip('\r\n').split(' ')[0])):
			test_val_posi.append(tuples_val_posi[k])
	half_length = int(float(len(test_val_posi))/2.0)
	for m in range(0,half_length):
		tuples_test_posi_fp.write(test_val_posi[m])
	for n in range(half_length,len(test_val_posi)):
		tuples_val_posi_fp.write(test_val_posi[n])

	test_val_neg = []
	for j in range(0,len(tuples_test_neg)):
		if (i==int(tuples_test_neg[j].strip('\r\n').split(' ')[0])):
			test_val_neg.append(tuples_test_neg[j])
	for k in range(0,len(tuples_val_neg)):
		if (i==int(tuples_val_neg[k].strip('\r\n').split(' ')[0])):
			test_val_neg.append(tuples_val_neg[k])
	half_length = int(float(len(test_val_neg))/2.0)
	for m in range(0,half_length):
		tuples_test_neg_fp.write(test_val_neg[m])
	for n in range(half_length,len(test_val_neg)):
		tuples_val_neg_fp.write(test_val_neg[n])

tuples_test_posi_fp.close()
tuples_val_posi_fp.close()
tuples_test_neg_fp.close()
tuples_val_neg_fp.close()