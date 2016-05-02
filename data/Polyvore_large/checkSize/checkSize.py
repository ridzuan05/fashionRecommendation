#!/usr/bin/env python

import os

userNames_folder = '/local2/home/tong/fashionRecommendation/data/Polyvore_large/1120_users/images/'
userNames = os.listdir(userNames_folder)

# checkSize.txt
checkSize_fp = open('/local2/home/tong/fashionRecommendation/data/Polyvore_large/checkSize/checkSize.txt','w')

for u in range(0,len(userNames)):

	userContents = os.listdir(userNames_folder+userNames[u])

	checkSize_fp.write(userNames[u]+' ')

	if 'items' in userContents:
		items = userNames_folder+userNames[u]+'/items/full/'
		itemsImgs = os.listdir(items)
		itemsImgsNum = len(itemsImgs)
		checkSize_fp.write('1 '+str(itemsImgsNum)+' ')
	else:
		checkSize_fp.write('0 0 ')

	if 'items_append' in userContents:
		items_append =userNames_folder+userNames[u]+'/items_append/full/'
		items_appendImgs = os.listdir(items_append)
		items_appendImgsNum = len(items_appendImgs)
		checkSize_fp.write('1 '+str(items_appendImgsNum)+'\r\n')
	else:
		checkSize_fp.write('0 0\r\n')

	if 'sets' in userContents:
		sets =userNames_folder+userNames[u]+'/sets/full/'
		setsImgs = os.listdir(sets)
		setsImgsNum = len(setsImgs)
		checkSize_fp.write('1 '+str(setsImgsNum)+'\r\n')
	else:
		checkSize_fp.write('0 0\r\n')

checkSize_fp.close()