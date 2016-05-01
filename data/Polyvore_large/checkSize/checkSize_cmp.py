#!/usr/bin/env python

checkSize = open('./checkSize.txt').readlines()
checkSize_dell = open('./checkSize_dell.txt').readlines()

checkSize_cmp_fp = open('./checkSize_cmp.txt','w')

for u_dell in range(0,len(checkSize_dell)):
	for u in range(0,len(checkSize)):

		checkSize_dell_list = checkSize_dell.strip('\r\n').split(' ')
		checkSize_list = checkSize.strip('\r\n').split(' ')

		# if userName match
		if (checkSize_dell_list[0] == checkSize_list[0]):
			# if userContents don't match
			if (checkSize_dell_list != checkSize_list):

				userName = checkSize_dell_list[0]
				items = str(int(checkSize_dell_list[1])-int(checkSize_list[1]))
				itemsNum = str(int(checkSize_dell_list[2])-int(checkSize_list[2]))
				items_append = str(int(checkSize_dell_list[3])-int(checkSize_list[3]))
				items_appendNum = str(int(checkSize_dell_list[4])-int(checkSize_list[4]))

				checkSize_cmp_fp.write(userName+' '+items+' '+itemsNum+' '+items_append+' '+items_appendNum+'\r\n')

		break

checkSize_cmp_fp.close()